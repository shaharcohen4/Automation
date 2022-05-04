import time
import DobotDllType as dType
import os


# Connect Dobot
class Robot:
    def __init__(self):
        self.api = dType.load()
        self.connect = self.connection()

    def connection(self):
        connection = dType.ConnectDobot(self.api, "COM3", 115200)[0]
        return connection

    def get_current_position(self):
        current_positions = dType.GetPose(self.api)
        return current_positions

    def set_position(self, current_position, x, y, z):
        dType.SetPTPCommonParams(self.api, 100, 100, isQueued=0)
        time.sleep(5)
        dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, current_position[0] + x, current_position[1] + y,
                        current_position[2] + z, current_position[3], isQueued=0)

# my_robot = Robot()
# position = my_robot.get_current_position()
# my_robot.set_position(position, 50, 50, 50)
