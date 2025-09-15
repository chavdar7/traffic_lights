// Socket.IO bağlantısı
        const socket = io();

        // Işık listelerini oluştur
        function createLightLists() {
            const carLights = document.getElementById('car-lights');
            const pedestrianLights = document.getElementById('pedestrian-lights');

            // Trafik ışıkları (1-8)
            for (let i = 1; i <= 8; i++) {
                const lightItem = document.createElement('div');
                lightItem.className = 'light-item';
                lightItem.innerHTML = `
                    <div class="light-number">Işık ${i}</div>
                    <div class="light-status red" id="car-status-${i}">
                        <i class="fas fa-circle"></i>
                        KIRMIZI
                    </div>
                    <div class="queue-info">
                        Bekleyen: <span class="queue-count" id="car-queue-${i}">0</span>
                    </div>
                `;
                carLights.appendChild(lightItem);
            }

            // Yaya ışıkları (1-8)
            for (let i = 1; i <= 8; i++) {
                const lightItem = document.createElement('div');
                lightItem.className = 'light-item';
                lightItem.innerHTML = `
                    <div class="light-number">Yaya ${i}</div>
                    <div class="light-status red" id="pedestrian-status-${i}">
                        <i class="fas fa-circle"></i>
                        KIRMIZI
                    </div>
                    <div class="queue-info">
                        Bekleyen: <span class="queue-count" id="pedestrian-queue-${i}">0</span>
                    </div>
                `;
                pedestrianLights.appendChild(lightItem);
            }

            // Bekleyen araçlar ve yayalar listesi
            for (let i = 1; i <= 8; i++) {
                const carListItem = document.createElement('li');
                carListItem.id = `waiting-cars-list-${i}`;
                document.getElementById('waiting-cars-list').appendChild(carListItem);

                const pedestrianListItem = document.createElement('li');
                pedestrianListItem.id = `waiting-pedestrians-list-${i}`;
                document.getElementById('waiting-pedestrians-list').appendChild(pedestrianListItem);
            }
        }


        // Görüntüyü güncelle
        function updateDisplay(data) {
            // Döngü bilgileri
            document.getElementById('active-cycle').textContent = data.active_cycle;
            document.getElementById('cycle-progress').textContent = data.cycle_progress;
            document.getElementById('system-time').textContent = data.current_time + 's';

            // Progress bar
            const [current, total] = data.cycle_progress.split('/').map(Number);
            const percentage = (current / total) * 100;
            document.getElementById('progress-fill').style.width = percentage + '%';

            // İstatistikler
            let totalCars = 0;
            let totalPedestrians = 0;
            let greenLights = 0;

            // Işık durumlarını güncelle
            for (let i = 1; i <= 8; i++) {
                const carStatus = document.getElementById(`car-status-${i}`);
                const pedestrianStatus = document.getElementById(`pedestrian-status-${i}`);
                
                // Trafik ışığı durumu
                if (data.lights[`light_${i}`].car_light === 'green') {
                    carStatus.className = 'light-status green';
                    carStatus.innerHTML = '<i class="fas fa-circle"></i> YEŞİL';
                    greenLights++;
                } else {
                    carStatus.className = 'light-status red';
                    carStatus.innerHTML = '<i class="fas fa-circle"></i> KIRMIZI';
                }

                // Yaya ışığı durumu
                if (data.lights[`light_${i}`].pedestrian_light === 'green') {
                    pedestrianStatus.className = 'light-status green';
                    pedestrianStatus.innerHTML = '<i class="fas fa-circle"></i> YEŞİL';
                } else {
                    pedestrianStatus.className = 'light-status red';
                    pedestrianStatus.innerHTML = '<i class="fas fa-circle"></i> KIRMIZI';
                }

                // Kuyruk sayıları
                const carQueue = data.queues[`queue_${i}`].waiting_cars;
                const pedestrianQueue = data.queues[`queue_${i}`].waiting_pedestrians;
                
                document.getElementById(`car-queue-${i}`).textContent = carQueue;
                document.getElementById(`pedestrian-queue-${i}`).textContent = pedestrianQueue;

                // Bekleyen araba ve yaya ID'lerini göster
                const carWaitingList = data.queues[`queue_${i}`].waiting_cars_ids;
                const walkerWaitingList = data.queues[`queue_${i}`].waiting_pedestrians_ids;
                document.getElementById(`waiting-cars-list-${i}`).textContent = `Işık ${i}: ${carWaitingList}`;
                document.getElementById(`waiting-pedestrians-list-${i}`).textContent = `Işık ${i}: ${walkerWaitingList}`;

                
                totalCars += carQueue;
                totalPedestrians += pedestrianQueue;
            }

            // Genel istatistikler
            document.getElementById('total-cars').textContent = totalCars;
            document.getElementById('total-pedestrians').textContent = totalPedestrians;
            document.getElementById('green-lights').textContent = greenLights;
        }

        // Socket olayları
        socket.on('connect', function() {
            console.log('Sunucuya bağlandı');
            document.getElementById('connection-status').innerHTML = '<i class="fas fa-check-circle" style="color: #27ae60;"></i>';
        });

        socket.on('disconnect', function() {
            console.log('Bağlantı kesildi');
            document.getElementById('connection-status').innerHTML = '<i class="fas fa-times-circle" style="color: #e74c3c;"></i>';
        });

        socket.on('status', function(data) {
            updateDisplay(data);
        });


        // Sayfa yüklendiğinde
        document.addEventListener('DOMContentLoaded', function() {
            createLightLists();

            // Başlat formu
            const startForm = document.getElementById('start-form');
            startForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const carInterval = document.getElementById('car-interval').value;
                const carCount = document.getElementById('car-count').value;
                const walkerInterval = document.getElementById('walker-interval').value;
                const walkerCount = document.getElementById('walker-count').value;
                fetch('/api/start', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        car_interval: Number(carInterval),
                        car_count: Number(carCount),
                        walker_interval: Number(walkerInterval),
                        walker_count: Number(walkerCount)
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Sistem başlatıldı:', data);
                })
                .catch(error => {
                    console.log('Sistem başlatılamadı:', error);
                });
            });

            // İlk durum güncellemesi
            fetch('/api/status')
                .then(response => response.json())
                .then(updateDisplay)
                .catch(error => {
                    console.log('API bağlantısı kurulamadı:', error);
                });
        });

        // Her 5 saniyede bir durum kontrolü (WebSocket bağlantısı koptuğunda)
        setInterval(function() {
            if (!socket.connected) {
                fetch('/api/status')
                    .then(response => response.json())
                    .then(updateDisplay)
                    .catch(error => {
                        console.log('Bağlantı hatası:', error);
                    });
            }
        }, 5000);