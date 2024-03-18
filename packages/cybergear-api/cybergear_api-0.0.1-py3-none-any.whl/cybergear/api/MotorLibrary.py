from .client import MotorClient

class MotorLibrary(MotorClient):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_DOC_FORMAT = 'reST'
    ROBOT_LIBRARY_VERSION = "0.1"
