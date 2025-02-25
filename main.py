from machine import Pin
import dht
import network
import utime as time
import urequests as requests
import ujson

# Konfigurasi WiFi
WIFI_SSID = "Kanteen.mekar"
WIFI_PASSWORD = "Ngopidulu"

# Konfigurasi Ubidots
UBIDOTS_DEVICE_ID = "esp32-sic-6-hardware"
UBIDOTS_TOKEN = "BBUS-bXBKTrmmHCmTb3BK6ipYLMboqZyYw9"
UBIDOTS_URL = "http://things.ubidots.com/api/v1.6/devices/" + UBIDOTS_DEVICE_ID

# Konfigurasi Flask Server
FLASK_SERVER_URL = "http://192.168.1.41:5001/sensor"  # Ganti dengan IP Flask Server
HEADERS = {
    "Content-Type": "application/json"
}

# Pin Sensor & Aktuator
DHT_PIN = Pin(5)
PIR_PIN = Pin(23, Pin.IN)   # HC-SR501 di GPIO 23 (input)
LED_PIN = Pin(22, Pin.OUT)  # LED di GPIO 22 (output)

# Fungsi untuk koneksi WiFi
def connect_wifi():
    wifi_client = network.WLAN(network.STA_IF)
    wifi_client.active(True)
    print("Connecting device to WiFi")
    wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

    while not wifi_client.isconnected():
        print("Connecting...")
        time.sleep(0.5)
    
    print("WiFi Connected!")
    print("IP Address:", wifi_client.ifconfig()[0])

# Fungsi untuk mengirim data ke Ubidots
def send_to_ubidots(temperature, humidity, motion, led):
    headers = {"Content-Type": "application/json", "X-Auth-Token": UBIDOTS_TOKEN}
    data = {"temp": temperature, "humidity": humidity, "motion": motion, "led": led}

    try:
        response = requests.post(UBIDOTS_URL, json=data, headers=headers, timeout=5)
        print("Response Ubidots:", response.text)
    except Exception as e:
        print("Failed to send to Ubidots:", e)

# Fungsi untuk mengirim data ke Flask
def send_to_flask(temperature, humidity, motion, led):
    payload = ujson.dumps({
        "temperature": temperature,
        "humidity": humidity,
        "motion": motion,
        "led": led
    })
    print(f"Mengirim data ke server: {payload}")

    response = requests.post(FLASK_SERVER_URL, headers=HEADERS, data=payload)
    status.code = response.status_code
    response.close()
        

# Hubungkan ke WiFi
connect_wifi()

# Inisialisasi sensor
dht_sensor = dht.DHT11(DHT_PIN)

while True:
    try:
        # Baca suhu & kelembapan dari DHT11
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # Baca status gerakan dari HC-SR501
        motion = PIR_PIN.value()  # 1 = ada gerakan, 0 = tidak ada gerakan

        # Kontrol LED berdasarkan motion
        led = "menyala" if motion else "mati"
        LED_PIN.value(1 if motion else 0)

        # Cetak hasil pembacaan
        print("Temperature:", temperature, "°C, Humidity:", humidity, "%, Motion:", motion, "LED:", led)

        # Kirim data ke Ubidots
        send_to_ubidots(temperature, humidity, motion, led)

        # Kirim data ke Flask untuk disimpan ke MongoDB
        send_to_flask(temperature, humidity, motion, led)

    except Exception as e:
        print("Error reading sensors:", e)

    time.sleep(5)  # Delay 5 detik sebelum pembacaan berikutnya
