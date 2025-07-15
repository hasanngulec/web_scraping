#!/usr/bin/env python3
"""
geocoding_cli.py  –  Tek dosyada coğrafi kodlama kütüphanesi + CLI

• JSON içinden başlıkları okuyup ardışık olarak 4 algoritma uygular
  (Nominatim basic ➊, Geliştirilmiş Nominatim ➋, Photon ➌, OpenCage ➍)
• Çıktıları 2 JSON dosyasına yazar: coor_resolved.json & coor_remaining.json
• İstendiğinde kütüphane gibi de içe aktarılabilir (from geocoding_cli import GeocodingSystem)

Kullanım örneği:
    python geocoding_cli.py --in balat.json --city "İstanbul" --country Türkiye
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim, Photon

# ------------------------------------------------------------
# Opsiyonel: OpenCage
try:
    from opencage.geocoder import OpenCageGeocode  # type: ignore
except ImportError:  # kitaplık yoksa sorun değil; 4. aşama atlanır
    OpenCageGeocode = None

load_dotenv()


class GeocodingSystem:
    """OpenStreetMap tabanlı 4-aşamalı coğrafi kodlayıcı."""

    def __init__(self, sleep: float = 1.0):
        self.sleep = sleep  # API saygısı
        self.nominatim = Nominatim(user_agent="geo_cli")
        self.opencage_key: str | None = os.getenv("OPENCAGE_API_KEY")
        self._reset()

    # -------------------------- JSON Yardımcıları ------------------------- #
    def _load_json(self, path: str | Path, default: List[Dict]) -> List[Dict]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return default

    def _save_json(self, path: str | Path, data: List[Dict]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _reset(self) -> None:
        self.resolved: List[Dict] = []
        self.remaining: List[Dict] = []

    # ------------------------- Veri Yükleme ------------------------------- #
    def load_locations(self, infile: str | Path) -> List[Dict]:
        data = self._load_json(infile, [])
        locs: List[Dict] = []
        for item in data:
            if isinstance(item, dict) and "title" in item:
                locs.append({
                    "title": item["title"],
                    "content": item.get("content", ""),
                    "labels": item.get("labels", []),
                    "coordinates": item.get("coordinates"),
                })
        return locs

    # ------------------------- AŞAMA 1: Nominatim Basic ------------------- #
    def _nominatim(self, title: str, city: str, country: str, district: str = "") -> Tuple[float, float] | None:
        query = ", ".join(x for x in (title, district, city, country) if x)
        try:
            res = self.nominatim.geocode(query, timeout=10)
            if res:
                return res.latitude, res.longitude
        except (GeocoderTimedOut, GeocoderUnavailable):
            pass
        return None

    # -------------------- AŞAMA 2: Nominatim Enhanced --------------------- #
    def _nominatim_variants(self, title: str, city: str, country: str, content: str, district: str = "") -> Tuple[float, float] | None:
        tokens = [
            f"{title}, {country}",
            f"{title} mahallesi, {country}",
            f"{title} semti, {country}",
            f"{title} meydanı, {country}",
            f"{title} caddesi, {country}",
        ]
        if city:
            tokens.insert(0, f"{title}, {city}, {country}")
        if district:
            tokens.insert(0, f"{title}, {district}, {city}, {country}")
        # İçerikteki şehir isimlerine bak
        for keyword in ("istanbul", "fatih", "balat", "fener", "ayvansaray"):
            if keyword in content.lower():
                tokens.append(f"{title}, {keyword.title()}, {country}")
        for q in tokens:
            try:
                res = self.nominatim.geocode(q, timeout=10)
                if res:
                    return res.latitude, res.longitude
            except (GeocoderTimedOut, GeocoderUnavailable):
                continue
            time.sleep(self.sleep)
        return None

    # ------------------------- AŞAMA 3: Photon ---------------------------- #
    def _photon(self, title: str, city: str, country: str, district: str = "") -> Tuple[float, float] | None:
        geo = Photon(user_agent="geo_cli_photon")
        variants = [
            f"{title}, {country}",
            title,
        ]
        if city:
            variants.insert(0, f"{title}, {city}, {country}")
        if district:
            variants.insert(0, f"{title}, {district}, {city}, {country}")
        for q in variants:
            try:
                res = geo.geocode(q, timeout=10)
                if res:
                    return res.latitude, res.longitude
            except Exception:
                continue
            time.sleep(self.sleep)
        return None

    # ------------------------- AŞAMA 4: OpenCage -------------------------- #
    def _opencage(self, title: str, city: str, country: str, district: str = "") -> Tuple[float, float] | None:
        if not (self.opencage_key and OpenCageGeocode):
            return None
        coder = OpenCageGeocode(self.opencage_key)
        query = ", ".join(x for x in (title, district, city, country) if x)
        try:
            results = coder.geocode(query, countrycode="tr")
            if results:
                g = results[0]["geometry"]
                return g["lat"], g["lng"]
        except Exception:
            pass
        return None

    # ------------------------- PIPELINE ---------------------------------- #
    def resolve(self, locations: List[Dict], *, city: str = "", country: str = "Türkiye", district: str = "") -> None:
        self._reset()
        candidates = locations
        for step_name, step_fn in [
            ("nominatim_basic",       lambda loc: self._nominatim(loc["title"], city, country, district)),
            ("nominatim_variants",    lambda loc: self._nominatim_variants(loc["title"], city, country, loc["content"], district)),
            ("photon",                lambda loc: self._photon(loc["title"], city, country, district)),
            ("opencage",              lambda loc: self._opencage(loc["title"], city, country, district)),
        ]:
            next_round: List[Dict] = []
            for loc in candidates:
                if loc.get("coordinates"):
                    self.resolved.append(loc)
                    continue
                coords = step_fn(loc)
                if coords:
                    lat, lon = coords
                    loc["coordinates"] = {
                        "latitude": lat,
                        "longitude": lon,
                        "method": step_name,
                    }
                    self.resolved.append(loc)
                else:
                    next_round.append(loc)
                time.sleep(self.sleep)
            candidates = next_round
            if not candidates:
                break  # hepsi bulundu
        self.remaining = candidates

    # ------------------------- Özet -------------------------------------- #
    def summary(self) -> Dict:
        return {
            "found": len(self.resolved),
            "missing": len(self.remaining),
        }

    # ------------------------- Kaydet ------------------------------------ #
    def save_results(self, resolved_path: str, remaining_path: str) -> None:
        self._save_json(resolved_path, self.resolved)
        self._save_json(remaining_path, self.remaining)


# ===================================================================== #
# CLI
# ===================================================================== #

def _cli() -> None:  # pragma: no cover
    p = argparse.ArgumentParser(description="JSON lokasyon başlıklarını coğrafi kodlar")
    p.add_argument("--in", dest="infile", required=True, help="Girdi JSON yolu")
    p.add_argument("--city", default="İstanbul", help="Varsayılan şehir (opsiyonel)")
    p.add_argument("--country", default="Türkiye", help="Varsayılan ülke")
    p.add_argument("--district", default="", help="Varsayılan semt/ilçe/mahalle (opsiyonel)")
    p.add_argument("--out-resolved", default="coor_resolved.json")
    p.add_argument("--out-remaining", default="coor_remaining.json")
    args = p.parse_args()

    geo = GeocodingSystem()
    locs = geo.load_locations(args.infile)
    geo.resolve(locs, city=args.city, country=args.country, district=args.district)
    geo.save_results(args.out_resolved, args.out_remaining)

    s = geo.summary()
    print(f"\nBulunan  : {s['found']}")
    print(f"Bulunamayan: {s['missing']}")
    print(f"Çıktılar   : {args.out_resolved}, {args.out_remaining}\n")


if __name__ == "__main__":  # pragma: no cover
    _cli()
