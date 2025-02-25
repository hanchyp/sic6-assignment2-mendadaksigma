# 🤖IoT Projects - SIC6 - Stage 2🤖

## Task✏️‼️
Buatlah sebuah dashboard di platform ubidots dengan minimal 2 visualisasi (bisa berupa chart/grafik dll) dan script micropython untuk mengirimkan data sensor (boleh menggunakan sensor apa saja)
  - Dapatkan data sensor ultrasonic/menggunakan sensor yang ada/yang kalian pakai untuk project kalian
  - Kirimkan data tersebut ke ubidots dashboard melalui REST API/MQTT
  - Tampilkan data sensor dalam sebuah dashboard (minimal 2 buah visualisasi, contohnya grafik & gauge)!

## IoT Feature🗿
- Humidity Sensor
- Temperature Sensor
- Motion Sensor with LED sign
- Integrated with Ubidots & MongoDB

### NOTES!
app.py → Flask Backend for MongoDB connection\

main.py → MicroPython for Ubidots and IoT connection\

### ‼️HOW TO RUN‼️
1. Change the WIFI_ID and WIFI_PASSWORD (main.py)
2. Change FLASK_SERVER_URL (main.py) with your IP Address
3. Run the Flask (app.py) first
4. Then run the MicroPython (main.py)
