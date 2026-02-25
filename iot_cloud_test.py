import subprocess
import serial
import time
import requests
import os
import sys

COM_PORT = "COM6"
BAUD_RATE = 115200
FQBN = "esp32:esp32:esp32"
SKETCH_FOLDER = "temp"


# --------------------------------------------------
# Compile Firmware
# --------------------------------------------------
def compile_firmware():
    print('\n>>> Compiling firmware...')
    cmd = f'.\\arduino-cli.exe compile --fqbn {FQBN} {SKETCH_FOLDER}'
    result = subprocess.run(cmd, shell=True)
    return result.returncode


# --------------------------------------------------
# Upload Firmware
# --------------------------------------------------
def upload_firmware():
    print('\n>>> Uploading firmware...')
    cmd = f'.\\arduino-cli.exe upload -p {COM_PORT} --fqbn {FQBN} {SKETCH_FOLDER}'
    result = subprocess.run(cmd, shell=True)
    return result.returncode


# --------------------------------------------------
# Verify Device Boot
# --------------------------------------------------
def verify_device_boot():
    print("\n>>> Checking device boot logs...")

    time.sleep(10)  # Wait for ESP32 reboot

    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        print("Serial open error:", e)
        return 1

    logs = ""
    start = time.time()

    while time.time() - start < 20:
        if ser.in_waiting:
            line = ser.readline().decode(errors="ignore").strip()
            print("DEVICE:", line)
            logs += line

    ser.close()

    if "WIFI_CONNECTED" in logs and "BLYNK_CONNECTED" in logs:
        print("Device boot verified ✅")
        return 0

    print("Device boot failed ❌")
    return 1


# --------------------------------------------------
# Verify Cloud API
# --------------------------------------------------
def verify_cloud():
    print("\n>>> Checking Blynk cloud API...")

    BLYNK_TOKEN = os.getenv("here I added that token")

    if not BLYNK_TOKEN:
        print("Missing BLYNK_TOKEN environment variable")
        return 1

    try:
        url = f"https://blynk.cloud/external/api/isHardwareConnected?token={BLYNK_TOKEN}"
        r = requests.get(url, timeout=10)

        print("Cloud response:", r.text)

        if r.status_code == 200 and r.text.strip() == "true":
            print("Cloud connection verified ✅")
            return 0

    except Exception as e:
        print("Cloud check error:", e)

    print("Cloud verification failed ❌")
    return 1


# --------------------------------------------------
# Verify Temperature Data From Serial
# --------------------------------------------------
def verify_temperature():
    print("\n>>> Checking temperature JSON output...")

    time.sleep(5)

    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        print("Serial open error:", e)
        return 1

    start = time.time()

    while time.time() - start < 15:
        if ser.in_waiting:
            line = ser.readline().decode(errors="ignore").strip()
            print("DEVICE:", line)

            if '"TEMP"' in line:
                print("Temperature data received ✅")
                ser.close()
                return 0

    ser.close()
    print("Temperature data not received ❌")
    return 1


# --------------------------------------------------
# Main Execution
# --------------------------------------------------
if __name__ == "__main__":

    if compile_firmware() != 0:
        sys.exit(1)

    if upload_firmware() != 0:
        sys.exit(1)

    if verify_device_boot() != 0:
        sys.exit(1)

    if verify_temperature() != 0:
        sys.exit(1)

    if verify_cloud() != 0:
        sys.exit(1)

    print("\n🎉 ALL CHECKS PASSED")
    sys.exit(0)
