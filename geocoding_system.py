"""
Coğrafi Kodlama Sistemi
OpenStreetMap tabanlı lokasyon eşleştirme sistemi
"""

import json
import os
from typing import List, Dict, Tuple, Optional
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from rapidfuzz import fuzz
import time
from dotenv import load_dotenv

load_dotenv()

class GeocodingSystem:
    """4 aşamalı coğrafi kodlama sistemi"""
    
    def __init__(self):
        self.nominatim = Nominatim(user_agent="web_scraper_geocoder")
        self.opencage_key = os.getenv("OPENCAGE_API_KEY")
        self.locationiq_key = os.getenv("LOCATIONIQ_API_KEY")
        
        # Sonuç dosyaları
        self.resolved_file = "bulunanlar.json"
        self.remaining_file = "kalanlar.json"
        
        # Mevcut sonuçları yükle
        self.resolved_locations = self._load_json(self.resolved_file, [])
        self.remaining_locations = self._load_json(self.remaining_file, [])
    
    def _load_json(self, filename: str, default: List) -> List:
        """JSON dosyasını güvenli şekilde yükle"""
        try:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Dosya yüklenirken hata: {e}")
        return default
    
    def _save_json(self, filename: str, data: List) -> None:
        """JSON dosyasını güvenli şekilde kaydet"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Dosya kaydedilirken hata: {e}")
    
    def _update_files(self) -> None:
        """Dosyaları güncelle"""
        self._save_json(self.resolved_file, self.resolved_locations)
        self._save_json(self.remaining_file, self.remaining_locations)
    
    def load_locations_from_file(self, filename: str) -> List[Dict]:
        """Seçilen JSON dosyasından lokasyonları yükle"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Sadece title alanı olan öğeleri al
            locations = []
            for item in data:
                if isinstance(item, dict) and 'title' in item:
                    location = {
                        'title': item['title'],
                        'content': item.get('content', ''),
                        'labels': item.get('labels', []),
                        'coordinates': item.get('coordinates', None)
                    }
                    locations.append(location)
            
            return locations
        except Exception as e:
            print(f"Dosya yüklenirken hata: {e}")
            return []
    
    def stage1_nominatim_basic(self, locations: List[Dict], city: str = '', country: str = 'Türkiye') -> Tuple[List[Dict], List[Dict]]:
        """Aşama 1: Nominatim ile temel sorgu"""
        resolved = []
        remaining = []
        for location in locations:
            if location.get('coordinates'):
                resolved.append(location)
                continue
            title = location['title']
            query = title
            if city:
                query += f", {city}"
            if country:
                query += f", {country}"
            try:
                result = self.nominatim.geocode(query, timeout=10)
                if result:
                    location['coordinates'] = {
                        'latitude': result.latitude,
                        'longitude': result.longitude,
                        'method': 'nominatim_basic',
                        'query': query
                    }
                    resolved.append(location)
                else:
                    remaining.append(location)
            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                print(f"Nominatim hatası ({title}): {e}")
                remaining.append(location)
            time.sleep(1)
        return resolved, remaining

    def stage2_enhanced_queries(self, locations: List[Dict], city: str = '', country: str = 'Türkiye') -> Tuple[List[Dict], List[Dict]]:
        """Aşama 2: Geliştirilmiş lokasyon sorguları"""
        resolved = []
        remaining = []
        turkish_cities = [
            "İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", 
            "Konya", "Gaziantep", "Şanlıurfa", "Kocaeli", "Mersin", 
            "Diyarbakır", "Hatay", "Manisa", "Kayseri", "Samsun", "Balıkesir",
            "Kahramanmaraş", "Van", "Aydın", "Tekirdağ", "Sakarya", "Muğla",
            "Eskişehir", "Denizli", "Trabzon", "Erzurum", "Ordu", "Afyonkarahisar"
        ]
        for location in locations:
            if location.get('coordinates'):
                resolved.append(location)
                continue
            title = location['title']
            queries = []
            if city:
                queries.append(f"{title}, {city}, {country}")
            queries += [
                f"{title}, {country}",
                f"{title} mahallesi, {country}",
                f"{title} semti, {country}",
                f"{title} meydanı, {country}",
                f"{title} caddesi, {country}"
            ]
            content = location.get('content', '').lower()
            for tcity in turkish_cities:
                if tcity.lower() in content:
                    queries.append(f"{title}, {tcity}, {country}")
                    break
            resolved_location = None
            for query in queries:
                try:
                    result = self.nominatim.geocode(query, timeout=10)
                    if result:
                        location['coordinates'] = {
                            'latitude': result.latitude,
                            'longitude': result.longitude,
                            'method': 'enhanced_queries',
                            'query': query
                        }
                        resolved_location = location
                        break
                except (GeocoderTimedOut, GeocoderUnavailable) as e:
                    print(f"Geliştirilmiş sorgu hatası ({title}): {e}")
                    continue
                time.sleep(1)
            if resolved_location:
                resolved.append(resolved_location)
            else:
                remaining.append(location)
        return resolved, remaining

    def stage2_photon(self, locations: List[Dict], city: str = '', country: str = 'Türkiye') -> Tuple[List[Dict], List[Dict]]:
        """Aşama 2: Photon (OpenStreetMap) ile gelişmiş sorgu varyasyonları"""
        from geopy.geocoders import Photon
        resolved = []
        remaining = []
        geolocator = Photon(user_agent="web_scraper_photon")
        for location in locations:
            if location.get('coordinates'):
                resolved.append(location)
                continue
            title = location['title']
            queries = []
            if city:
                queries.append(f"{title}, {city}, {country}")
            queries += [
                f"{title}, {country}",
                f"{title} mahallesi, {country}",
                f"{title} semti, {country}",
                f"{title} meydanı, {country}",
                f"{title} caddesi, {country}",
                f"{title}"
            ]
            resolved_location = None
            for query in queries:
                try:
                    result = geolocator.geocode(query, timeout=10)
                    if result:
                        location['coordinates'] = {
                            'latitude': result.latitude,
                            'longitude': result.longitude,
                            'method': 'photon',
                            'query': query
                        }
                        resolved_location = location
                        break
                except Exception as e:
                    print(f"Photon hatası ({title}): {e}")
                    continue
                time.sleep(1)
            if resolved_location:
                resolved.append(resolved_location)
            else:
                remaining.append(location)
        return resolved, remaining

    def stage3_opencage_api(self, locations: List[Dict], city: str = '', country: str = 'Türkiye') -> Tuple[List[Dict], List[Dict]]:
        """Aşama 3: OpenCage API kullanımı"""
        if not self.opencage_key:
            print("OpenCage API anahtarı bulunamadı!")
            return [], locations
        try:
            from opencage.geocoder import OpenCageGeocode
            geocoder = OpenCageGeocode(self.opencage_key)
        except ImportError:
            print("OpenCage kütüphanesi yüklü değil!")
            return [], locations
        resolved = []
        remaining = []
        for location in locations:
            if location.get('coordinates'):
                continue  # Zaten koordinatı olanları atla
            title = location['title']
            query = title
            if city:
                query += f", {city}"
            if country:
                query += f", {country}"
            try:
                results = geocoder.geocode(query, countrycode='tr')
                if results:
                    result = results[0]
                    location['coordinates'] = {
                        'latitude': result['geometry']['lat'],
                        'longitude': result['geometry']['lng'],
                        'method': 'opencage_api',
                        'query': query
                    }
                    resolved.append(location)
                else:
                    remaining.append(location)
            except Exception as e:
                print(f"OpenCage hatası ({title}): {e}")
                remaining.append(location)
            time.sleep(1)
        return resolved, remaining

    def stage4_manual_input(self, locations: List[Dict], city: str = '', country: str = 'Türkiye') -> Tuple[List[Dict], List[Dict]]:
        return [], locations

    def process_stage(self, stage: int, locations: List[Dict], city: str = '', country: str = 'Türkiye') -> Dict:
        if stage == 1:
            resolved, remaining = self.stage1_nominatim_basic(locations, city, country)
        elif stage == 2:
            resolved, remaining = self.stage2_enhanced_queries(locations, city, country)
        elif stage == 3:
            resolved, remaining = self.stage3_opencage_api(locations, city, country)
        elif stage == 4:
            resolved, remaining = self.stage4_manual_input(locations, city, country)
        else:
            return {"error": "Geçersiz aşama numarası"}
        # --- Accumulate all found locations across stages ---
        # Build a dict for fast lookup and deduplication by title
        prev_resolved = {loc['title']: loc for loc in self.resolved_locations if loc.get('coordinates')}
        for loc in resolved:
            if loc.get('coordinates'):
                prev_resolved[loc['title']] = loc
        self.resolved_locations = list(prev_resolved.values())
        self.remaining_locations = remaining
        self._update_files()
        return {
            "resolved_count": len(resolved),
            "remaining_count": len(remaining),
            "resolved": resolved,
            "remaining": remaining,
            "stage": stage
        }
    
    def get_summary(self) -> Dict:
        """Mevcut durum özeti"""
        return {
            "total_resolved": len(self.resolved_locations),
            "total_remaining": len(self.remaining_locations),
            "resolved_locations": self.resolved_locations,
            "remaining_locations": self.remaining_locations
        }
    
    def reset_progress(self) -> None:
        """İlerlemeyi sıfırla"""
        self.resolved_locations = []
        self.remaining_locations = []
        self._update_files() 