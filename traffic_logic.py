from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from collections import deque
import random
import time

# ENUM AND CLASS DEFINITIONS
class Status(Enum):
    MOVING = "moving"
    STOPPED = "stopped"
    COMPLETED = "completed"

class Color(Enum):
    RED = "red"
    YELLOW = "yellow"
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

        self.active_cycle = 1  # 1:(1,2), 2:(3,4), 3:(5,6), 4:(7,8)
        self.cycle_counter = 0

        self.running = True


    #sistemi başlatacağız
    def initialize(self):
        print("Trafik sistemi başlatılıyor!")

        #tüm ışıkları kırmızı yapacağız
        for i in range(1, 9):
            self.carLights[i].setColor(Color.RED)
            self.walkLights[i].setColor(Color.RED)

        #ilk döngüyü başlatacağız (1,2 numaralı ışıklar yeşil)
        self.active_cycle = 1
        self.cycle_counter = 0
        self.set_active_cycle()

        print("Trafik sistemi başlatıldı.")

        # while True:
        #     self.generate_Random()
        #     self.current_time += 1
        #     time.sleep(1)  # 1 saniye bekle (simülasyon için)

        #     if self.current_time % 10 == 0:
        #         print("bekleyen arabalar")
        #         for i in range(1,9):
        #             print(self.waitingCars[i])

        #         print("bekleyen yayalar")
        #         for i in range(1,9):
        #             print(self.waitingWalkers[i])
    
    # aktif döngüyü ayarlayacağız
    def set_active_cycle(self):
        for i in range(1, 9):
            self.carLights[i].setColor(Color.RED)
            self.walkLights[i].setColor(Color.RED)

        # aktif döngüye göre ışıkları ayarla
        if self.active_cycle == 1:
            self.carLights[1].setColor(Color.GREEN)
            self.carLights[2].setColor(Color.GREEN)
            print(f"[{self.get_timestamp()}] Döngü 1 aktif - Işık 1,2 yeşil")
        elif self.active_cycle == 2:
            self.carLights[3].setColor(Color.GREEN)
            self.carLights[4].setColor(Color.GREEN)
            print(f"[{self.get_timestamp()}] Döngü 2 aktif - Işık 3,4 yeşil")
        elif self.active_cycle == 3:
            self.carLights[5].setColor(Color.GREEN)
            self.carLights[6].setColor(Color.GREEN)
            print(f"[{self.get_timestamp()}] Döngü 3 aktif - Işık 5,6 yeşil")
        elif self.active_cycle == 4:
            self.carLights[7].setColor(Color.GREEN)
            self.carLights[8].setColor(Color.GREEN)
            print(f"[{self.get_timestamp()}] Döngü 4 aktif - Işık 7,8 yeşil")

    #random insan ve araba oluşturacağız
    def generate_Random(self):
        
        if self.current_time % 3 == 0:
            if random.randint(1,100) <= 40: # %40 ihtimalle araba oluştur
                light_id = random.randint(1,8)
                car = Car(self.next_car_id, Status.STOPPED, light_id)
                self.waitingCars[light_id].append(car)
                self.next_car_id += 1
                print(f"[{self.get_timestamp()}] Araba {car.id} ışık {light_id}'de bekliyor.")

        if self.current_time % 5 == 0:
            if random.randint(1,100) <= 30: # %30 ihtimalle yaya oluştur
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
                    car = self.waitingCars[light_id].popleft()
                    car.status = Status.MOVING
                    print(f"[{self.get_timestamp()}] Araba {car.id} ışık {light_id}'den geçti.")
                    car.status = Status.COMPLETED

    #sistemi çalıştıracağız
    # def run(self):
    #     print("Trafik sistemi çalışıyor...")
    #     while True:
    #         self.generate_Random()
    #         self.process_Traffic()
    #         self.current_time += 1
    #         self.cycle_counter += 1
    #         time.sleep(1)  # 1 saniye bekle (simülasyon için)

    #         if self.cycle_counter >= 10:  # Her 10 saniyede bir döngüyü değiştir
    #             self.active_cycle = (self.active_cycle % 4) + 1
    #             self.set_active_cycle()
    #             self.cycle_counter = 0

    #         if self.current_time % 10 == 0:
    #             print("Bekleyen arabalar:")
    #             for i in range(1, 9):
    #                 print(f"Işık {i}: {[car.id for car in self.waitingCars[i]]}")

    #             print("Bekleyen yayalar:")
    #             for i in range(1, 9):
    #                 print(f"Işık {i}: {[walker.id for walker in self.waitingWalkers[i]]}")

    #faz kontrolü
    def check_phase_change(self):

        self.cycle_counter += 1

        if self.cycle_counter >= 10:  # Her 10 saniyede bir döngüyü değiştir
            self.active_cycle += 1
            self.cycle_counter = 0

            if self.active_cycle > 4:
                self.active_cycle = 1

    def get_timestamp(self):
        return datetime.now().strftime("%H:%M:%S")
    


    def print_status(self):
        """Sistem durumunu yazdır"""
        print(f"\n=== Zaman: {self.current_time}s - Döngü: {self.active_cycle} ({self.cycle_counter}/{10}) ===")

        for i in range(1, 9):
            araba_durum = self.carLights[i].getColor()
            bekleyen_araba = len(self.waitingCars[i])
            bekleyen_yaya = len(self.waitingWalkers[i])

            print(f"Işık {i}: {araba_durum} - Bekleyen araba: {bekleyen_araba}, Bekleyen yaya: {bekleyen_yaya}")
        print()


    #run denememeee
    def run_simulation(self, duration=60):
        self.initialize()
        start_time = self.current_time

        print(f"Simülasyon başlatıldı - Süre: {duration} saniye")

        while self.running and (self.current_time - start_time) < duration:
            self.generate_Random()
            self.process_Traffic()
            self.check_phase_change()

            if self.current_time % 10 == 0:
                self.print_status()

            self.current_time += 1
            time.sleep(1)  # 1 saniye bekle 

        print("Simülasyon tamamlandı.")
        self.running = False

if __name__ == "__main__":
    traffic_system = TrafficSystem()
    traffic_system.run_simulation(120)  # 120 saniyelik simülasyon

