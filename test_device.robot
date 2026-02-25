*** Settings ***
Library    Process
Suite Setup    Log To Console    ===== STARTING ESP32 CI TEST =====
Suite Teardown    Log To Console    ===== TEST SUITE FINISHED =====

*** Variables ***
${PYTHON}    python

*** Test Cases ***

1. Compile Firmware
    ${result}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_compile()    shell=True
    Should Be Equal As Integers    ${result.rc}    0

2. Flash ESP32
    ${result}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_flash()    shell=True
    Should Be Equal As Integers    ${result.rc}    0

3. Verify Device Boot
    ${result}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_device_check()    shell=True
    Should Be Equal As Integers    ${result.rc}    0

4. Verify Cloud API Reachable
    ${result}=    Run Process    ${PYTHON}    -c    import requests; import os; print(requests.get(f'https://blynk.cloud/external/api/get?token={os.getenv(\"BLYNK_TOKEN\")}&V0').status_code)"    shell=True
    Should Be Equal As Integers    ${result.rc}    0

5. Full Hardware Integration
    ${result}=    Run Process    ${PYTHON}    iot_cloud_test.py    shell=True
    Should Be Equal As Integers    ${result.rc}    0

6. Re-run Device Validation
    ${result}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_device_check()    shell=True
    Should Be Equal As Integers    ${result.rc}    0

7. Re-run Cloud Validation
    ${result}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_cloud_check()    shell=True
    Should Be Equal As Integers    ${result.rc}    0

8. Serial Communication Stability
    ${result}=    Run Process    ${PYTHON}    -c    import serial; s=serial.Serial('COM6',115200,timeout=1); s.close()"    shell=True
    Should Be Equal As Integers    ${result.rc}    0

9. API Response Timing Check
    ${result}=    Run Process    ${PYTHON}    -c    import requests, time, os; t=time.time(); requests.get(f'https://blynk.cloud/external/api/get?token={os.getenv(\"BLYNK_TOKEN\")}&V0'); print(time.time()-t)"    shell=True
    Should Be Equal As Integers    ${result.rc}    0

10. Final System Health Check
    ${result}=    Run Process    ${PYTHON}    iot_cloud_test.py    shell=True
    Should Be Equal As Integers    ${result.rc}    0
