*** Settings ***
Library           Process
Library           RequestsLibrary
Library           OperatingSystem
Library           Collections

*** Variables ***
${COM_PORT}       COM6
${BAUD}           115200
${TOKEN}          AV6Yyn81W7kNA723S4Y0asvrV2eUu6nC
${BASE_URL}       https://blynk.cloud/external/api

*** Test Cases ***

Compile Firmware
    Log    ===== COMPILING ESP32 FIRMWARE =====
    ${result}=    Run Process    arduino-cli    compile --fqbn esp32:esp32:esp32 .
    Should Be Equal As Integers    ${result.rc}    0

Flash ESP32
    Log    ===== FLASHING DEVICE =====
    ${result}=    Run Process    arduino-cli    upload -p ${COM_PORT} --fqbn esp32:esp32:esp32 .
    Should Be Equal As Integers    ${result.rc}    0

Verify Device Boot
    Log    ===== VERIFYING WIFI + RSSI + DEVICE =====
    Sleep    10s
    ${result}=    Run Process    python    check_serial.py
    Should Be Equal As Integers    ${result.rc}    0

Validate Cloud Temperature
    Log    ===== VALIDATING CLOUD TEMPERATURE =====
    ${response}=    GET    ${BASE_URL}/get?token=${TOKEN}&v0
    Should Be Equal As Integers    ${response.status_code}    200
    ${temp}=    Convert To Number    ${response.text}
    Log    Temperature: ${temp}
    Should Be True    ${temp} > 0
    Should Be True    ${temp} < 100

Validate Cloud WiFi Strength
    Log    ===== VALIDATING CLOUD WIFI RSSI =====
    ${response}=    GET    ${BASE_URL}/get?token=${TOKEN}&v1
    Should Be Equal As Integers    ${response.status_code}    200
    ${rssi}=    Convert To Number    ${response.text}
    Log    RSSI: ${rssi}
    Should Be True    -120 < ${rssi} < 0
