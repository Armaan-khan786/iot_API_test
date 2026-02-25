*** Settings ***
Library    Process
Suite Setup    Log To Console    ===== STARTING ESP32 CI TEST =====
Suite Teardown    Log To Console    ===== TEST SUITE FINISHED =====

*** Variables ***
${PYTHON}    python

*** Test Cases ***

Compile Firmware
    ${result}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_compile()    shell=True
    Should Be Equal As Integers    ${result.rc}    0

Flash ESP32
    ${result}=    Run Process    ${PYTHON}    -c    import iot_cloud_test; iot_cloud_test.main_flash()    shell=True
    Should Be Equal As Integers    ${result.rc}    0

Full Hardware + Cloud Integration Test
    ${result}=    Run Process    ${PYTHON}    iot_cloud_test.py    shell=True
    Should Be Equal As Integers    ${result.rc}    0
