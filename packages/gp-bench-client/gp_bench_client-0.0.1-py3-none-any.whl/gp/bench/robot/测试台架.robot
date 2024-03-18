*** Settings ***

Documentation     This is a test suite for testing the login functionality of the application
Library           gp.bench.robot.BenchLibrary    WITH NAME    Bench

*** Keywords ***

设置目标台架
    [Arguments]    ${IP}    ${PORT}
    ${ret}    Bench.Setup Target    ${IP}    ${PORT}
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

初始化IO模组
    [Arguments]    ${COM}    ${BAUDRATE}    ${TIMEOUT}    ${CHANNEL}=32    ${ADDRESS}=1    ${DEVICE_NAME}=DAM
    ${ret}    Bench.Setup    ${COM}    ${BAUDRATE}    ${TIMEOUT}    ${CHANNEL}    ${ADDRESS}    ${DEVICE_NAME}
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

指定从机地址
    [Arguments]    ${从机地址}
    ${ret}    Bench.setup_address    ${从机地址}
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

打开IO模组通道
    [Arguments]    ${通道ID}
    ${ret}    Bench.Open    ${通道ID}
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

关闭IO模组通道
    [Arguments]    ${通道ID}
    ${ret}    Bench.Close    ${通道ID}
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

打开所有通道
    ${ret}    Bench.Open All
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

关闭所有通道
    ${ret}    Bench.Close All
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

获取IO模组输出状态
    ${ret}    Bench.Read All Do
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

读取保持寄存器
    [Arguments]    ${寄存器地址}    ${寄存器长度}=1
    ${ret}    Bench.Read    ${寄存器地址}    ${寄存器长度}
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

写入保持寄存器
    [Arguments]    ${寄存器地址}    ${寄存器值}
    ${ret}    Bench.Write    ${寄存器地址}    ${寄存器值}
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

读取输入寄存器
    [Arguments]    ${寄存器地址}    ${寄存器长度}=1
    ${ret}    Bench.Read Input    ${寄存器地址}    ${寄存器长度}
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}

发送MODBUS请求
    [Arguments]    ${MODBUS请求}
    ${ret}    Bench.request    ${MODBUS请求}
    Should Be Equal    ${ret["status"]}    ok
    [Return]    ${ret}