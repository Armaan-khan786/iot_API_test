import subprocess
import serial
import time
import requests
import sys
import os
import json

# ==============================
# CONFIG
# ==============================
ARDUINO_CLI = ".\\arduino-cli.exe"
COM_PORT = "COM6"
BOARD = "esp32:esp32:esp32"
SKETCH_PATH = "temp"
BLYNK_TOKEN = os.getenv("AV6Yyn81W7kNA723S4Y0asvrV2eUu6nC")
VIRTUAL_PIN = "V0"

# ==============================
# HELPERS
# ==============================
def run_command(cmd):
    print("\n>>>", cmd)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(1)

def open_serial_with_retry(port, baud=115200, retries=5):
    for _ in range(retries):
        try:
            return serial.Serial(port, baud, timeout=1)
        except:
            time.sleep(2)
    sys.exit(1)

# ==============================
# CORE FUNCTIONS
# ==============================
def compile_firmware():
    run_command(f'"{ARDUINO_CLI}" compile --fqbn {BOARD} {SKETCH_PATH}')

def flash_firmware():
    run_command(f'"{ARDUINO_CLI}" upload -p {COM_PORT} --fqbn {BOARD} {SKETCH_PATH}')

def verify_device_boot():
    ser = open_serial_with_retry(COM_PORT)
    time.sleep(5)

    wifi_ok = False
    blynk_ok = False
    temperature = None

    start_time = time.time()

    while time.time() - start_time < 60:
        line = ser.readline().decode(errors="ignore").strip()

        if line:
            print("DEVICE:", line)

            if line.startswith("ERROR:"):
                ser.close()
                sys.exit(1)

            if "WIFI_CONNECTED" in line:
                wifi_ok = True

            if "BLYNK_CONNECTED" in line:
                blynk_ok = True

            if line.startswith("{") and "TEMP" in line:
                try:
                    data = json.loads(line)
                    temperature = float(data["TEMP"])
                except:
                    pass

        if wifi_ok and blynk_ok and temperature is not None:
            ser.close()
            return temperature

    ser.close()
    sys.exit(1)

def verify_cloud_value(device_temp):
    for _ in range(5):
        try:
            url = f"https://blynk.cloud/external/api/get?token={BLYNK_TOKEN}&{VIRTUAL_PIN}"
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                sys.exit(1)

            value = float(response.text)

            if abs(device_temp - value) <= 2:
                return value
            else:
                sys.exit(1)

        except:
            time.sleep(2)

    sys.exit(1)

# ==============================
# ROBOT FUNCTIONS
# ==============================
def main_compile():
    compile_firmware()

def main_flash():
    flash_firmware()

def main_device_check():
    verify_device_boot()

def main_cloud_check():
    device_temp = verify_device_boot()
    verify_cloud_value(device_temp)

# ==============================
# FULL PIPELINE
# ==============================
def main():
    compile_firmware()
    flash_firmware()
    device_temp = verify_device_boot()
    verify_cloud_value(device_temp)
    print("🎉 PASS: SYSTEM HEALTHY")

if __name__ == "__main__":
    main()
