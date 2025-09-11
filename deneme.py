import time
import random
import threading
from collections import deque
from datetime import datetime

# ===================== CLASS DEFINITIONS =====================

class Araba:
    def __init__(self, id, araba_işık_no):
        self.id = id
        self.status = "waiting"  # "waiting", "moving"
        self.araba_işık_no = araba_işık_no

class Yaya:
    def __init__(self, id, yaya_işık_no):
        self.id = id
        self.status = "waiting"  # "waiting", "crossing"
        self.yaya_işık_no = yaya_işık_no

class ArabaIşık:
    def __init__(self, id):
        self.id = id
        self.renk = "red"  # "red", "green"
    
    def get(self):
        return self.renk
    
    def set(self, new_color):
        self.renk = new_color

class YayaIşık:
    def __init__(self, id):
        self.id = id
        self.renk = "red"  # "red", "green"
    
    def get(self):
        return self.renk
    
    def set(self, new_color):
        self.renk = new_color

# ===================== MAIN SYSTEM CLASS =====================

class TrafikSistemi:
    def __init__(self):
        # Arrays - Dictionary kullanarak (1-8 index)
        self.araba_işıkları = {i: ArabaIşık(i) for i in range(1, 9)}
        self.yaya_işıkları = {i: YayaIşık(i) for i in range(1, 9)}
        self.araba_bekleyenler = {i: deque() for i in range(1, 9)}  # FIFO queue
        self.yaya_bekleyenler = {i: deque() for i in range(1, 9)}
        
        # Sistem değişkenleri
        self.aktif_döngü = 1  # 1:(1,2), 2:(3,4), 3:(5,6), 4:(7,8)
        self.döngü_sayacı = 0
        self.YEŞİL_SÜRE = 30    # 30 saniye yeşil
        self.KIRMIZI_SÜRE = 90  # 90 saniye kırmızı (diğer 3 döngü süresi)
        
        self.current_time = 0
        self.next_vehicle_id = 1
        self.next_pedestrian_id = 1
        
        # Sistem kontrolü
        self.running = False
        self.thread = None

    # ===================== INITIALIZATION =====================

    def initialize(self):
        """Sistemi başlat"""
        print("Trafik sistemi başlatılıyor...")
        
        # Tüm ışıkları kırmızı yap
        for i in range(1, 9):
            self.araba_işıkları[i].set("red")
            self.yaya_işıkları[i].set("red")
        
        # İlk döngüyü başlat (1,2 numaralı ışıklar yeşil)
        self.aktif_döngü = 1
        self.döngü_sayacı = 0
        self.set_active_phase()
        
        print("Sistem başlatıldı!")

    def set_active_phase(self):
        """Aktif fazı ayarla"""
        # Önce tüm araba ışıklarını kırmızı yap
        for i in range(1, 9):
            self.araba_işıkları[i].set("red")
            self.yaya_işıkları[i].set("red")
        
        # Aktif döngüye göre araba ışıklarını yeşil yap
        if self.aktif_döngü == 1:  # Işık 1,2 yeşil
            self.araba_işıkları[1].set("green")
            self.araba_işıkları[2].set("green")
            print(f"[{self.get_timestamp()}] Döngü 1 aktif - Işık 1,2 yeşil")
            
        elif self.aktif_döngü == 2:  # Işık 3,4 yeşil
            self.araba_işıkları[3].set("green")
            self.araba_işıkları[4].set("green")
            print(f"[{self.get_timestamp()}] Döngü 2 aktif - Işık 3,4 yeşil")
            
        elif self.aktif_döngü == 3:  # Işık 5,6 yeşil
            self.araba_işıkları[5].set("green")
            self.araba_işıkları[6].set("green")
            print(f"[{self.get_timestamp()}] Döngü 3 aktif - Işık 5,6 yeşil")
            
        elif self.aktif_döngü == 4:  # Işık 7,8 yeşil
            self.araba_işıkları[7].set("green")
            self.araba_işıkları[8].set("green")
            print(f"[{self.get_timestamp()}] Döngü 4 aktif - Işık 7,8 yeşil")
        
        # Yaya ışıkları şimdilik hep kırmızı (basitlik için)

    # ===================== TRAFFIC GENERATION =====================

    def generate_random_traffic(self):
        """Rastgele trafik oluştur"""
        # Her 3 saniyede bir rastgele araba oluştur
        if self.current_time % 3 == 0:
            if random.randint(1, 100) <= 40:  # %40 şans
                işık_no = random.randint(1, 8)
                araba = Araba(self.next_vehicle_id, işık_no)
                self.next_vehicle_id += 1
                self.araba_bekleyenler[işık_no].append(araba)
                print(f"[{self.get_timestamp()}] Yeni araba eklendi - ID: {araba.id}, Işık: {işık_no}")
        
        # Her 5 saniyede bir rastgele yaya oluştur
        if self.current_time % 5 == 0:
            if random.randint(1, 100) <= 30:  # %30 şans
                işık_no = random.randint(1, 8)
                yaya = Yaya(self.next_pedestrian_id, işık_no)
                self.next_pedestrian_id += 1
                self.yaya_bekleyenler[işık_no].append(yaya)
                print(f"[{self.get_timestamp()}] Yeni yaya eklendi - ID: {yaya.id}, Işık: {işık_no}")

    # ===================== TRAFFIC PROCESSING =====================

    def process_traffic(self):
        """Trafiği işle"""
        # Yeşil ışıktaki arabaları geçir
        for işık_no in range(1, 9):
            if self.araba_işıkları[işık_no].get() == "green":
                # Her saniye 1 araba geçebilir
                if len(self.araba_bekleyenler[işık_no]) > 0:
                    araba = self.araba_bekleyenler[işık_no].popleft()
                    araba.status = "moving"
                    print(f"[{self.get_timestamp()}] Araba geçti - ID: {araba.id}, Işık: {işık_no}")
        
        # Yaya işleme (şimdilik sadece kuyrukta bekletiyoruz)
        # Yaya ışıkları genelde kırmızı olduğu için sadece bekliyorlar

    # ===================== PHASE MANAGEMENT =====================

    def check_phase_change(self):
        """Faz değişimi kontrol et"""
        self.döngü_sayacı += 1
        
        # 30 saniye tamamlandıysa bir sonraki döngüye geç
        if self.döngü_sayacı >= self.YEŞİL_SÜRE:
            self.döngü_sayacı = 0
            self.aktif_döngü += 1
            
            # Döngü 4'ten sonra 1'e geri dön
            if self.aktif_döngü > 4:
                self.aktif_döngü = 1
            
            self.set_active_phase()

    # ===================== STATUS AND REPORTING =====================

    def print_status(self):
        """Sistem durumunu yazdır"""
        print(f"\n=== Zaman: {self.current_time}s - Döngü: {self.aktif_döngü} ({self.döngü_sayacı}/{self.YEŞİL_SÜRE}) ===")
        
        for i in range(1, 9):
            araba_durum = self.araba_işıkları[i].get()
            bekleyen_araba = len(self.araba_bekleyenler[i])
            bekleyen_yaya = len(self.yaya_bekleyenler[i])
            
            print(f"Işık {i}: {araba_durum.upper()} - Bekleyen araba: {bekleyen_araba}, Bekleyen yaya: {bekleyen_yaya}")
        print()

    def get_timestamp(self):
        """Zaman damgası al"""
        return datetime.now().strftime("%H:%M:%S")

    def get_system_status(self):
        """Sistem durumunu JSON formatında döndür (Flask için)"""
        status = {
            "current_time": self.current_time,
            "active_cycle": self.aktif_döngü,
            "cycle_progress": f"{self.döngü_sayacı}/{self.YEŞİL_SÜRE}",
            "lights": {},
            "queues": {}
        }
        
        for i in range(1, 9):
            status["lights"][f"light_{i}"] = {
                "car_light": self.araba_işıkları[i].get(),
                "pedestrian_light": self.yaya_işıkları[i].get()
            }
            status["queues"][f"queue_{i}"] = {
                "waiting_cars": len(self.araba_bekleyenler[i]),
                "waiting_pedestrians": len(self.yaya_bekleyenler[i])
            }
        
        return status

    # ===================== SIMULATION CONTROL =====================

    def run_simulation(self, duration=300):
        """Simülasyon çalıştır - Thread'de çalışacak"""
        self.initialize()
        start_time = self.current_time
        
        print(f"Simülasyon başlatıldı - Süre: {duration} saniye")
        
        while self.running and (self.current_time - start_time) < duration:
            # 1. Rastgele trafik oluştur
            self.generate_random_traffic()
            
            # 2. Trafiği işle
            self.process_traffic()
            
            # 3. Faz değişimi kontrol et
            self.check_phase_change()
            
            # 4. Her 10 saniyede durum yazdır
            if self.current_time % 10 == 0:
                self.print_status()
            
            # 5. Zamanı ilerlet ve bekle
            self.current_time += 1
            time.sleep(1)  # 1 saniye bekle
        
        print("Simülasyon tamamlandı!")
        self.running = False

    def start(self):
        """Sistemi başlat (thread'de)"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_simulation, args=(300,))
            self.thread.daemon = True  # Ana program kapandığında thread'de kapansın
            self.thread.start()
            return True
        return False

    def stop(self):
        """Sistemi durdur"""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join(timeout=2)  # En fazla 2 saniye bekle
            return True
        return False

    def is_running(self):
        """Sistem çalışıyor mu?"""
        return self.running

# ===================== MAIN EXECUTION =====================

def main():
    """Ana program - test için"""
    sistem = TrafikSistemi()
    
    try:
        print("Trafik Işığı Sistemi")
        print("Çıkış için Ctrl+C basın")
        
        sistem.start()
        
        # Ana thread'i canlı tut
        while sistem.is_running():
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nSistem durduruluyor...")
        sistem.stop()
        print("Sistem durduruldu!")

if __name__ == "__main__":
    main()