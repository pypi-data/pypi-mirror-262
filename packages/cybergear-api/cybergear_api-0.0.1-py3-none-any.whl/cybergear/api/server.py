from loguru import logger
from fastapi import FastAPI, APIRouter
from .device import MotorDevice


class Agent(object):
    app: FastAPI
    router: APIRouter

    def __init__(self):
        self.app = FastAPI()
        self.router = APIRouter()
        self.device = MotorDevice()

        # motor 设备控制
        self.router.add_api_route("/motor/setup", self.device.setup, methods=["POST"])
        self.router.add_api_route("/motor/enable", self.device.enable, methods=["GET"])
        self.router.add_api_route("/motor/disable", self.device.disable, methods=["GET"])
        self.router.add_api_route("/motor/speed_mode", self.device.speed_mode, methods=["GET"])
        self.router.add_api_route("/motor/position_mode", self.device.position_mode, methods=["GET"])
        self.router.add_api_route("/motor/set_speed", self.device.set_speed, methods=["GET"])
        self.router.add_api_route("/motor/set_position", self.device.set_position, methods=["GET"])
        self.router.add_api_route("/motor/set_0_position", self.device.set_0_position, methods=["GET"])
        self.router.add_api_route("/motor/read_params", self.device.read_params, methods=["GET"])

        self.app.include_router(self.router)
