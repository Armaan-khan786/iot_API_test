*** Settings ***
Library    Process

*** Test Cases ***
Compile Firmware
    Log To Console    ===== COMPILING ESP32 FIRMWARE =====
    ${result}=    Run Process    python    -c    import iot_cloud_test; iot_cloud_test.main_compile()    shell=True
    Should Be Equal As Integers    ${result.rc}    0

Flash ESP32
    Log To Console    ===== FLASHING DEVICE =====
    ${result}=    Run Process    python    -c    import iot_cloud_test; iot_cloud_test.main_flash()    shell=True
    Should Be Equal As Integers    ${result.rc}    0

Verify Device Boot
    Log To Console    ===== VERIFYING WIFI + DEVICE =====
    ${result}=    Run Process    python    -c    import iot_cloud_test; iot_cloud_test.main_device_check()    shell=True
    Should Be Equal As Integers    ${result.rc}    0

Validate Cloud Temperature
    Log To Console    ===== VALIDATING CLOUD DATA =====
    ${result}=    Run Process    python    -c    import iot_cloud_test; iot_cloud_test.main_cloud_check()    shell=True
    Should Be Equal As Integers    ${result.rc}    0
