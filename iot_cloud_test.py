import subprocess
import serial
import time
import requests
import sys

# ==============================
# USER CONFIG
# ==============================
ARDUINO_CLI = ".\\arduino-cli.exe"
COM_PORT = "COM6"
BOARD = "esp32:esp32:esp32"
SKETCH_PATH = "temp"
BLYNK_TOKEN = "AV6Yyn81W7kNA723S4Y0asvrV2eUu6nC"
VIRTUAL_PIN = "V0"

# ==============================
# COMMON HELPERS
# ==============================
def run_command(cmd):
    print("\n>>>", cmd)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("❌ Command failed")
        sys.exit(1)

def open_serial_with_retry(port, baud=115200, retries=5):
    for _ in range(retries):
        try:
            return serial.Serial(port, baud, timeout=1)
        except:
            time.sleep(2)
    print("❌ Cannot open serial port")
    sys.exit(1)

# ==============================
# CORE OPERATIONS
# ==============================
def compile_firmware():
    print("\n=== COMPILING FIRMWARE ===")
    run_command(f'"{ARDUINO_CLI}" compile --fqbn {BOARD} {SKETCH_PATH}')

def flash_firmware():
    print("\n=== FLASHING ESP32 ===")
    run_command(f'"{ARDUINO_CLI}" upload -p {COM_PORT} --fqbn {BOARD} {SKETCH_PATH}')

def verify_device_boot():
    print("\n=== WAITING FOR DEVICE BOOT ===")

    ser = open_serial_with_retry(COM_PORT)
    time.sleep(5)

    wifi_ok = False
    blynk_ok = False
    temperature = None

    start_time = time.time()

    while time.time() - start_time < 40:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            print("DEVICE:", line)

            if "WIFI_CONNECTED" in line:
                wifi_ok = True

            if "BLYNK_CONNECTED" in line:
                blynk_ok = True

            if line.startswith("TEMP:"):
                try:
                    temperature = float(line.split(":")[1])
                except:
                    pass

        if wifi_ok and blynk_ok and temperature is not None:
            ser.close()
            print("Device Temperature:", temperature)
            return temperature

    ser.close()

    if not wifi_ok:
        print("❌ FAIL: WiFi not connected")
    if not blynk_ok:
        print("❌ FAIL: Blynk not connected")

    sys.exit(1)

def verify_cloud_value():
    print("\n=== CHECKING CLOUD VALUE ===")

    for _ in range(5):
        try:
            url = f"https://blynk.cloud/external/api/get?token={BLYNK_TOKEN}&{VIRTUAL_PIN}"
            value = float(requests.get(url, timeout=5).text)
            print("Cloud Temperature:", value)

            if 10 <= value <= 50:
                return value
            else:
                print("❌ FAIL: Temperature out of range")
                sys.exit(1)

        except:
            time.sleep(2)

    print("❌ FAIL: Cannot read cloud value")
    sys.exit(1)

# ==============================
# FUNCTIONS FOR ROBOT FRAMEWORK
# ==============================
def main_compile():
    compile_firmware()

def main_flash():
    flash_firmware()

def main_device_check():
    verify_device_boot()

def main_cloud_check():
    verify_cloud_value()

# ==============================
# FULL PIPELINE (manual run)
# ==============================
def main():
    compile_firmware()
    flash_firmware()
    verify_device_boot()
    verify_cloud_value()
    print("\n🎉 PASS: SYSTEM HEALTHY")

if __name__ == "__main__":
    main()