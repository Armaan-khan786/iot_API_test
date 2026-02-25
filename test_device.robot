*** Settings ***
Library    Process
Suite Setup    Log To Console    ===== STARTING ESP32 CI TEST =====
Suite Teardown    Log To Console    ===== TEST SUITE FINISHED =====

*** Variables ***
${PYTHON}    python

*** Test Cases ***

1. Compile Firmware
    ${r}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_compile()    shell=True
    Should Be Equal As Integers    ${r.rc}    0

2. Flash ESP32
    ${r}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_flash()    shell=True
    Should Be Equal As Integers    ${r.rc}    0

3. Device Boot Check
    ${r}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_device_check()    shell=True
    Should Be Equal As Integers    ${r.rc}    0

4. Cloud Check
    ${r}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_cloud_check()    shell=True
    Should Be Equal As Integers    ${r.rc}    0

5. Full Integration Run
    ${r}=    Run Process    ${PYTHON}    iot_cloud_test.py    shell=True
    Should Be Equal As Integers    ${r.rc}    0

6. Repeat Device Boot Check
    ${r}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_device_check()    shell=True
    Should Be Equal As Integers    ${r.rc}    0

7. Repeat Cloud Check
    ${r}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_cloud_check()    shell=True
    Should Be Equal As Integers    ${r.rc}    0

8. Full System Run Again
    ${r}=    Run Process    ${PYTHON}    iot_cloud_test.py    shell=True
    Should Be Equal As Integers    ${r.rc}    0

9. Device Stability Check
    ${r}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_device_check()    shell=True
    Should Be Equal As Integers    ${r.rc}    0

10. Final Cloud Validation
    ${r}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_cloud_check()    shell=True
    Should Be Equal As Integers    ${r.rc}    0
