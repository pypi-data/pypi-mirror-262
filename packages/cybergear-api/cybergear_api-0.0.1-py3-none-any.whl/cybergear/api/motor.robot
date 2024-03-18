*** Settings ***

Documentation     关节电机控制库
# Library           MotorLibrary.py    WITH NAME    Motor
Library           cybergear.api.MotorLibrary    WITH NAME    Motor

*** Keywords ***

设置服务器
    [Arguments]    ${IP}    ${PORT}
    ${ret}    Motor.setup_target    ${IP}    ${PORT}
    Log To Console    设置服务器: ${IP} ${PORT}
    [Return]    ${ret}

设置目标电机
    [Arguments]    ${bus_config}     ${motor_id}
    ${ret}    Motor.setup_motor    ${bus_config}    ${motor_id}   
    Log To Console    设置目标电机: ${bus_config} ${motor_id}
    [Return]    ${ret}

使能电机
    [Arguments]
    ${ret}    Motor.Enable
    Log To Console    使能电机
    [Return]    ${ret}

禁用电机
    [Arguments]
    ${ret}    Motor.Disable
    Log To Console    禁用电机
    [Return]    ${ret}

使能位置模式
    [Arguments]
    Motor.Disable
    Motor.PositionMode
    ${ret}    Motor.Enable
    Log To Console    使能位置模式
    [Return]    ${ret}

设置位置和速度
    [Arguments]    ${position}    ${speed}
    ${ret}    Motor.set_position    ${position}    ${speed}
    Log To Console    设置位置和速度: ${position} ${speed}
    [Return]    ${ret}

设置机械零点
    [Arguments]
    Motor.Disable
    Motor.set_0_position
    ${ret}    Motor.Enable
    Log To Console    设置机械零点
    [Return]    ${ret}

使能速度模式
    [Arguments]
    Motor.Disable
    Motor.SpeedMode
    ${ret}    Motor.Enable
    Log To Console    使能速度模式
    [Return]    ${ret}

设置速度
    [Arguments]    ${speed}
    ${ret}    Motor.set_speed    ${speed}
    Log To Console    设置速度: ${speed}
    [Return]    ${ret}

读取所有参数
    [Arguments]
    ${ret}    Motor.read_params
    Log To Console    读取所有参数
    [Return]    ${ret}