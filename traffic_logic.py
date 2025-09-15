from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from collections import deque
import random
import time
import threading

# ENUM AND CLASS DEFINITIONS
class Status(Enum):
    MOVING = "moving"
    STOPPED = "stopped"
    COMPLETED = "completed"

class Color(Enum):
    RED = "red"
    GREEN = "green"
    

@dataclass
class Car:
    id: int
    status: Status
    carLightId: int

@dataclass
class Walker:
    id: int
    status: Status
    walkLightId: int

@dataclass
class CarLight:
    id: int
    color: Color

    def getColor(self) -> Color:
        return self.color
    
    def setColor(self, color: Color):
        self.color = color

@dataclass
class WalkLight:
    id: int
    color: Color

    def getColor(self) -> Color:
        return self.color
    
    def setColor(self, color: Color):
        self.color = color

# MAIN SYSTEM
class TrafficSystem:
    def __init__(self):
        #diziler ve dictler
        self.carLights = {i: CarLight(i, Color.RED) for i in range(1, 9)}
        self.walkLights = {i: WalkLight(i, Color.RED) for i in range(1, 9)}
        self.waitingCars = {i : deque() for i in range(1,9)}
        self.waitingWalkers = {i : deque() for i in range(1,9)}

        #sistem değişkenleri
        self.current_time = 0
        self.next_car_id = 1
        self.next_walker_id = 1

        self.green_duration = 10    # 10 saniye yeşil

        self.active_cycle = 1  # 1:(1,2), 2:(3,4), 3:(5,6), 4:(7,8)
        self.cycle_counter = 0

        self.running = False
        self.thread = None

        # Kullanıcıdan alınacak parametreler
        self.car_interval = 1
        self.car_count = 3
        self.walker_interval = 1
        self.walker_count = 3


    #sistemi başlatacağız
    def initialize(self):
        print("Trafik sistemi başlatılıyor!")

        #tüm ışıkları kırmızı yapacağız
        # for i in range(1, 9):
        #     self.carLights[i].setColor(Color.RED)
        #     self.walkLights[i].setColor(Color.RED)

        #ilk döngüyü başlatacağız (1,2 numaralı ışıklar yeşil)
        self.active_cycle = 1
        self.cycle_counter = 0
        self.set_active_cycle()

        print("Trafik sistemi başlatıldı.")
    
    # aktif döngüyü ayarlayacağız
    def set_active_cycle(self):
        for i in range(1, 9):
            self.carLights[i].setColor(Color.RED)
            self.walkLights[i].setColor(Color.RED)

        # aktif döngüye göre ışıkları ayarla
        if self.active_cycle == 1:
            self.carLights[1].setColor(Color.GREEN)
            self.carLights[2].setColor(Color.GREEN)

            self.walkLights[1].setColor(Color.GREEN)
            self.walkLights[3].setColor(Color.GREEN)

            print(f"[{self.get_timestamp()}] Döngü 1 aktif - Trafik Işık 1,2; Yaya Işık 1,3 yeşil")

        elif self.active_cycle == 2:
            self.carLights[3].setColor(Color.GREEN)
            self.carLights[4].setColor(Color.GREEN)

            self.walkLights[6].setColor(Color.GREEN)
            self.walkLights[8].setColor(Color.GREEN)
            
            print(f"[{self.get_timestamp()}] Döngü 2 aktif - Trafik Işık 3,4; Yaya Işık 6,8 yeşil")
        
        elif self.active_cycle == 3:
            self.carLights[5].setColor(Color.GREEN)
            self.carLights[6].setColor(Color.GREEN)

            self.walkLights[5].setColor(Color.GREEN)
            self.walkLights[7].setColor(Color.GREEN)

            print(f"[{self.get_timestamp()}] Döngü 3 aktif - Trafik Işık 5,6; Yaya Işık 5,7 yeşil")
        
        elif self.active_cycle == 4:
            self.carLights[7].setColor(Color.GREEN)
            self.carLights[8].setColor(Color.GREEN)

            self.walkLights[2].setColor(Color.GREEN)
            self.walkLights[4].setColor(Color.GREEN)

            print(f"[{self.get_timestamp()}] Döngü 4 aktif - Trafik Işık 7,8; Yaya Işık 2,4 yeşil")

    #random insan ve araba oluşturacağız
    def generate_Random(self):
        # Araba oluşturma
        if self.current_time % self.car_interval == 0:
            for _ in range(self.car_count):
                light_id = random.randint(1,8)
                car = Car(self.next_car_id, Status.STOPPED, light_id)
                self.waitingCars[light_id].append(car)
                self.next_car_id += 1
                print(f"[{self.get_timestamp()}] Araba {car.id} ışık {light_id}'de bekliyor.")

        # Yaya oluşturma
        if self.current_time % self.walker_interval == 0:
            for _ in range(self.walker_count):
                light_id = random.randint(1,8)
                walker = Walker(self.next_walker_id, Status.STOPPED, light_id)
                self.waitingWalkers[light_id].append(walker)
                self.next_walker_id += 1
                print(f"[{self.get_timestamp()}] Yaya {walker.id} ışık {light_id}'de bekliyor.")


    #trafik işleyeceğiz
    def process_Traffic(self):
        for light_id in range(1, 9):
            if self.carLights[light_id].getColor() == Color.GREEN:
                if self.waitingCars[light_id]:
                    sil = 0
                    while sil < 4 and self.waitingCars[light_id]:
                        car = self.waitingCars[light_id].popleft()
                        car.status = Status.MOVING
                        print(f"[{self.get_timestamp()}] Araba {car.id} ışık {light_id}'den geçti.")
                        car.status = Status.COMPLETED
                        sil += 1
            if self.walkLights[light_id].getColor() == Color.GREEN:
                if self.waitingWalkers[light_id]:
                    walker = self.waitingWalkers[light_id].popleft()
                    walker.status = Status.MOVING
                    print(f"[{self.get_timestamp()}] Yaya {walker.id} ışık {light_id}'den geçti.")
                    walker.status = Status.COMPLETED


    #faz kontrolü
    def check_phase_change(self):

        self.cycle_counter += 1

        if self.cycle_counter >= self.green_duration:  # Her 10 saniyede bir döngüyü değiştir
            self.active_cycle += 1
            self.cycle_counter = 0

            if self.active_cycle > 4:
                self.active_cycle = 1      
            self.set_active_cycle()

    def get_timestamp(self):
        return datetime.now().strftime("%H:%M:%S")
    

    def print_status(self):
        """Sistem durumunu yazdır"""
        print(f"\n=== Zaman: {self.current_time}s - Döngü: {self.active_cycle} ({self.cycle_counter}/{self.green_duration}) ===")

        for i in range(1, 9):
            araba_durum = self.carLights[i].getColor()
            bekleyen_araba = len(self.waitingCars[i])
            bekleyen_yaya = len(self.waitingWalkers[i])

            print(f"Işık {i}: {araba_durum} - Bekleyen araba: {bekleyen_araba}, Bekleyen yaya: {bekleyen_yaya}")
        print()


    def get_system_status(self):
        """Sistem durumunu JSON formatında döndür (Flask için)"""
        status = {
            "current_time": self.current_time,
            "active_cycle": self.active_cycle,
            "cycle_progress": f"{self.cycle_counter}/{self.green_duration}",
            "lights": {},
            "queues": {}
        }
            
        
        for i in range(1, 9):
            status["lights"][f"light_{i}"] = {
                "car_light": self.carLights[i].getColor().value,  # .value ekle!
                "pedestrian_light": self.walkLights[i].getColor().value  # .value ekle!
            }
            status["queues"][f"queue_{i}"] = {
                "waiting_cars": len(self.waitingCars[i]),
                "waiting_pedestrians": len(self.waitingWalkers[i]),
                "waiting_cars_ids": [car.id for car in self.waitingCars[i]],
                "waiting_pedestrians_ids": [walker.id for walker in self.waitingWalkers[i]]
            }
        
        return status



    #run denememeee
    def run_simulation(self, duration=60):
        self.initialize()
        start_time = self.current_time

        print(f"Simülasyon başlatıldı - Süre: {duration} saniye")

        while self.running and (self.current_time - start_time) < duration:
            self.generate_Random()
            self.process_Traffic()
            self.check_phase_change()

            # if self.current_time % 10 == 0:
            #     self.print_status()

            # if self.current_time % 10 == 0:
            #     for i in range(1, 9):
            #         print(f"Işık {i}: bekleyen arabalar: {[car.id for car in self.waitingCars[i]]}")
                
            
            self.current_time += 1
            time.sleep(1)  # 1 saniye bekle 

        print("Simülasyon tamamlandı.")
        self.running = False



    def start(self):
        """Sistemi başlat (thread'de)"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_simulation, args=(60,))
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
    

def main():
    """Ana program - test için"""
    sistem = TrafficSystem()
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

