import requests

class MotorClient:
    def __init__(self):
        super().__init__()
        self.ip = "127.0.0.1"
        self.port = 8000
        self.session = requests.Session()
        self.session.keep_alive = True
        self.params = {}        # 通用参数

    def setup_target(self, ip: str, port: int):
        """设置目标地址"""
        self.ip = ip
        self.port = port
        return {"status": "ok"}
    
    def setup_motor(self, bus_config: dict, motor_can_id: int):
        """设置电机"""
        url = f"http://{self.ip}:{self.port}/motor/setup"
        data = {
            "bus_config": bus_config,
            "motor_can_id": motor_can_id
        }
        ret = self.session.post(url, json=data)
        return ret.json()
    
    def speed_mode(self):
        """速度模式"""
        url = f"http://{self.ip}:{self.port}/motor/speed_mode"
        ret = self.session.get(url)
        return ret.json()
    
    def position_mode(self):
        """位置模式"""
        url = f"http://{self.ip}:{self.port}/motor/position_mode"
        ret = self.session.get(url)
        return ret.json()
    
    def enable(self):
        """使能"""
        url = f"http://{self.ip}:{self.port}/motor/enable"
        ret = self.session.get(url)
        return ret.json()
    
    def disable(self):
        """禁用"""
        url = f"http://{self.ip}:{self.port}/motor/disable"
        ret = self.session.get(url)
        return ret.json()
    
    def set_speed(self, speed: float):
        """设置速度"""
        url = f"http://{self.ip}:{self.port}/motor/set_speed"
        ret = self.session.get(url, params={"speed": speed})
        return ret.json()
    
    def set_position(self, position: float, speed: float):
        """设置位置和速度"""
        url = f"http://{self.ip}:{self.port}/motor/set_position"
        ret = self.session.get(url, params={"position": position, "speed": speed})
        return ret.json()
    
    def set_0_position(self):
        """设置0点位置"""
        url = f"http://{self.ip}:{self.port}/motor/set_0_position"
        ret = self.session.get(url)
        return ret.json()
    
    def read_params(self):
        """读取所有参数"""
        url = f"http://{self.ip}:{self.port}/motor/read_params"
        ret = self.session.get(url)
        return ret.json()
