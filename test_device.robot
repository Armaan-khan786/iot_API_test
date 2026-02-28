*** Settings ***
Library    RequestsLibrary

*** Variables ***
${TOKEN}    AV6Yyn81W7kNA723S4Y0asvrV2eUu6nC
${BASE}     https://blynk.cloud/external/api

*** Test Cases ***
Validate Cloud Temperature
    ${response}=    GET    ${BASE}/get?token=${TOKEN}&v0
    ${temp}=    Convert To Number    ${response.text}
    Log    Temperature: ${temp}
    Should Be True    ${temp} > 0
    Should Be True    ${temp} < 100

Validate Cloud WiFi Strength
    ${response}=    GET    ${BASE}/get?token=${TOKEN}&v1
    ${rssi}=    Convert To Number    ${response.text}
    Log    RSSI: ${rssi}
    Should Be True    -120 < ${rssi} < 0
