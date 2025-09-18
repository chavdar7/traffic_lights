# Trafik Işığı Projesi Dokümantasyonu

## İçindekiler





1. [Proje Hakkında](#proje-hakkında)
2. [Kurulum](#kurulum)
3. [Kullanım](#kullanım)
4. [Katkıda Bulunma](#katkıda-bulunma)
5. [Lisans](#lisans)


## Proje Hakkında
Bu projede, 2 şeritli ve ışıklarda 4 şerite çıkan 2 anayol ve 2 şeritli 2 tali yolun olduğu bir trafik ışığı sistemi simüle edilmiştir. Toplamda 8 adet araba ışığı ve 8 adet yaya ışığı bulunmaktadır. Sistemimizde kullanıcı kendi isteği üzerine trafik yoğunluğu ayarlanabilmekte ve sistemi başlatmaktadır. Işıklar da birbiriyle optimize şekilde çalışarak trafiği yönetmeye çalışmaktadır.

## Dosya Yapısı

```
traffic_lights/
├── templates/
│   └── index.html          
├── static/
│   ├── images/
│   │   └── traffic.png
│   ├── styles.css       
│   └── script.js        
├── app.py              
└── traffic_logic.py   
```

- **/index.html**
  Kullanıcı arayüzünü içerir.
- **/style.css**
  index.html sayfasının css stilleri içerir.
- **/script.js**
  Frontend ve backend arası bağlantı kurar. Sayfadaki bazı dinamik elementleri oluşturur. API iletişimlerini sağlar.
- **/app.py**
  Main program sayfası. Flask backend içerir, pageleri tutar ve program burdan çalıştırılır.
- **/traffic_logic.py**
  Arka planda çalışan trafik algoritmasını içerir.

---

## Kullanıcı Arayüzü
### Kullanıcı Arayüzü Bileşenleri
- **Trafik Işıklarının ve Yolların Yerini Gösteren Plan**
- **Trafik Yoğunluğu Ayarı**
- **Araba ve Yaya Işıklarının Durumunu Gösteren Panel**
- **Bekleyen Araba ve Yaya Listesi**
- **Döngü Bilgileri ve İstatistikler**

### 1- Işık ve Yol Planı
Sayfanın sol üst tarafında yoğunluk ayar panelinin solunda trafik ışıklarının ve yolların yerini gösteren bir plan bulunmaktadır.

### 2- Trafik Yoğunluğu Ayar Paneli
Sayfanın sağ üst tarafında yol planının sağında kullanıcının isteğine göre kaç saniyede kaç araba ve yaya oluşmasını ayarlayabileceği bir panel bulunmaktadır. Burada girilen sayılar yollara ve ışıklara rastgele olarak dağılmaktadır. Kullanıcı istediği zaman bu ayarları değiştirebilir.

### 3- Araba ve Yaya Işıklarının Durumunu Gösteren Panel
Üstteki iki panelin hemen altında araba ve yaya ışıkları için 2 panel bulunmaktadır. Her panelin içinde 8 adet ışık ve her birinin altında o ışıkta anlık olarak bekleyen sayısı bulunmaktadır. Işıkların renkleri kırmızı ve yeşil olarak zaman içinde değişmektedir ve yeşil ışıkta bulunan araba ve yayalar sırayla harekete geçerek bekleyen sayısını azaltırlar. Araba ve yaya ışıkları optimize olarak birbirleriyle uyumlu çalışmaktadır.
Tabloda optimize olarak yeşil yana ışıklar verilmiştir.

  |döngü|trafik ışığı | yaya ışığı |
  |:-----------:|:-----------:|:---------:|
  |1   |1,2         |1,3      |
  |2   |3,4         |6,8      |
  |3   |5,6         |5,7      |
  |4   |7,8         |2,4      |

### 4- Bekleyen Araba ve Yaya Listesi
Işık durumlarını gösteren panellerin hemen altında her ışıkta bekleyen araba ve yayaların id listesini gösteren alt alta iki panel bulunmaktadır. Bu liste de ışıkların renklerine göre değişmektedir. Yeşil ışıkta olanlar sırayla listeden çıkmaktadır.

### 5- Aktif Döngü Bilgileri
Bulunduğu saniye sistemin hangi döngüde olduğunu, hangi saniyede olduğunu gösteren panel

### 6- Anlık İstatistikler
Sistemde anlık olarak kaç araba ve kaç yaya beklediğini, arka planla bağlantı durumunu ve yeşil ışık sayısını gösteren panel


## API Çağrıları ve Sayfalar

### Durum Bildirim
her saniye sistemin durumunu json olarak döndürür. Gerektiğinde veriler buradan çekilir
```
GET /api/status
```
**Yanıt**
``` json
{
  "active_cycle": 1,
  "current_time": 0,
  "cycle_progress": "0/10",
  "lights": {
    "light_1": {
      "car_light": "red",
      "pedestrian_light": "red"
    },
    "light_2": {
      "car_light": "red",
      "pedestrian_light": "red"
    },
    "light_3": {
      "car_light": "red",
      "pedestrian_light": "red"
    },
    "light_4": {
      "car_light": "red",
      "pedestrian_light": "red"
    },
    "light_5": {
      "car_light": "red",
      "pedestrian_light": "red"
    },
    "light_6": {
      "car_light": "red",
      "pedestrian_light": "red"
    },
    "light_7": {
      "car_light": "red",
      "pedestrian_light": "red"
    },
    "light_8": {
      "car_light": "red",
      "pedestrian_light": "red"
    }
  },
  "queues": {
    "queue_1": {
      "waiting_cars": 0,
      "waiting_cars_ids": [],
      "waiting_pedestrians": 0,
      "waiting_pedestrians_ids": []
    },
    "queue_2": {
      "waiting_cars": 0,
      "waiting_cars_ids": [],
      "waiting_pedestrians": 0,
      "waiting_pedestrians_ids": []
    },
    "queue_3": {
      "waiting_cars": 0,
      "waiting_cars_ids": [],
      "waiting_pedestrians": 0,
      "waiting_pedestrians_ids": []
    },
    "queue_4": {
      "waiting_cars": 0,
      "waiting_cars_ids": [],
      "waiting_pedestrians": 0,
      "waiting_pedestrians_ids": []
    },
    "queue_5": {
      "waiting_cars": 0,
      "waiting_cars_ids": [],
      "waiting_pedestrians": 0,
      "waiting_pedestrians_ids": []
    },
    "queue_6": {
      "waiting_cars": 0,
      "waiting_cars_ids": [],
      "waiting_pedestrians": 0,
      "waiting_pedestrians_ids": []
    },
    "queue_7": {
      "waiting_cars": 0,
      "waiting_cars_ids": [],
      "waiting_pedestrians": 0,
      "waiting_pedestrians_ids": []
    },
    "queue_8": {
      "waiting_cars": 0,
      "waiting_cars_ids": [],
      "waiting_pedestrians": 0,
      "waiting_pedestrians_ids": []
    }
  }
}
```

### İşleyiş Çağrıları
Sisteme başlama, bitirme ve resetleme api sayfaları
```
POST /api/start
POST /api/stop
POST /api/reset
```

## Bazı Önemli Fonksiyonlar


### Javascript Fonksiyonları

#### `createLightLists()`
- Araba ve yaya ışıklarını oluşturup hepsini kırmızı renge ayarlar
- Araba ve yaya ışıklarında bekleyenlerin listesini boş olarak oluşturur.

#### `updateDisplay(data)`
- Arayüzü her saniye günceller, her panelin güncel görüntüsünü hangi durumda olduğuna göre yeniler.


### Python Fonksiyonları

#### `initialize()`
- Sistemi başlatır ve `set_active_cycle()` çağırır

#### `set_active_cycle()`
- Döngü sayısına göre kırmızı ve yeşil ışıkları ayarlar

#### `generate_Random()`
- Kullanıcının girdiği verilere göre araba ve yaya oluşturur. Bunları rastgele olarak ışıklara atar.

#### `process_Traffic()`
- Yeşil ışıkta bekleyen araba ve yayaları sırayla harekete geçirir.

#### `check_phase_change()`
- Faz döngüsünü kontrol eder ve her 4 döngüde bir başa döner



## Kurulum ve Çalıştırma

1. **Gereksinimler**

- Python 3.x
- Flask framework
- Modern web tarayıcı
  
1. **Flask uygulamasını çalıştır**:
   ```bash
   python /dosya_yolu/app.py
   ```

2. **Tarayıcıda aç**:
   ```
   http://localhost:5000
   ```

