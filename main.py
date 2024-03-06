import socket
import struct
import sys
import os
import pprint
import pygame
import time
from enum import IntEnum
from time import sleep
import requests


class Ps4Controls(IntEnum):
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1
    RIGHT_STICK_X = 2
    RIGHT_STICK_Y = 3
    FINGER1_X = 4
    FINGER1_Y = 5
    FINGER2_X = 6
    FINGER2_Y = 7
    SHARE = 128
    OPTIONS = 129
    PS = 130
    UP = 11
    RIGHT = 14
    DOWN = 12
    LEFT = 13
    TRIANGLE = 135
    CIRCLE = 136
    CROSS = 137
    SQUARE = 138
    L1 = 139
    R1 = 140
    L2 = 141
    R2 = 142
    L3 = 143
    R3 = 144
    TOUCHPAD = 145
    FINGER1 = 146
    FINGER2 = 147


class ButtonState(IntEnum):
    RELEASED = 0
    PRESSED = 255


def bool_to_button(_bool):
    return int(_bool) * 255


def parse_button_dict(button_dict):
    """
    Returns a dict with the names of the buttons as keys and the values as integers.
    """
    name_dict = {}
    for key in button_dict.keys():
        if key == 0:
            name_dict["cross"] = bool_to_button(button_dict[key])
        if key == 1:
            name_dict["circle"] = bool_to_button(button_dict[key])
        if key == 2:
            name_dict["triangle"] = bool_to_button(button_dict[key])
        if key == 3:
            name_dict["square"] = bool_to_button(button_dict[key])
        if key == 4:
            name_dict["l1"] = bool_to_button(button_dict[key])
        if key == 5:
            name_dict["r1"] = bool_to_button(button_dict[key])
        if key == 6:
            name_dict["l2"] = bool_to_button(button_dict[key])
        if key == 7:
            name_dict["r2"] = bool_to_button(button_dict[key])
        if key == 8:
            name_dict["share"] = bool_to_button(button_dict[key])
        if key == 9:
            name_dict["options"] = bool_to_button(button_dict[key])
        if key == 10:
            name_dict["PS"] = bool_to_button(button_dict[key])
        if key == 11:
            name_dict["l3"] = bool_to_button(button_dict[key])
        if key == 12:
            name_dict["r3"] = bool_to_button(button_dict[key])
    return name_dict


def bool_to_axis(_bool):
    return int(_bool) * 127


def axis_parser(axis_dict):
    """
    Returns a dict with the names of the axes as keys and the values scaled properly.
    """
    name_dict = {}
    for key in axis_dict.keys():
        if key == 0:
            name_dict["LEFT_STICK_X"] = int(axis_dict[key] * 127)
        if key == 1:
            name_dict["LEFT_STICK_Y"] = int(axis_dict[key] * 127)
        if key == 3:
            name_dict["RIGHT_STICK_X"] = int(axis_dict[key] * 127)
        if key == 4:
            name_dict["RIGHT_STICK_Y"] = int(axis_dict[key] * 127)
    return name_dict


def IN_RANGE(x, a, b, delta):
    if x < a:
        return a
    if x > b:
        return b
    return x + delta


def DEG2RAD(x):
    return x * 3.14159265358979323846 / 180


arm_init_pos = {"T": 1041, "x": 311.94, "y": 1.91, "z": 232.72, "t": DEG2RAD(150)}
arm_cur_pos = arm_init_pos

import time


def send(state):
    start_time = time.time()
    # tank_url = "http://192.168.43.159/js?"
    tank_url = "http://192.168.4.1/js?"
    arm_url = "http://192.168.43.103/js?"
    for i in range(4):
        print(f"{i}: {state[i]}")
    speed = state[Ps4Controls.LEFT_STICK_Y] * 1.2
    print(speed)

    leftX = state[Ps4Controls.LEFT_STICK_X]

    rotateDir = -1 if leftX < 0 else 1
    rotateSpeed = 0.1
    if abs(leftX) > 0.5:
        tank_payload = {
            "T": 1,
            "L": rotateSpeed * rotateDir,
            "R": rotateSpeed * rotateDir * -1,
        }
    else:
        tank_payload = {"T": 1, "L": speed, "R": speed}

    ############## arm #################
    MOV = 10
    T_MOV = DEG2RAD(5)

    Y_LOW = -100
    Y_HIGH = 100
    X_LOW = 100
    X_HIGH = 500
    Z_LOW = 100
    Z_HIGH = 400
    T_LOW = DEG2RAD(100)
    T_HIGH = DEG2RAD(180)

    arm_dis_x = state[Ps4Controls.RIGHT_STICK_X]
    arm_dis_y = state[Ps4Controls.RIGHT_STICK_Y]
    arm_dis_z = state[Ps4Controls.UP] + state[Ps4Controls.DOWN] * -1
    arm_dis_t = state[Ps4Controls.LEFT] + state[Ps4Controls.RIGHT] * -1
    print(arm_dis_x, arm_dis_y)

    arm_cur_pos["y"] = IN_RANGE(arm_cur_pos["y"], Y_LOW, Y_HIGH, (arm_dis_x) * MOV * -1)

    arm_cur_pos["x"] = IN_RANGE(arm_cur_pos["x"], X_LOW, X_HIGH, (arm_dis_y) * MOV * -1)
    arm_cur_pos["z"] = IN_RANGE(arm_cur_pos["z"], Z_LOW, Z_HIGH, (arm_dis_z) * MOV * 1)
    arm_cur_pos["t"] = IN_RANGE(
        arm_cur_pos["t"], T_LOW, T_HIGH, (arm_dis_t) * T_MOV * 1
    )

    print(arm_cur_pos)

    try:
        r = requests.post(tank_url, json=tank_payload, timeout=0.5)
    except requests.exceptions.ConnectionError:
        pass
    except:
        pass

    print("finished sending tank")

    # try:
    #     r = requests.post(arm_url, json=arm_cur_pos, timeout=0.5)
    # except requests.exceptions.ConnectionError:
    #     pass
    # except:
    #     pass

    print("finished sending arm")
    end_time = time.time()
    print(f"time used: {end_time - start_time}")
    return True


