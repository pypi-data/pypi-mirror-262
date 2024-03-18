import can
from typing import Dict
from pydantic import BaseModel
from cybergear import CANMotorController

class MotorConfig(BaseModel):
    bus_config: Dict = {
        "channel": "PCAN_USBBUS1",
        "bustype": "pcan",
        "bitrate": 1000000,
    }
    motor_can_id: int = 127

class MotorDevice(object):
    _bus: can.interface.Bus = None
    _motor: CANMotorController = None

    def setup(self, config : MotorConfig):
        self.config = config
        if self._motor is not None:
            self._motor.disable()
        if self._bus is not None:
            self._bus.shutdown()
        self._bus = can.interface.Bus(**self.config.bus_config)
        self._motor = CANMotorController(self._bus, self.config.motor_can_id)
        ret = self._motor.disable()     # 禁用电机
        return ret

    def speed_mode(self):
        """速度模式"""
        ret = self._motor.write_single_param("run_mode", value=2)
        return ret

    def position_mode(self):
        """位置模式"""
        ret = self._motor.write_single_param("run_mode", value=1)
        return ret

    def enable(self):
        ret = self._motor.enable()
        return ret

    def disable(self):
        ret = self._motor.disable()
        return ret

    def set_speed(self, speed: float):
        ret = self._motor.write_single_param("spd_ref", value=speed)
        return ret

    def set_position(self, position: float, speed: float):
        """设置位置和速度
        
        Args:
            position (float): 位置
            speed (float): 速度
        """
        ret = self._motor.write_single_param("loc_ref", value=position)
        ret = self._motor.write_single_param("limit_spd", value=speed)
        return ret
    
    def set_0_position(self):
        """设置机械0点位置"""
        ret = self._motor.set_0_pos()
        return ret
    
    def read_params(self):
        """读取所有参数"""
        ret = {}
        for param in self._motor.PARAMETERS.keys():
            _, value = self._motor.read_single_param(param)
            ret[param] = value
        return ret