def parse_arrow_dict(arrow_dict):
    name_dict = {}
    name_dict["left"] = 255 if arrow_dict[0][0] == -1 else 0
    name_dict["right"] = 255 if arrow_dict[0][0] == 1 else 0
    name_dict["up"] = 255 if arrow_dict[0][1] == 1 else 0
    name_dict["down"] = 255 if arrow_dict[0][1] == -1 else 0
    return name_dict


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            print("No controller found")
            pygame.quit()
            quit()

        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {0: 0, 1: 0, 3: 0, 4: 0}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        self.thres = 0.1
        millis = 0
        running = True

        # connect_hotspot()

        while running:
            try:
                axis_data = {0: 0, 1: 0, 3: 0, 4: 0}
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # # Get controller input
                axes = self.controller.get_numaxes()
                for i in range(axes):
                    axis = self.controller.get_axis(i)
                    if abs(axis) < self.thres:
                        axis = 0
                    self.axis_data[i] = axis

                print(self.axis_data[Ps4Controls.LEFT_STICK_X])
                print(self.axis_data[Ps4Controls.LEFT_STICK_Y])

                # --------------- to be tested --------- #
                buttons = self.controller.get_numbuttons()
                for i in range(buttons):
                    button = self.controller.get_button(i)
                    if i >= 11:
                        self.axis_data[i] = button
                    # print(f"Button {i}: {button}")

                # hats = self.controller.get_numhats()
                # print("hats", hats)
                # for i in range(hats):
                #     hat = self.controller.get_hat(i)
                #     print(f"Hat {i}: {hat}")

                # --------------- to be tested --------- #

                res = send(self.axis_data)

                # ------------------- not-in-use -------------- #
                # for event in pygame.event.get():
                #     if event.type == pygame.JOYAXISMOTION:
                #         self.axis_data[event.axis] = round(event.value, 1)
                #     elif event.type == pygame.JOYBUTTONDOWN:
                #         self.button_data[event.button] = True
                #     elif event.type == pygame.JOYBUTTONUP:
                #         self.button_data[event.button] = False
                #     elif event.type == pygame.JOYHATMOTION:
                #         self.hat_data[event.hat] = event.value

                #     # Insert your code on what you would like to happen for each event here!
                #     # In the current setup, I have the state simply printing out to the screen.

                #     os.system("clear")
                #     # print(
                #     #     self.button_data,
                #     #     self.axis_data,
                #     #     self.hat_data,
                #     #     (" " * 150),
                #     #     end="\r",
                #     # )
                #     # b_dict = parse_button_dict(self.button_data)
                #     a_dict = axis_parser(self.axis_data)
                #     # ar_dict = parse_arrow_dict(self.hat_data)
                #     state = {
                #         Ps4Controls.LEFT_STICK_X: a_dict["LEFT_STICK_X"],
                #         Ps4Controls.LEFT_STICK_Y: a_dict["LEFT_STICK_Y"],
                #         Ps4Controls.RIGHT_STICK_X: a_dict["RIGHT_STICK_X"],
                #         Ps4Controls.RIGHT_STICK_Y: a_dict["RIGHT_STICK_Y"],
                #         # Ps4Controls.SHARE: b_dict["share"],
                #         # Ps4Controls.OPTIONS: b_dict["options"],
                #         # Ps4Controls.PS: b_dict["PS"],
                #         # Ps4Controls.UP: ar_dict["up"],
                #         # Ps4Controls.RIGHT: ar_dict["right"],
                #         # Ps4Controls.DOWN: ar_dict["down"],
                #         # Ps4Controls.LEFT: ar_dict["left"],
                #         # Ps4Controls.TRIANGLE: b_dict["triangle"],
                #         # Ps4Controls.CIRCLE: b_dict["circle"],
                #         # Ps4Controls.CROSS: b_dict["cross"],
                #         # Ps4Controls.SQUARE: b_dict["square"],
                #         # Ps4Controls.L1: b_dict["l1"],
                #         # Ps4Controls.R1: b_dict["r1"],
                #         # Ps4Controls.L2: b_dict["l2"],
                #         # Ps4Controls.R2: b_dict["r2"],
                #         # Ps4Controls.L3: b_dict["l3"],
                #         # Ps4Controls.R3: b_dict["r3"],
                #     }

                # ------------------- not-in-use -------------- #
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
