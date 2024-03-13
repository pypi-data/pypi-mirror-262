# # -*- coding: utf-8 -*-
# v1.0.3
# 20230830
# https://linuxcnc.org/docs/2.7/html/config/python-interface.html
import platform
import time
import math
from enum import Enum
import subprocess
import logging
import os
from pymycobot.log import setup_logging
def is_debian_os():
    try:
        # 执行 lsb_release -a 命令，并捕获输出
        result = subprocess.run(['lsb_release', '-a'], capture_output=True, text=True, check=True)

        # 解析输出，获取 Distributor ID 的信息
        lines = result.stdout.split('\n')
        for line in lines:
            if line.startswith('Distributor ID:'):
                distributor_id = line.split(':', 1)[1].strip()
                if distributor_id != "Debian":
                    return False
                return True

    except subprocess.CalledProcessError as e:
        print(f"Error executing lsb_release -a: {e}")
        return False


    return None
if platform.system() == "Linux" and platform.machine() == "aarch64" and is_debian_os():
    import linuxcnc as elerob
    import hal
    class JogMode(Enum):
        JOG_JOINT = elerob.ANGULAR - 1
        JOG_TELEOP = elerob.LINEAR - 1
from time import sleep

COORDS_EPSILON = 0.50
MAX_JOINTS = 6
MAX_CARTE = 3
jog_velocity = 1.0  # 100.0/60.0
angular_jog_velocity = 3600 / 60
MAX_PINS = 64
MAX_ANGULAR_SPEED = 6930
MAX_LINEAR_SPEED = 30000
DEFAULT_XY_TORQUE_LIMIT = 55
DEFAULT_Z_TORQUE_LIMIT = 30


class TaskMode(Enum):
    MANUAL = 1
    AUTO = 2
    MDI = 3


class RobotMoveState(Enum):
    IDLE_STATE = 0
    JOG_JOINT_STATE = 1
    JOG_AXIS_STATE = 2
    MOVE_AXIS_STATE = 3
    MOVE_JOINT_STATE = 4
    RUN_PROGRAM_STATE = 5


class JogDirection(Enum):
    POSITIVE = 1
    NEGATIVE = -1


class Axis(Enum):
    X = 0
    Y = 1
    Z = 2
    RX = 3
    RY = 4
    RZ = 5


class Joint(Enum):
    J1 = 0
    J2 = 1
    J3 = 2
    J4 = 3
    J5 = 4
    J6 = 5


class DI(Enum):
    """Available Digital Input Pins."""

    PIN_0 = 0
    PIN_1 = 1
    PIN_2 = 2
    PIN_3 = 3
    PIN_4 = 4
    PIN_5 = 5
    PIN_6 = 6
    PIN_7 = 7
    PIN_8 = 8
    PIN_9 = 9
    PIN_10 = 10
    PIN_11 = 11
    PIN_12 = 12
    PIN_13 = 13
    PIN_14 = 14

    CAT_PHYSICAL_START = 15
    CAT_PHYSICAL_STOP = 16
    CAT_PHYSICAL_USER_DEFINE = 17

    PIN_18 = 18
    PIN_19 = 19
    PIN_20 = 20
    PIN_21 = 21
    PIN_22 = 22
    PIN_23 = 23
    PIN_24 = 24
    PIN_25 = 25
    PIN_26 = 26
    PIN_27 = 27
    PIN_28 = 28
    PIN_29 = 29
    PIN_30 = 30
    PIN_31 = 31
    PIN_32 = 32
    PIN_33 = 33

    J1_COMMUNICATION = 34
    J2_COMMUNICATION = 35
    J3_COMMUNICATION = 36
    J4_COMMUNICATION = 37
    J5_COMMUNICATION = 38
    J6_COMMUNICATION = 39

    IO_STOP_TRIGGERED = 40
    IO_RUN_TRIGGERED = 41

    PIN_42 = 42

    HARDWARE_PAUSE_PRESSED = 43

    BRAKE_ACTIVATION_RUNNING = 44
    J1_SERVO_ENABLED = 45
    J2_SERVO_ENABLED = 46
    J3_SERVO_ENABLED = 47
    J4_SERVO_ENABLED = 48
    J5_SERVO_ENABLED = 49
    J6_SERVO_ENABLED = 50

    HARDWARE_FREE_MOVE = 51
    MOTION_ENABLE = 52

    PIN_53 = 53
    PIN_54 = 54
    PIN_55 = 55

    J1_STATUS = 56
    J2_STATUS = 57
    J3_STATUS = 58
    J4_STATUS = 59
    J5_STATUS = 60
    J6_STATUS = 61

    EMERGENCY_STOP = 62
    POWER_ON_STATUS = 63


class DO(Enum):
    """Available Digital Output Pins."""

    PIN_0 = 0
    PIN_1 = 1
    PIN_2 = 2
    PIN_3 = 3
    PIN_4 = 4
    PIN_5 = 5
    PIN_6 = 6
    PIN_7 = 7
    PIN_8 = 8
    PIN_9 = 9
    PIN_10 = 10
    PIN_11 = 11
    PIN_12 = 12
    PIN_13 = 13
    PIN_14 = 14
    PIN_15 = 15
    PIN_16 = 16
    PIN_17 = 17
    PIN_18 = 18
    PIN_19 = 19
    PIN_20 = 20
    PIN_21 = 21
    PIN_22 = 22
    PIN_23 = 23
    PIN_24 = 24
    PIN_25 = 25
    PIN_26 = 26
    PIN_27 = 27
    PIN_28 = 28
    PIN_29 = 29
    PIN_30 = 30
    PIN_31 = 31
    PIN_32 = 32
    PIN_33 = 33
    PIN_34 = 34
    PIN_35 = 35
    PIN_36 = 36
    PIN_37 = 37
    PIN_38 = 38
    PIN_39 = 39
    PIN_40 = 40
    PIN_41 = 41
    PIN_42 = 42
    PIN_43 = 43
    PIN_44 = 44
    PIN_45 = 45
    PIN_46 = 46

    BRAKE_ACTIVE_AUTO = 47
    BRAKE_MANUAL_MODE_ENABLE = 48
    J1_BRAKE_RELEASE = 49
    J2_BRAKE_RELEASE = 50
    J3_BRAKE_RELEASE = 51
    J4_BRAKE_RELEASE = 52
    J5_BRAKE_RELEASE = 53
    J6_BRAKE_RELEASE = 54

    SKIP_INIT_ERRORS = 55
    PROGRAM_AUTO_RUNNING = 56
    POWER_ON_RELAY_1 = 57
    POWER_ON_RELAY_2 = 58

    PIN_59 = 59

    SOFTWARE_FREE_MOVE = 60

    PIN_61 = 61
    PIN_62 = 62
    PIN_63 = 63


class AI(Enum):
    """Available Analog Input Pins."""

    PIN_0 = 0
    PIN_1 = 1
    PIN_2 = 2
    PIN_3 = 3
    PIN_4 = 4
    PIN_5 = 5
    PIN_6 = 6
    PIN_7 = 7
    PIN_8 = 8
    PIN_9 = 9
    PIN_10 = 10
    PIN_11 = 11
    PIN_12 = 12
    PIN_13 = 13
    PIN_14 = 14
    PIN_15 = 15
    PIN_16 = 16
    PIN_17 = 17
    PIN_18 = 18
    PIN_19 = 19
    PIN_20 = 20
    PIN_21 = 21
    PIN_22 = 22
    PIN_23 = 23
    PIN_24 = 24
    PIN_25 = 25
    PIN_26 = 26
    PIN_27 = 27
    PIN_28 = 28
    PIN_29 = 29
    PIN_30 = 30

    J1_VOLTAGE = 31
    J2_VOLTAGE = 32
    J3_VOLTAGE = 33
    J4_VOLTAGE = 34
    J5_VOLTAGE = 35
    J6_VOLTAGE = 36

    J1_TEMPERATURE = 37
    J2_TEMPERATURE = 38
    J3_TEMPERATURE = 39
    J4_TEMPERATURE = 40
    J5_TEMPERATURE = 41
    J6_TEMPERATURE = 42

    J1_WINDING_A_CURRENT = 43
    J2_WINDING_A_CURRENT = 44
    J3_WINDING_A_CURRENT = 45
    J4_WINDING_A_CURRENT = 46
    J5_WINDING_A_CURRENT = 47
    J6_WINDING_A_CURRENT = 48

    J1_WINDING_B_CURRENT = 49
    J2_WINDING_B_CURRENT = 50
    J3_WINDING_B_CURRENT = 51
    J4_WINDING_B_CURRENT = 52
    J5_WINDING_B_CURRENT = 53
    J6_WINDING_B_CURRENT = 54

    ROBOT = 55

    ROBOT_AVG_POWER = 56
    CONTROLLER_TEMPERATURE = 57

    J1_CURRENT = 58
    J2_CURRENT = 59
    J3_CURRENT = 60
    J4_CURRENT = 61
    J5_CURRENT = 62
    J6_CURRENT = 63


class AO(Enum):
    """Available Analog Output Pins."""

    PIN_0 = 0
    PIN_1 = 1
    PIN_2 = 2
    PIN_3 = 3
    PIN_4 = 4
    PIN_5 = 5
    PIN_6 = 6
    PIN_7 = 7
    PIN_8 = 8
    PIN_9 = 9
    PIN_10 = 10
    PIN_11 = 11
    PIN_12 = 12
    PIN_13 = 13
    PIN_14 = 14
    PIN_15 = 15

    LED_LIGHT = 16

    PIN_17 = 17
    PIN_18 = 18
    PIN_19 = 19
    PIN_20 = 20
    PIN_21 = 21
    PIN_22 = 22
    PIN_23 = 23
    PIN_24 = 24
    PIN_25 = 25
    PIN_26 = 26
    PIN_27 = 27
    PIN_28 = 28
    PIN_29 = 29
    PIN_30 = 30
    PIN_31 = 31
    PIN_32 = 32
    PIN_33 = 33
    PIN_34 = 34
    PIN_35 = 35
    PIN_36 = 36
    PIN_37 = 37
    PIN_38 = 38
    PIN_39 = 39
    PIN_40 = 40

    ACCELERATION = 41

    PIN_42 = 42
    PIN_43 = 43
    PIN_44 = 44
    PIN_45 = 45
    PIN_46 = 46
    PIN_47 = 47

    TOOL_FORCE = 48
    TOOL_SPEED = 49
    STOPPING_DISTANCE = 50
    STOPPING_TIME = 51
    POWER_LIMIT = 52

    PAYLOAD = 53

    PIN_54 = 54
    PIN_55 = 55

    J1_TORQUE = 56
    J2_TORQUE = 57
    J3_TORQUE = 58
    J4_TORQUE = 59
    J5_TORQUE = 60
    J6_TORQUE = 61

    XY_AXIS_TORQUE = 62
    Z_AXIS_TORQUE = 63


class Robots(Enum):
    ELEPHANT = 101
    PANDA_3 = 201
    PANDA_5 = 202
    CAT_3 = 301
    MY_COB = 401
    MY_COB_PRO = 402
    PRO_320 = 501
    PRO_600 = 502


class JointState(Enum):
    OK = 0
    ERROR = 1
    POWERED_OFF = 2


class Phoenix:
    """Interface for phoenix.

    Example:
      - Start / Stop Robot Workflow:
        1. start_robot() or start_power_on_only()
        2. shutdown_robot()
        3. go to 1.
    """

    def __init__(self, debug=False):
        self.c = elerob.command()
        self.s = elerob.stat()
        self.e = elerob.error_channel()
        self.robot_state = RobotMoveState.IDLE_STATE
        self.command_id = 0
        self.current_robot = 0
        self.init_hal()
        self.init_robot()
        setup_logging(debug)

    # def __del__(self):
    #     self.stop_force_sensor()
    #     self.g.unready()
    #     self.hal_serial.unready()

    def init_hal(self):
        self.init_hal_gpio()
        self.init_hal_serial()
        self.apply_hal_config()

    def init_hal_gpio(self):
        """Inits HAL pins in halgpio component."""

        self.g = hal.component("halgpio", "halgpio")

        for i in range(MAX_PINS):
            self.g.newpin("digital-in-" + str(i).zfill(2), hal.HAL_BIT, hal.HAL_IN)
            self.g.newpin("digital-out-" + str(i).zfill(2), hal.HAL_BIT, hal.HAL_OUT)
            self.g.newpin("analog-in-" + str(i).zfill(2), hal.HAL_FLOAT, hal.HAL_IN)
            self.g.newpin("analog-out-" + str(i).zfill(2), hal.HAL_FLOAT, hal.HAL_OUT)

        # 0 .. MAX_JOINTS: joint status word
        # MAX_JOINTS .. MAX_JOINTS * 2: joint error mask
        for i in range(MAX_JOINTS * 2):
            self.g.newpin("U32-in-" + str(i).zfill(2), hal.HAL_U32, hal.HAL_IN)

        for i in range(MAX_JOINTS):
            self.g.newpin(str(i) + ".min_limit", hal.HAL_FLOAT, hal.HAL_OUT)
            self.g.newpin(str(i) + ".max_limit", hal.HAL_FLOAT, hal.HAL_OUT)

        self.g.ready()

    def init_hal_serial(self):
        self.hal_serial = hal.component("serial", "serial")

        self.hal_serial.newpin("0.xtorq", hal.HAL_FLOAT, hal.HAL_OUT)
        self.hal_serial.newpin("0.ytorq", hal.HAL_FLOAT, hal.HAL_OUT)
        self.hal_serial.newpin("0.ztorq", hal.HAL_FLOAT, hal.HAL_OUT)
        self.hal_serial.newpin("0.atorq", hal.HAL_FLOAT, hal.HAL_OUT)
        self.hal_serial.newpin("0.btorq", hal.HAL_FLOAT, hal.HAL_OUT)
        self.hal_serial.newpin("0.ctorq", hal.HAL_FLOAT, hal.HAL_OUT)

        self.hal_serial.newpin("0.sensor_torq_open", hal.HAL_U32, hal.HAL_OUT)
        self.hal_serial.newpin("0.sensor_error_pkgs", hal.HAL_U32, hal.HAL_OUT)
        self.hal_serial.newpin("0.sensor_recv_timeout", hal.HAL_U32, hal.HAL_OUT)
        self.hal_serial.newpin("0.motion_flexible", hal.HAL_U32, hal.HAL_OUT)

        self.hal_serial.ready()

    def apply_hal_config(self):
        os.system(
            "halcmd -f $(dirname $(grep LAST_CONFIG ~/.linuxcncrc | cut -d' ' -f3))/elerob_gpio.hal"
        )

    def init_robot(self):
        self.detect_robot()
        self._set_free_move(False)

        self.set_carte_torque_limit(Axis.X, DEFAULT_XY_TORQUE_LIMIT)
        self.set_carte_torque_limit(Axis.Y, DEFAULT_XY_TORQUE_LIMIT)
        self.set_carte_torque_limit(Axis.Z, DEFAULT_Z_TORQUE_LIMIT)

        self.set_acceleration(400)

        self.joint_brake(Joint.J1, 0)
        self.joint_brake(Joint.J2, 0)
        self.joint_brake(Joint.J3, 0)
        self.joint_brake(Joint.J4, 0)
        self.joint_brake(Joint.J5, 0)
        self.joint_brake(Joint.J6, 0)

        # joint torque limits
        self.set_joint_torque_limit(Joint.J1, 0.15)
        self.set_joint_torque_limit(Joint.J2, 0.15)
        self.set_joint_torque_limit(Joint.J3, 0.12)
        self.set_joint_torque_limit(Joint.J4, 0.10)
        self.set_joint_torque_limit(Joint.J5, 0.10)
        self.set_joint_torque_limit(Joint.J6, 0.10)

        self.set_payload(1.0)

        # joint angle limits
        self.set_joint_min_pos_limit(Joint.J1, -180)
        self.set_joint_min_pos_limit(Joint.J2, -270)
        self.set_joint_min_pos_limit(Joint.J3, -150)
        self.set_joint_min_pos_limit(Joint.J4, -260)
        self.set_joint_min_pos_limit(Joint.J5, -168)
        self.set_joint_min_pos_limit(Joint.J6, -174)

        self.set_joint_max_pos_limit(Joint.J1, 180)
        self.set_joint_max_pos_limit(Joint.J2, 90)
        self.set_joint_max_pos_limit(Joint.J3, 150)
        self.set_joint_max_pos_limit(Joint.J4, 80)
        self.set_joint_max_pos_limit(Joint.J5, 168)
        self.set_joint_max_pos_limit(Joint.J6, 174)

        self.set_motion_flexible(0)

    def detect_robot(self):
        robot = Robots(self.get_analog_in(AI.ROBOT))
        if robot == Robots.ELEPHANT:
            self.current_robot = 0
        elif robot == Robots.PANDA_3:
            self.current_robot = 1
        elif robot == Robots.PANDA_5:
            self.current_robot = 2
        elif robot == Robots.CAT_3:
            self.current_robot = 3
        elif robot == Robots.MY_COB:
            self.current_robot = 4
        elif robot == Robots.MY_COB_PRO:
            self.current_robot = 5
        elif robot == Robots.PRO_320:
            self.current_robot = 6
        elif robot == Robots.PRO_600:
            self.current_robot = 7

    def start_robot(self, power_on_only=False):
        """Start robot"""
        self.power_off()
        time.sleep(0.5)
        power_on_ok = self.is_power_on()
        power_on_retry_count = 0
        while (not power_on_ok) and (power_on_retry_count <= 10):
            if power_on_only:
                self.power_on_only()
            else:
                self.power_on()
            power_on_retry_count += 1
            power_on_ok = self.is_power_on()
            time.sleep(1)
        power_on_ok = self.is_power_on()
        if not power_on_ok:
            print("power_on_ok is false")
            return False
        # power on ok
        servo_enable_ok = False
        servo_enable_retry_count = 0
        while (not servo_enable_ok) and (servo_enable_retry_count <= 30):
            servo_enable_ok = self.is_all_servo_enabled()
            time.sleep(1)
            servo_enable_retry_count += 1
        if not servo_enable_ok:
            print("servo_enable_ok is false")
            return False
        # servo motor ok
        # self.state_on()
        robot_type = self.get_analog_in(AI.ROBOT)
        if (robot_type == Robots.PANDA_3) or (robot_type == Robots.PANDA_5):
            brake_active_ok = False
            brake_active_retry_count = 0
            while (not brake_active_ok) and (brake_active_retry_count <= 20):
                self.state_on()
                brake_active_ok = not self.get_digital_in(DI.BRAKE_ACTIVATION_RUNNING)
                time.sleep(1)
                brake_active_retry_count += 1
            if not brake_active_ok:
                print("brake_active_ok is false")
                return False
        state_on_ok = self.state_check()
        state_on_retry_count = 0
        while (not state_on_ok) and (state_on_retry_count <= 5):
            self.state_on()
            time.sleep(2)
            state_on_ok = self.state_check()
            state_on_retry_count += 1
        if not state_on_ok:
            print("state_on_ok is false")
            return False

        return True

    def start_power_on_only(self):
        """Start robot with power on only

        Returns:
            True if success, False otherwise
        """
        return self.start_robot(power_on_only=True)

    def shutdown_robot(self):
        self.power_off()

    def power_on(self):
        """Powers on and prepares for operation the robot."""
        self.s.poll()
        if self.s.task_state == elerob.STATE_ESTOP:
            self.set_estop_reset()
        self.set_digital_out(DO.POWER_ON_RELAY_1, 1)
        time.sleep(0.25)
        self.set_digital_out(DO.POWER_ON_RELAY_2, 1)
        time.sleep(0.25)
        self.set_digital_out(DO.POWER_ON_RELAY_2, 0)

        self._set_free_move(False)

        if self.current_robot != Robots.ELEPHANT.value:
            self.set_digital_out(DO.BRAKE_ACTIVE_AUTO, 0)
            time.sleep(0.1)
            self.set_digital_out(DO.BRAKE_ACTIVE_AUTO, 1)

        return True

    def power_on_only(self):
        """Only powers on the robot."""
        self.set_digital_out(DO.POWER_ON_RELAY_1, 1)
        time.sleep(0.25)
        self.set_digital_out(DO.POWER_ON_RELAY_2, 1)
        time.sleep(0.25)
        self.set_digital_out(DO.POWER_ON_RELAY_2, 0)
        self.set_estop()
        self._set_free_move(False)
        return True

    def power_off(self):
        """Powers off the robot."""
        self.set_digital_out(DO.POWER_ON_RELAY_1, 0)
        self.set_digital_out(DO.POWER_ON_RELAY_2, 0)
        if self.current_robot != Robots.ELEPHANT.value:
            self.set_digital_out(DO.BRAKE_ACTIVE_AUTO, 0)
        return True

    # TODO blockly 12-18测试可用
    def get_coords(self):
        """Returns current robot coordinates.

        Returns:
            list[float]: list of 6 float values for each axis
        """
        c = self.get_actual_position()
        return c

    # TODO blockly 12-18测试可用
    def set_coords(self, coords, speed):
        """Set coords

        Args:
            coords (list[float]): coords to set, list[float] of size 6
            speed (float): speed percentage (0 ~ 100 %)
        """
        if self.is_in_position(coords, True):
            return True
        self.set_robot_move_state(RobotMoveState.MOVE_AXIS_STATE, 0, 0)
        return self.send_mdi(
            "G01F" + str(speed * MAX_LINEAR_SPEED / 100) + self.coords_to_gcode(coords)
        )

    # TODO blockly 12-18测试可用
    def get_coord(self, axis):
        """Returns current coord of specified axis

        Args:
            axis (Axis): axis

        Returns:
            float: current coord of specified axis
        """
        return self.get_coords()[axis.value]

    # TODO blockly 12-18测试可用
    def set_coord(self, axis, coord, speed):
        """Set coord of axis

        Args:
            axis (Axis): Axis.X ~ Axis.RY
            coord (float): coord value
            speed (float): speed percentage (1 ~ 100 %)
        """
        coords = self.get_coords()
        coords[axis.value] = coord
        self.set_coords(coords, speed)

    # TODO blockly 12-18测试可用
    def get_angles(self):
        """Returns current joint angles

        Returns:
            list[float]: current angles list[float] of size MAX_JOINTS
        """
        return self.get_actl_joint_float()

    # TODO blockly 12-18测试可用
    def set_angles(self, angles, speed):
        """Sets angles

        Args:
            angles (list[float]): joint angles, list[float] of size MAX_JOINTS
            speed (float): speed percentage (1 ~ 100 %)
        """
        if self.is_in_position(angles, False):
            return
        self.set_robot_move_state(RobotMoveState.MOVE_JOINT_STATE, 0, 0)
        self.send_mdi(
            "G38.3F"
            + str(speed * MAX_ANGULAR_SPEED / 100)
            + self.angles_to_gcode(angles)
        )

    # TODO blockly 12-18测试可用
    def get_angle(self, joint):
        """Returns specified joint's current angle

        Args:
            joint (Joint): Joint.J1 (0) ~ Joint.J6 (5)

        Returns:
            float: specified joint angle
        """
        return self.get_angles()[joint.value]

    # TODO blockly 12-18测试可用
    def set_angle(self, joint, angle, speed):
        """Sets specified joint's angle to given value with passed speed.

        Args:
            joint (Joint): 0 ~ 5 or Joint.J1 ~ Joint.J6
            angle (float): angle to set
            speed (float): speed percentage (0 ~ 100 %)
        """
        angles = self.get_angles()
        if isinstance(joint, int):
            angles[joint] = angle
        elif isinstance(joint, Joint):
            angles[joint.value] = angle
        self.set_angles(angles, speed)

    # TODO blockly 12-18测试可用
    def get_speed(self):
        """_summary_"""
        return self.get_current_velocity()

    def state_on(self):
        """Sets robot state to ON.

        Returns:
            bool: True if success, False otherwise.
        """
        self.s.poll()
        if self.s.estop:  # FIXME: add errors check...
            return False
        if self.s.task_mode != elerob.MODE_MANUAL:
            self.c.mode(elerob.MODE_MANUAL)
            self.c.wait_complete()
            time.sleep(0.2)
        self.s.poll()
        if self.s.motion_mode != elerob.TRAJ_MODE_FREE:
            self.c.teleop_enable(0)
            self.c.wait_complete()
            time.sleep(0.1)
        self.c.state(elerob.STATE_ON)
        self.c.wait_complete()
        time.sleep(0.1)
        if self.state_check():
            self.send_mdi("G64 P1")
            self.task_stop()
            time.sleep(0.1)
        self.set_robot_move_state(RobotMoveState.IDLE_STATE, 0, 0)
        return True

    def state_off(self):
        """Sets robot state to OFF."""
        self.c.state(elerob.STATE_OFF)
        self.c.wait_complete()

    def state_check(self):
        """Checks if robot's state is ready for operation.

        Currently only checks motion enable flag.

        Returns:
            bool: True if robot state is ready for operation, False otherwise.
        """
        return self.get_motion_enabled()

    def check_running(self):
        """Returns True if robot is moving, False otherwise.

        Returns:
            bool: True if robot is moving, False otherwise
        """
        return not self.is_in_commanded_position()

    # TODO blockly 12-18测试可用
    def is_in_position(self, coords, is_linear):
        """Returns True if current position equals passed coords.

        Args:
            coords (list[float]): coords or angles
            is_linear (bool): False (0) - angles, True (1) - coords

        Returns:
            bool: True if robot is in passed coords, False otherwise
        """
        if is_linear:
            return self.coords_equal(self.get_coords(), coords)
        else:
            return self.angles_equal(self.get_angles(), coords)

    def set_free_move_mode(self, on=True):
        """Enables or disables free move mode.

        Args:
            on (bool, optional): True to enable free move mode,
                                 False to disable free move mode.
                                 Defaults to True.

        Returns:
            bool: True if success, False otherwise
        """
        if on:
            if not self.state_check():
                return False
        self._set_free_move(on)
        if not on:
            self.state_on()
        return True

    def _set_free_move(self, on=True):
        """Sets free move.

        Args:
            on (bool): True to enable, False to disable
        """
        if on:
            self.set_jog_mode(JogMode.JOG_TELEOP)
        self.set_digital_out(DO.SOFTWARE_FREE_MOVE, on)

    def is_software_free_move(self):
        """Checks if free move mode is enabled by set_free_move_mode() function
           or other similar API.

        Returns:
            bool: True if free move mode enabled by software, False otherwise
        """
        return bool(self.get_digital_out(DO.SOFTWARE_FREE_MOVE))

    def is_hardware_free_move(self):
        """Checks if free move mode is enabled by hardware (button).

        Returns:
            bool: True if free move mode is enabled by hardware (button)
        """
        return bool(self.get_digital_in(DI.HARDWARE_FREE_MOVE))

    def set_payload(self, payload_weight):
        """Sets current payload weight

        Args:
            payload_weight (float): payload weight in kg
        """
        self.set_analog_out(AO.PAYLOAD, payload_weight)

    def is_program_run_finished(self):
        """Checks if program run finished

        Returns:
            bool: True if program run finished, False otherwise
        """
        return not self.is_program_running(True)

    def is_program_paused(self):
        """Checks if program is paused

        Returns:
            bool: True if program is paused, False otherwise
        """
        self.s.poll()
        return self.s.paused

    def get_error(self):
        """Reads next error and returns type, error code, description as tuple

        Returns:
            tuple[str, int, str]: error info
        """
        type, kind, text = None, None, None
        error = self.e.poll()
        if error:
            kind, text = error
            if kind in (elerob.NML_ERROR, elerob.OPERATOR_ERROR):
                type = "error"
            else:
                type = "info"
        return (type, kind, text)

    def is_power_on(self):
        """Checks if robot is powered on

        Returns:
            bool: True if robot is powered on, False otherwise
        """
        return bool(self.get_digital_in(DI.POWER_ON_STATUS))

    def is_servo_enabled(self, joint):
        """Checks if servo corresponding to the specified joint is enabled

        Args:
            joint (Joint): Joint.J1 ~ Joint.J6

        Returns:
            bool: True if servo is enabled, False otherwise
        """
        return bool(self.get_digital_in(DI(DI.J1_SERVO_ENABLED.value + joint.value)))

    def is_all_servo_enabled(self):
        """Checks if all servos are enabled

        Returns:
            bool: True if all servos are enabled, False otherwise
        """
        return bool(
            self.is_servo_enabled(Joint.J1)
            and self.is_servo_enabled(Joint.J2)
            and self.is_servo_enabled(Joint.J3)
            and self.is_servo_enabled(Joint.J4)
            and self.is_servo_enabled(Joint.J5)
            and self.is_servo_enabled(Joint.J6)
        )

    # TODO blockly 12-18测试可用
    def get_joint_min_pos_limit(self, joint):
        """Returns minimum position limit value of specified joint

        Args:
            joint_number (Joint): Joint.J1 ~ Joint.J6

        Returns:
            float: minimum position limit value of specified joint
        """
        return self.g[str(joint.value) + ".min_limit"]

    # TODO blockly 12-18测试可用
    def set_joint_min_pos_limit(self, joint, limit):
        """Sets minimum position limit value of specified joint

        Args:
            joint_number (Joint): Joint.J1 ~ Joint.J6
            limit (float): minimum position limit value of specified joint
        """
        self.g[str(joint.value) + ".min_limit"] = limit

    # TODO blockly 12-18测试可用
    def get_joint_max_pos_limit(self, joint):
        """Returns maximum position limit value of specified joint

        Args:
            joint_number (Joint): Joint.J1 ~ Joint.J6

        Returns:
            float: maximum position limit value of specified joint
        """
        return self.g[str(joint.value) + ".max_limit"]

    # TODO blockly 12-18测试可用
    def set_joint_max_pos_limit(self, joint, limit):
        """Sets maximum position limit value of specified joint

        Args:
            joint_number (Joint): Joint.J1 ~ Joint.J6
            limit (float): maximum position limit value of specified joint
        """
        self.g[str(joint.value) + ".max_limit"] = limit

    # def set_joint_max_velocity(self, joint, limit):
    #     """_summary_

    #     Args:
    #         joint (_type_): _description_
    #         limit (_type_): _description_
    #     """
    #     raise NotImplementedError

    def get_current_cnc_mode(self):
        """Returns current task mode

        Returns:
            TaskMode: one of TaskMode enum values: AUTO, MANUAL, MDI
        """
        self.s.poll()
        return TaskMode(self.s.task_mode)

    def set_estop_reset(self):
        """Resets E-Stop state of the robot."""
        self.c.state(elerob.STATE_ESTOP_RESET)
        self.c.wait_complete()

    def set_estop(self):
        """Puts robot into E-Stop state."""
        self.c.state(elerob.STATE_ESTOP)
        self.c.wait_complete()

    def get_acceleration(self):
        """Returns acceleration value of robot

        Returns:
            float: acceleration value
        """
        return self.get_analog_out(AO.ACCELERATION)

    def set_mode(self, mode):
        """Sets mode to mode.

        Args:
            mode (TaskMode): one of TaskMode.AUTO, TaskMode.MANUAL, TaskMode.MDI

        Returns:
            bool: always returns True
        """
        self.s.poll()
        if self.s.task_mode == mode.value:
            return True
        self.c.mode(mode.value)
        self.c.wait_complete()
        return True

    def joint_brake(self, joint, release):
        """Releases or enables specified joint's brake.

        Args:
            joint (Joint): joint
            release (bool): True to release, False to enable brake
        """
        self.set_digital_out(DO(joint.value + DO.J1_BRAKE_RELEASE.value), release)

    def is_cnc_in_mdi_mode(self):
        """Checks if robot is in MDI mode.

        Returns:
            bool: True if robot is in MDI mode
        """
        self.s.poll()
        return self.s.task_mode == elerob.MODE_MDI

    def set_cnc_in_mdi_mode(self):
        """Sets robot mode to MDI."""
        self.ensure_mode(TaskMode.MDI)

    def get_motion_line(self):
        """Returns source line number motion is currently executing.

        Returns:
            int: motion line number
        """
        self.s.poll()
        return self.s.motion_line

    def set_teleop(self, enable):
        """Enables/disables teleop mode (cartesian movement by axes).

        Args:
            enable (bool): True to enable (cartesian movement), False to disable (joint movement)
        """
        self.c.teleop_enable(enable)
        self.c.wait_complete()

    def get_robot_status(self):
        """Returns robot status

        Returns:
            bool: True if OK, False if disabled / error / cannot move
        """
        return self.state_check()

    # TODO blockly 12-18测试可用
    def get_robot_temperature(self):
        """Returns robot (currently CPU) temperature.

        Returns:
            float: robot temperature
        """
        cpu_temp = CPUTemperature()
        return cpu_temp.temperature

    # TODO blockly 12-18测试可用
    def get_robot_power(self):
        """Returns robot current consuming power in Watts (W).

        Returns:
            float: current consuming power
        """
        robot_power = 17
        for i in range(MAX_JOINTS):
            robot_power += self.get_joint_voltage(Joint(i)) * math.fabs(
                self.get_joint_current(Joint(i))
            )
        return robot_power

    def get_joint_state(self, joint):
        """Returns specified joint's state.

        Args:
            joint (Joint): Joint.J1 ~ Joint.J6

        Returns:
            JointState: joint state
        """
        joint_status = self.g["U32-in-" + str(joint.value).zfill(2)]
        if joint_status & (1 << 1):
            if joint_status & (1 << 3):
                return JointState.ERROR
            return JointState.OK
        return JointState.POWERED_OFF

    def get_joint_temperature(self, joint):
        """Returns specified joint's temperature.

        Args:
            joint (Joint): joint

        Returns:
            float: joint temperature
        """
        return self.get_analog_in(AI(AI.J1_TEMPERATURE.value + joint.value))

    # TODO blockly 12-18测试可用
    def get_joint_communication(self, joint):
        """Returns True if specified joint's communication is OK.

        Args:
            joint (Joint): joint

        Returns:
            bool: True if joint communication is OK, False otherwise
        """
        return not self.get_digital_in(DI(DI.J1_COMMUNICATION.value + joint.value))

    def get_joint_voltage(self, joint):
        """Returns specified joint's voltage.

        Args:
            joint (Joint): joint

        Returns:
            float: voltage
        """
        return self.get_analog_in(AI(AI.J1_VOLTAGE.value + joint.value))

    def get_joint_current(self, joint):
        """Returns specified joint's current.

        Args:
            joint (Joint): joint

        Returns:
            float: current
        """
        return self.get_analog_in(AI(AI.J1_WINDING_A_CURRENT.value + joint.value))

    def get_joint_error_mask(self, joint):
        """Returns specified joint's error mask

        Args:
            joint (Joint): joint

        Returns:
            int: error mask
        """
        return self.g["U32-in-" + str(joint.value + MAX_JOINTS).zfill(2)]

    def set_power_limit(self, power_limit):
        """Sets robot power limit.

        Args:
            power_limit (float): power limit
        """
        self.set_analog_out(AO.POWER_LIMIT, power_limit)

    def get_power_limit(self):
        """Returns current robot power limit.

        Returns:
            float: power limit
        """
        return self.get_analog_out(AO.POWER_LIMIT)

    def set_stopping_time(self, stopping_time):
        """Sets stopping time

        Args:
            stopping_time (float): stopping time
        """
        self.set_analog_out(AO.STOPPING_TIME, stopping_time)

    def get_stopping_time(self):
        """Returns stopping time.

        Returns:
            float: stopping time
        """
        return self.get_analog_out(AO.STOPPING_TIME)

    def set_stopping_distance(self, stopping_distance):
        """Sets stopping distance.

        Args:
            stopping_distance (float): stopping distance
        """
        self.set_analog_out(AO.STOPPING_DISTANCE, stopping_distance)

    def get_stopping_distance(self):
        """Returns current stopping distance.

        Returns:
            float: stopping distance
        """
        return self.get_analog_out(AO.STOPPING_DISTANCE)

    def set_tool_speed(self, tool_speed):
        """Sets tool speed.

        Args:
            tool_speed (float): tool speed
        """
        self.set_analog_out(AO.TOOL_SPEED, tool_speed)

    def get_tool_speed(self):
        """Returns tool speed

        Returns:
            float: tool speed
        """
        return self.get_analog_out(AO.TOOL_SPEED)

    def set_tool_force(self, tool_force):
        """Sets tool force.

        Args:
            tool_force (float): tool force
        """
        self.set_analog_out(AO.TOOL_FORCE, tool_force)

    def get_tool_force(self):
        """Returns current tool force.

        Returns:
            float: tool force
        """
        return self.get_analog_out(AO.TOOL_FORCE)

    # def start_force_sensor(self):
    #     """Not Implemented"""
    #     raise NotImplementedError

    # def stop_force_sensor(self):
    #     """Not Implemented"""
    #     return

    def set_motion_flexible(self, flexible):
        """Sets motion flexible flag.

        Args:
            flexible (bool): True / False
        """
        self.hal_serial["0.motion_flexible"] = flexible

    def get_actual_position(self):
        """Returns actual coord position.

        Returns:
            list[float]: actual coord position
        """
        return self.get_actl_pos_float()

    def get_actual_joints(self):
        """Returns actual joints angles.

        Returns:
            list[float]: actual joints angles
        """
        return self.get_actl_joint_float()

    def is_in_commanded_position(self):
        """Returns machine-in-position flag. True if commanded position
        equals actual position.
        返回机器就位标志。如果指令位置为True，等于实际位置。

        Returns:
            bool: machine-in-position flag
        """
        self.s.poll()
        return self.s.inpos

    def set_acceleration(self, acceleration):
        """Sets acceleration.

        Args:
            acceleration (float): new acceleration value
        """
        self.set_analog_out(AO.ACCELERATION, acceleration)

    # TODO blockly 12-18测试可用
    def jog_angle(self, joint, direction, speed):
        """Jog joint

        Args:
            joint (Joint): Joint.J1 ~ Joint.J6
            direction (JogDirection): JogDirection.POSITIVE (1) or
                                      JogDirection.NEGATIVE (-1) (1增大，-1减小)
            speed (float): speed percentage (0 ~ 100 %)

        Returns:
            bool: True if jog started successfully, False otherwise
        """
        self.set_robot_move_state(RobotMoveState.JOG_JOINT_STATE, joint, direction)
        self.command_id += 1
        return self._jog_continuous(
            JogMode.JOG_JOINT, joint, direction, speed, self.command_id
        )

    # TODO blockly 12-18测试可用
    def jog_coord(self, axis, direction, speed):
        """Jog axis

        Args:
            axis (Axis): Axis.X ~ Axis.RZ, 对应 x ~ rz
            direction (JogDirection): JogDirection.POSITIVE (1) 增大,
                                      JogDirection.NEGATIVE (-1) 减小
            speed (float): speed percentage (1 ~ 100 %)

        Returns:
            bool: True if jog started successfully, False otherwise
        """
        self.set_robot_move_state(RobotMoveState.JOG_AXIS_STATE, axis, direction)
        self.command_id += 1
        return self._jog_continuous(
            JogMode.JOG_TELEOP, axis, direction, speed, self.command_id
        )

    def _jog_continuous(self, jog_mode, joint_or_axis, direction, speed, jog_id):
        """Start axis or joint jog.

        Args:
            jog_mode (JogMode): jog mode - axis (JogMode.JOG_TELEOP) or joint (JogMode.JOG_JOINT)
            joint_or_axis (Joint | Axis): axis or joint
            direction (JogDirection): direction of movement (1 or -1)
            speed (float): speed of movement (0 ~ 100 %)
            jog_id (int): command_id for this jog

        Returns:
            bool: True if jog started successfully, False otherwise
        """
        if not self.set_jog_mode(jog_mode):
            return False
        self.s.poll()
        if self.s.task_state != elerob.STATE_ON:
            return False
        if (
            (jog_mode == JogMode.JOG_JOINT)
            and (self.s.motion_mode == elerob.TRAJ_MODE_TELEOP)
        ) or (
            (jog_mode == JogMode.JOG_TELEOP)
            and (self.s.motion_mode != elerob.TRAJ_MODE_TELEOP)
        ):
            return False
        if (jog_mode == JogMode.JOG_JOINT) and (
            joint_or_axis.value < 0 or joint_or_axis.value >= MAX_JOINTS
        ):
            return False
        if (jog_mode == JogMode.JOG_TELEOP) and (joint_or_axis.value < 0):
            return False
        if jog_id != self.command_id:
            print("_jog_continuous cancelled: some delay: jog_id != command_id")
            return False
        self.c.jog(
            elerob.JOG_CONTINUOUS,
            jog_mode.value,
            joint_or_axis.value,
            direction.value * speed,
        )
        return True

    def jog_increment_angle(self, joint, increment, speed):
        """Move specified joint by given increment with speed.

        Args:
            joint (Joint): joint
            increment (float): angle
            speed (float): speed percentage (0 ~ 100 %)

        Returns:
            bool: True if jog successfully started, False otherwise
        """
        return self._jog_increment(JogMode.JOG_JOINT, joint, increment, speed)

    def jog_increment_coord(self, axis, increment, speed):
        """Move specified axis by given increment value with speed.

        Args:
            axis (Axis): axis
            increment (float): increment
            speed (float): speed percentage % (0 ~ 100)

        Returns:
            bool: True if jog successfully started, False otherwise
        """
        return self._jog_increment(JogMode.JOG_TELEOP, axis, increment, speed)

    # TODO blockly 12.18测试可用
    def _jog_increment(self, jog_mode, joint_or_axis, incr, speed):
        """Move joint or axis by specified value.

        Args:
            jog_mode (JogMode): move by axis(0) or joint(1)
            joint_or_axis (Joint | Axis): axis(0~5) or joint(0~5)
            incr (float): distance or angle to move for
            speed (float): speed of movement (0 ~ 100 %)

        Returns:
            bool: True if jog started successfully, False otherwise
        """
        if not self.set_jog_mode(jog_mode):
            return False
        self.s.poll()
        if self.s.task_state != elerob.STATE_ON:
            return False
        if (
            (jog_mode == JogMode.JOG_JOINT)
            and (self.s.motion_mode == elerob.TRAJ_MODE_TELEOP)
        ) or (
            (jog_mode == JogMode.JOG_TELEOP)
            and (self.s.motion_mode != elerob.TRAJ_MODE_TELEOP)
        ):
            return False
        if (jog_mode == JogMode.JOG_JOINT) and (
            joint_or_axis.value < 0 or joint_or_axis.value >= MAX_JOINTS
        ):
            return False
        if (jog_mode == JogMode.JOG_TELEOP) and (joint_or_axis.value < 0):
            return False
        direction = 1 if incr >= 0 else -1
        self.c.jog(
            elerob.JOG_INCREMENT,
            jog_mode.value,
            joint_or_axis.value,
            speed * direction,
            math.fabs(incr),
        )
        return True

    def jog_absolute_angle(self, joint, position, speed):
        """Jog given joint to the specified position with passed speed.

        Args:
            joint (Joint): joint
            position (float): position
            speed (float): speed percentage (0 ~ 100 %)

        Returns:
            bool: True if jog started successfully, False otherwise
        """
        return self._jog_absolute(joint, JogMode.JOG_JOINT, position, speed)

    def jog_absolute_coord(self, axis, position, speed):
        """Jog given axis to the specified position with passed speed.

        Args:
            axis (Axis): axis
            position (float): position
            speed (float): speed percentage (0 ~ 100 %)

        Returns:
            bool: True if jog started successfully, False otherwise
        """
        return self._jog_absolute(axis, JogMode.JOG_TELEOP, position, speed)

    def _jog_absolute(self, joint_or_axis, jog_mode, pos, speed):
        """Jog joint or axis to specified position.

        Args:
            joint_or_axis (Joint | Axis): joint or axis
            jog_mode (JogMode): JogMode.JOG_JOINT or JogMode.JOG_TELEOP
            pos (float): position
            speed (float): speed percentage (0 ~ 100 %)

        Returns:
            bool: True if jog started successfully, False otherwise
        """
        if not self.set_jog_mode(jog_mode):
            return False
        self.s.poll()
        if self.s.task_state != elerob.STATE_ON:
            return False
        if (
            (jog_mode == JogMode.JOG_JOINT)
            and (self.s.motion_mode == elerob.TRAJ_MODE_TELEOP)
        ) or (
            (jog_mode == JogMode.JOG_TELEOP)
            and (self.s.motion_mode != elerob.TRAJ_MODE_TELEOP)
        ):
            return False
        if (jog_mode == JogMode.JOG_JOINT) and (
            joint_or_axis.value < 0 or joint_or_axis.value >= MAX_JOINTS
        ):
            return False
        if (jog_mode == JogMode.JOG_TELEOP) and (joint_or_axis.value < 0):
            return False
        if jog_mode == JogMode.JOG_JOINT:
            self.set_angle(joint_or_axis, pos, speed)
            return True
        elif jog_mode == JogMode.JOG_TELEOP:
            self.set_coord(joint_or_axis, pos, speed)
            return True
        else:
            print("Jog Absolute: Wrong Jog Mode.")
            return False

    # TODO blockly 12.18测试可用
    def jog_stop(self, jog_mode, joint_or_axis):
        """Stop specified jog

        Args:
            jog_mode (JogMode): JogMode.JOG_TELEOP (axis (0)) or
                                JogMode.JOG_JOINT (joint (1))
            joint_or_axis (Joint | Axis): Joint.J1 ~ Joint.J6 or Axis.X ~ Axis.RZ

        Returns:
            bool: True if jog stopped successfully, False otherwise
        """
        if (jog_mode == JogMode.JOG_JOINT) and (
            joint_or_axis.value < 0 or joint_or_axis.value >= MAX_JOINTS
        ):
            return False
        if (jog_mode == JogMode.JOG_TELEOP) and (joint_or_axis.value < 0):
            return False
        self.c.jog(elerob.JOG_STOP, jog_mode.value, joint_or_axis.value)
        return True

    def jog_stop_all(self):
        """Stops any jogs and set angles or set coords.

        Returns:
            bool: always returns True
        """
        for j in range(Joint.J6.value):
            self.jog_stop(JogMode.JOG_JOINT, Joint(j))
        for a in range(Axis.RZ.value):
            self.jog_stop(JogMode.JOG_TELEOP, Axis(a))
        self.task_stop()
        return True

    def is_task_idle(self):
        """Returns True if program is not running or finished.

        Returns:
            bool: True if program is not running or finished, False otherwise.
        """
        self.s.poll()
        return self.s.exec_state <= elerob.EXEC_DONE and not self.is_program_running()

    # def start_3d_mouse(self, enable):
    #     """Starts movement my space nav mouse.

    #     Args:
    #         enable (bool): start if True, stop if False
    #     """
    #     raise NotImplementedError

    def set_robot_move_state(self, new_robot_state, joint_or_axis, direction):
        """Sets robot move state.

        Args:
            new_robot_state (RobotMoveState): any value from RobotMoveState enum
            joint_or_axis (Joint | Axis): joint or axis
            direction (JogDirection): direction from JogDirection enum
        """
        if new_robot_state == self.robot_state:
            return

        if new_robot_state == RobotMoveState.JOG_JOINT_STATE:
            self.command_id += 1
            self._jog_continuous(
                JogMode.JOG_JOINT, joint_or_axis, direction, 1, self.command_id
            )
            time.sleep(0.1)
        elif new_robot_state == RobotMoveState.JOG_AXIS_STATE:
            self.command_id += 1
            self._jog_continuous(
                JogMode.JOG_TELEOP, joint_or_axis, direction, 1, self.command_id
            )
            time.sleep(0.1)
        elif new_robot_state == RobotMoveState.MOVE_AXIS_STATE:
            self.send_mdi("G92.2")
            self.send_mdi("G01F2000" + self.coords_to_gcode(self.get_coords()))
        elif new_robot_state == RobotMoveState.MOVE_JOINT_STATE:
            self.send_mdi("G92.2")
            self.send_mdi("G38.3F1000" + self.angles_to_gcode(self.get_angles()))
        elif new_robot_state == RobotMoveState.RUN_PROGRAM_STATE:
            self.send_mdi("G92.2")
        self.robot_state = new_robot_state

    def update(self):
        """Updates robot data. Get current robot state. Run before any
        get function as needed.
        """
        self.s.poll()

    def set_state(self, s):
        """Change robot state to one of:
            elerob.STATE_ESTOP (1),
            elerob.STATE_ESTOP_RESET (2),
            elerob.STATE_OFF (3),
            elerob.STATE_ON (4)

        Args:
            s (str): robot state, can be "STATE_ON", "STATE_OFF", "STATE_ESTOP",
                    "STATE_ESTOP_RESET".
        """
        if "STATE_ON" == s:
            # self.c.state( elerob.STATE_ESTOP_RESET)
            # time.sleep(0.01)
            self.c.state(elerob.STATE_ON)
        elif "STATE_OFF" == s:
            self.c.state(elerob.STATE_OFF)
        elif "STATE_ESTOP" == s:
            self.c.state(elerob.STATE_ESTOP)
        elif "STATE_ESTOP_RESET" == s:
            self.c.state(elerob.STATE_ESTOP_RESET)

    def set_feedrate(self, new_val):
        """Set robot speed in percents (feedrate).

        Args:
            new_val (float): speed value in percents, 0 ~ 100.
        """
        try:
            value = float(new_val)
        except ValueError:
            return
        value = value / 100.0
        if value < 0.0:
            value = 0.0
        elif value >= 1.0:
            value = 1.0
        self.c.feedrate(value)

    def send_home(self, axis_num=-1):
        """Home axis or all axes (-1 means home all axes).
        Home means sets current joint or axis value as home position.

        Args:
            axis_num (int, optional): Axis to home. -1 means home all axes.
                                     Defaults to -1.
        """
        self.c.home(axis_num)

    def is_all_homed(self):
        """Checks if all axes are homed (in home position).

        Returns:
            bool: True if all axes are homed, False otherwise.
        """
        is_homed = True
        self.s.poll()
        for i, h in enumerate(self.s.homed):
            if self.s.axis_mask & (1 << i):
                is_homed = is_homed and h
        return is_homed

    def get_axis_limits(self):
        """Returns axis limits.

        Returns:
            list[int]: axes limits.
        """
        self.s.poll()
        limits = []
        for i, limit in enumerate(self.s.limit):
            if self.s.axis_mask & (1 << i):
                limits.append(limit)
        return limits

    def ensure_mdi(self):
        """Sets mode to MDI."""
        if not self.manual_ok():
            return
        self.ensure_mode(TaskMode.MDI)

    def send_mdi(self, gcode_command):
        """Send G-Code command to robot.

        Args:
            gcode_command (str): G-code command

        Returns:
            bool: True if command sent successfully, False otherwise
        """
        self.s.poll()
        if self.s.task_mode != elerob.MODE_MDI:
            self.set_mode(TaskMode.MDI)
        self.s.poll()
        if self.s.task_mode != elerob.MODE_MDI:
            print("send_mdi error: task_mode is not MODE_MDI")
            return False
        logging.debug(gcode_command)
        self.c.mdi(gcode_command)
        return True

    def send_mdi_wait(self, gcode_command):
        """Send command and wait for it to complete

        Args:
            program (str): G-code command
        """
        self.c.mdi(gcode_command)
        self.c.wait_complete()

    # # TODO 不明白什么意思
    # def set_optional_stop(self, on=0):
    #     self.c.set_optional_stop(on)
    #     self.c.wait_complete()

    # # TODO 不明白什么意思
    # def set_block_delete(self, on=0):
    #     self.c.set_block_delete(on)
    #     self.c.wait_complete()

    def is_program_running(self, do_poll=True):
        """Checks if robot is executing a program.

        Args:
            do_poll (bool, optional): if need to update robot state. Defaults to True.

        Returns:
            bool: True if robot is executing a program, False otherwise
        """
        if do_poll:
            self.s.poll()
        return (
            self.s.task_mode == elerob.MODE_AUTO
            and self.s.interp_state != elerob.INTERP_IDLE
        )

    # TODO 不明白什么意思
    def manual_ok(self, do_poll=True):
        if do_poll:
            self.s.poll()
        if self.s.task_state != elerob.STATE_ON:
            return False
        return self.s.interp_state == elerob.INTERP_IDLE

    def ensure_mode(self, m, *p):
        """If elerob is not already in one of the model given, switch it to
        the first mode: elerob.MODE_MDI, elerob.MODE_MANUAL, elerob.MODE_AUTO.

        Args:
            m (TaskMode) : TaskMode or "STEP_MODE"

        Returns:
            bool: True if mode is m or in p
        """
        if "STEP_MODE" == m:
            m = TaskMode.MDI
        self.s.poll()
        if self.s.task_mode == m.value or self.s.task_mode in p:
            return True
        if self.is_program_running(do_poll=False):
            return False
        return self.set_mode(m)

    def program_open(self, program_file_path):
        """Opens g-code file. Only absolute file paths are supported.

        Args:
            program_file_path (str): absolute path to program file (.ngc)
        """
        self.c.program_open(program_file_path)

    def program_run(self, start_line):
        """Run g-code file starting from given line.
        从给定行开始运行g-code文件

        Args:
            start_line (int): start line (first line is 0)

        Example:
            elerob.program_run(elerob.AUTO_RUN, 0)

        Returns:
            bool: True if program run started successfully, False otherwise
        """
        self.set_robot_move_state(RobotMoveState.RUN_PROGRAM_STATE, 0, 0)
        self.s.poll()
        if len(self.s.file) == 0:
            return False
        self.set_mode(TaskMode.AUTO)

        self.c.auto(elerob.AUTO_RUN, start_line)
        self.c.wait_complete()
        return True

    def get_current_line(self):
        """Returns current executing line of g-code file.

        Returns:
            int: current executing line
        """
        self.s.poll()
        if self.s.task_mode != elerob.MODE_AUTO or self.s.interp_state not in (
            elerob.INTERP_READING,
            elerob.INTERP_WAITING,
        ):
            return -1
        self.ensure_mode(TaskMode.AUTO)
        return int(self.s.current_line)

    def get_current_gcodes(self):
        """Get current execution G-code.

        Returns active G-codes for each modal group.

        Returns:
            tuple of integers: active G-codes
        """
        self.s.poll()
        return self.s.gcodes

    def set_max_velocity(self, velocity):
        """Sets maximum velocity.

        Args:
            velocity (float): max velocity to set, percentage, 0 ~ 100.
        """
        self.c.maxvel(float(velocity) / 100.0)

    def get_read_line(self):
        """Get G-Code interpreter read line.

        Returns:
            int: line interpreter is currently reading
        """
        self.s.poll()
        if self.s.task_mode != elerob.MODE_AUTO or self.s.interp_state not in (
            elerob.INTERP_READING,
            elerob.INTERP_WAITING,
        ):
            return -1
        self.ensure_mode(TaskMode.AUTO)
        return self.s.read_line

    def prog_exec_status(self):
        """Returns G-Code interpreter's current state.
        返回解释器当前状态

        Returns:
            int: Interpreter state: INTERP_IDLE (1),
                                    INTERP_READING (2),
                                    INTERP_PAUSED (3),
                                    INTERP_WAITING (4)
        """
        self.s.poll()
        return self.s.interp_state

    def elerob_status(self):
        """Returns current task state.

        Returns:
            int: Current task state, one of:
                    elerob.STATE_ESTOP (1),
                    elerob.STATE_ESTOP_RESET (2),
                    elerob.STATE_OFF (3),
                    elerob.STATE_ON (4)
        """
        self.s.poll()
        return self.s.task_state

    def optional_stop_resume(self):
        """Resume program after optional stop."""
        self.s.poll()
        if not self.s.paused:
            return
        if self.s.task_mode not in (elerob.MODE_AUTO, elerob.MODE_MDI):
            return
        self.ensure_mode(TaskMode.AUTO, TaskMode.MDI)
        self.c.auto(elerob.AUTO_RESUME)

    def program_pause(self):
        """Pause program."""
        self.s.poll()
        if self.s.task_mode != elerob.MODE_AUTO or self.s.interp_state not in (
            elerob.INTERP_READING,
            elerob.INTERP_WAITING,
        ):
            return
        self.ensure_mode(TaskMode.AUTO)
        self.c.auto(elerob.AUTO_PAUSE)

    def program_resume(self):
        """Resume program after pause."""
        self.s.poll()
        if self.s.task_mode not in (elerob.MODE_AUTO, elerob.MODE_MDI):
            return
        self.ensure_mode(TaskMode.AUTO, TaskMode.MDI)
        self.s.poll()
        if self.s.paused:
            self.c.auto(elerob.AUTO_RESUME)

        elif self.s.interp_state != elerob.INTERP_IDLE:
            # self.c.auto(elerob.AUTO_PAUSE)
            pass

    def task_stop(self):
        """Stop robot and wait for stop complete."""
        self.c.abort()
        self.c.wait_complete()
        if not self.is_task_idle():
            self.c.abort()
            self.c.wait_complete()
            self.s.poll()
            print(
                f"Warning: Failed Task abort: task_mode={self.s.task_mode}, exec_status={self.s.exec_state}, interp_state={self.s.interp_state}"
            )

    def task_stop_async(self):
        """Stop robot without waiting for stop to complete."""
        self.c.abort()

    def get_digital_in(self, pin_number):
        """Returns digital input pin value. One of DI Enum.

        Args:
            pin_number (DI): pin number

        Returns:
            int: pin value (0 or 1)
        """
        return int(self.g["digital-in-" + str(pin_number.value).zfill(2)])

    def get_digital_out(self, pin_number):
        """Returns digital output pin value. One of DO Enum.

        Args:
            pin_number (DO): pin number

        Returns:
            int: pin value (0 or 1)
        """
        return int(self.g["digital-out-" + str(pin_number.value).zfill(2)])

    def set_digital_out(self, pin_number, pin_value):
        """Sets digital output pin value. One of DO Enum.

        Args:
            pin_number (DO): pin number
            pin_value (int): pin value (0 or 1)
        """
        self.g["digital-out-" + str(pin_number.value).zfill(2)] = pin_value

    def get_analog_in(self, pin_number):
        """Returns analog input pin value. One of AI Enum.

        Args:
            pin_number (AI): pin number

        Returns:
            float: pin value
        """
        return float(self.g["analog-in-" + str(pin_number.value).zfill(2)])

    def get_analog_out(self, pin_number):
        """Returns analog output pin value. One of AO Enum.

        Args:
            pin_number (AO): pin number

        Returns:
            float: pin value
        """
        return float(self.g["analog-out-" + str(pin_number.value).zfill(2)])

    def set_analog_out(self, pin_number, pin_value):
        """Sets analog output pin value. One of AO Enum.

        Args:
            pin_number (AO): pin number
            pin_value (float): pin value
        """
        self.g["analog-out-" + str(pin_number.value).zfill(2)] = pin_value

    def get_axis_velocity(self, axis):
        """Return axis velocity.
        获取单关节速度

        Args:
            axis (Axis): axis number

        Returns:
            float: axis velocity or -1.0 if error
        """
        if 0 <= axis.value <= 6:
            self.s.poll()
            return self.s.axis[axis.value]["velocity"]
        return -1.0

    def get_current_command(self):
        """Returns current executing command.

        Returns:
            str: current executing command
        """
        self.s.poll()
        return self.s.command

    # def get_cmd_pos(self):
    #     """Returns trajectory position.
    #     返回轨迹位置

    #     Returns:
    #         str: string of list of values
    #     """
    #     self.s.poll()
    #     return str(
    #         [
    #             "%5.3f" % self.s.position[0],
    #             "%5.3f" % self.s.position[1],
    #             "%5.3f" % self.s.position[2],
    #             "%5.3f" % self.s.position[3],
    #             "%5.3f" % self.s.position[4],
    #             "%5.3f" % self.s.position[5],
    #         ]
    #     )

    # def get_actl_pos(self):
    #     """Returns current trajectory position.

    #     Returns:
    #         str: string of list of values
    #     """
    #     self.s.poll()
    #     return str(
    #         [
    #             "%5.3f" % self.s.actual_position[0],
    #             "%5.3f" % self.s.actual_position[1],
    #             "%5.3f" % self.s.actual_position[2],
    #             "%5.3f" % self.s.actual_position[3],
    #             "%5.3f" % self.s.actual_position[4],
    #             "%5.3f" % self.s.actual_position[5],
    #         ]
    #     )

    # def get_cmd_joint(self):
    #     """Returns desired joint positions

    #     Returns:
    #         str: string of list of values
    #     """
    #     self.s.poll()
    #     return str(
    #         [
    #             "%5.3f" % self.s.joint_position[0],
    #             "%5.3f" % self.s.joint_position[1],
    #             "%5.3f" % self.s.joint_position[2],
    #             "%5.3f" % self.s.joint_position[3],
    #             "%5.3f" % self.s.joint_position[4],
    #             "%5.3f" % self.s.joint_position[5],
    #         ]
    #     )

    # def get_actl_joint(self):
    #     """Returns actual joint positions.

    #     Returns:
    #         str: string of list of values
    #     """
    #     self.s.poll()
    #     return str(
    #         [
    #             "%5.3f" % self.s.joint_actual_position[0],
    #             "%5.3f" % self.s.joint_actual_position[1],
    #             "%5.3f" % self.s.joint_actual_position[2],
    #             "%5.3f" % self.s.joint_actual_position[3],
    #             "%5.3f" % self.s.joint_actual_position[4],
    #             "%5.3f" % self.s.joint_actual_position[5],
    #         ]
    #     )

    def get_cmd_pos_float(self):
        """Returns trajectory position.

        Returns:
            list[float]: list of strings of values
        """
        self.s.poll()
        return [
            round(self.s.position[0], 3),
            round(self.s.position[1], 3),
            round(self.s.position[2], 3),
            round(self.s.position[3], 3),
            round(self.s.position[4], 3),
            round(self.s.position[5], 3),
        ]

    def get_actl_pos_float(self):
        """Returns current trajectory position.

        Returns:
            list[float]: list of strings of values
        """
        self.s.poll()
        return [
            round(self.s.actual_position[0], 3),
            round(self.s.actual_position[1], 3),
            round(self.s.actual_position[2], 3),
            round(self.s.actual_position[3], 3),
            round(self.s.actual_position[4], 3),
            round(self.s.actual_position[5], 3),
        ]

    def get_cmd_joint_float(self):
        """Returns desired joint positions.

        Returns:
            list[float]: list of string of values
        """
        self.s.poll()
        return [
            round(self.s.joint_position[0], 3),
            round(self.s.joint_position[1], 3),
            round(self.s.joint_position[2], 3),
            round(self.s.joint_position[3], 3),
            round(self.s.joint_position[4], 3),
            round(self.s.joint_position[5], 3),
        ]

    def get_actl_joint_float(self):
        """Returns actual joint positions

        Returns:
            list[float]: list of strings of values
        """
        self.s.poll()
        return [
            round(self.s.joint_actual_position[0], 3),
            round(self.s.joint_actual_position[1], 3),
            round(self.s.joint_actual_position[2], 3),
            round(self.s.joint_actual_position[3], 3),
            round(self.s.joint_actual_position[4], 3),
            round(self.s.joint_actual_position[5], 3),
        ]

    ################################
    # get motion status
    ################################
    def get_current_velocity(self):
        """Returns current velocity.

        Returns:
            float: current velocity in units per second
        """
        self.s.poll()
        return self.s.current_vel

    def get_default_velocity(self):
        """Returns default velocity.

        Returns:
            float: default velocity
        """
        self.s.poll()
        return self.s.velocity

    def get_default_acceleration(self):
        """Returns default acceleration

        Returns:
            float: default acceleration
        """
        self.s.poll()
        return self.s.acceleration

    def get_max_velocity(self):
        """Returns maximum velocity.

        Returns:
            float: maximum velocity
        """
        self.s.poll()
        return self.s.max_velocity

    def get_max_acceleration(self):
        """Returns maximum acceleration.

        Returns:
            float: maximum acceleration
        """
        self.s.poll()
        return self.s.max_acceleration

    def get_feedrate(self):
        """Returns current feedrate override, 1.0 = 100%.

        Returns:
            float: current feedrate
        """
        self.s.poll()
        return self.s.feedrate

    def get_motion_enabled(self):
        """State of trajectory planner enabled flag.
        True if robot can move, false otherwise.
        轨迹规划器启用标志的状态。如果机器人可以移动，则为True，否则为False

        Returns:
            bool: enabled flag value
        """
        self.s.poll()
        return self.s.enabled

    # def get_joint_vel_fb(self, _num):
    #     """_summary_

    #     Args:
    #         _num (_type_): _description_

    #     Raises:
    #         NotImplementedError: _description_
    #     """
    #     self.s.poll()
    #     ###return self.s.jvel[num]
    #     raise NotImplementedError

    # def get_joint_torq_fb(self, _num):
    #     """_summary_

    #     Args:
    #         _num (_type_): _description_

    #     Raises:
    #         NotImplementedError: _description_
    #     """
    #     self.s.poll()
    #     ###return self.s.jtorq[num]
    #     raise NotImplementedError

    ################################
    # set cmds
    ################################
    def set_joint_torque_limit(self, joint, torque_limit):
        """Sets joint torque limits

        Arguments:
            joint (Joint): joint
            torque_limit (float): torque limit value
        """
        if joint.value < MAX_JOINTS:
            self.set_analog_out(AO(AO.J1_TORQUE.value + joint.value), torque_limit)

    def set_carte_torque_limit(self, axis, value):
        """Sets cartesian torque limit.

        Args:
            axis (Axis): axis to set torque for
            value (float): torque value
        """
        if axis == Axis.X or axis == Axis.Y:
            self.set_analog_out(AO.XY_AXIS_TORQUE, value)
        elif axis == Axis.Z:
            self.set_analog_out(AO.Z_AXIS_TORQUE, value)

    # def set_joint_torque_en(self, _state):
    #     # self.c.set_jtorq_enable(0,state)
    #     raise NotImplementedError

    # def set_carte_torque_en(self, _state):
    #     # self.c.set_cartetorq_enable(0,state)
    #     raise NotImplementedError

    def set_jog_mode(self, jog_mode):
        """Changes jog mode to jog_mode (angular or linear).
        AKA jog_state_check().

        Args:
            jog_mode (JogMode): linear (JogMode.JOG_TELEOP) or
                                angular (JogMode.JOG_JOINT) jog mode

        Returns:
            bool: True if change state was successful, False otherwise
        """
        self.s.poll()
        if (
            self.s.estop
            or not self.s.enabled
            or (self.s.interp_state != elerob.INTERP_IDLE)
        ):
            return False
        if self.s.task_mode != elerob.MODE_MANUAL:
            self.c.mode(elerob.MODE_MANUAL)
            self.c.wait_complete()
            time.sleep(0.2)
        self.s.poll()
        if jog_mode == JogMode.JOG_JOINT:
            if self.s.motion_mode != elerob.TRAJ_MODE_FREE:
                self.c.teleop_enable(0)
                self.c.wait_complete()
                time.sleep(0.2)
        elif jog_mode == JogMode.JOG_TELEOP:
            if self.s.motion_mode != elerob.TRAJ_MODE_TELEOP:
                self.c.teleop_enable(1)
                self.c.wait_complete()
                time.sleep(0.2)
        else:
            print("Error: set_jog_mode: Unknown JogMode")
            return False
        return True

    # def continuous_jog(self, jogmode, axis, direction):
    #     """Start axis or joint jog.

    #     Args:
    #         jogmode (_type_): jog mode (axis or joint)
    #         axis (_type_): axis or joint
    #         direction (_type_): direction of movement

    #     Returns:
    #         bool: True if successfully started jog, False otherwise
    #     """
    #     if not self.set_jog_mode(jogmode):
    #         return False
    #     if direction == 0:
    #         self.c.jog(elerob.JOG_STOP, jogmode, axis)
    #     else:
    #         # if axis in (3,4,5):
    #         # 	rate = self.angular_jog_velocity
    #         # else:
    #         rate = jog_velocity
    #         self.c.jog(elerob.JOG_CONTINUOUS, jogmode, axis, direction * rate)
    #     return True

    # def incremental_jog(self, jogmode, axis, direction, distance):
    #     """Move joint or axis by specified value.

    #     Args:
    #         jogmode (_type_): move by axis or joint
    #         axis (_type_): axis or joint
    #         direction (_type_): direction of movement
    #         distance (_type_): distance or angle to move for

    #     Returns:
    #         bool: True if jog started successfully, False otherwise
    #     """
    #     if not self.set_jog_mode(jogmode):
    #         return False
    #     if direction == 0:
    #         self.c.jog(elerob.JOG_STOP, jogmode, axis)
    #     else:
    #         # if axis in (3,4,5):
    #         # 	rate = self.angular_jog_velocity
    #         # else:
    #         rate = jog_velocity
    #         self.c.jog(elerob.JOG_INCREMENT, jogmode, axis, direction * rate, distance)
    #     return True

    def coords_to_gcode(self, coords):
        """Returns gcode string to move to given coords

        Args:
            coords (list[float | str]): list of coordinate values

        Returns:
            str: gcode string to move to given coords
        """
        return (
            "X"
            + str(coords[0])
            + "Y"
            + str(coords[1])
            + "Z"
            + str(coords[2])
            + "A"
            + str(coords[3])
            + "B"
            + str(coords[4])
            + "C"
            + str(coords[5])
        )

    def angles_to_gcode(self, angles):
        """Returns gcode string to move to given joint angles

        Args:
            coords (list[float | str]): list of joint angles values

        Returns:
            str: gcode string to move to given joint angles
        """
        return self.coords_to_gcode(angles)

    def float_equal(self, a, b, epsilon=COORDS_EPSILON):
        """_summary_

        Args:
            a (float): _description_
            b (float): _description_
            epsilon (float): _description_

        Returns:
            bool: _description_
        """
        return math.fabs(a - b) < epsilon

    def coords_equal(self, coords_1, coords_2):
        """Checks if specified coords are equal.

        Args:
            coords_1 (list): first coords to compare
            coords_2 (list): second coords to compare

        Returns:
            bool: True if coords are equal, False otherwise.
        """
        return (
            self.float_equal(coords_1[Axis.X.value], coords_2[Axis.X.value])
            and self.float_equal(coords_1[Axis.Y.value], coords_2[Axis.Y.value])
            and self.float_equal(coords_1[Axis.Z.value], coords_2[Axis.Z.value])
            and self.float_equal(coords_1[Axis.RX.value], coords_2[Axis.RX.value])
            and self.float_equal(coords_1[Axis.RY.value], coords_2[Axis.RY.value])
            and self.float_equal(coords_1[Axis.RZ.value], coords_2[Axis.RZ.value])
        )

    def angles_equal(self, angles_1, angles_2):
        """Checks if specified angles are equal.

        Args:
            angles_1 (list): first angles to compare
            angles_2 (list): second angles to compare

        Returns:
            bool: True if angles are equal, False otherwise.
        """
        return (
            self.float_equal(angles_1[Axis.X.value], angles_2[Axis.X.value])
            and self.float_equal(angles_1[Axis.Y.value], angles_2[Axis.Y.value])
            and self.float_equal(angles_1[Axis.Z.value], angles_2[Axis.Z.value])
            and self.float_equal(angles_1[Axis.RX.value], angles_2[Axis.RX.value])
            and self.float_equal(angles_1[Axis.RY.value], angles_2[Axis.RY.value])
            and self.float_equal(angles_1[Axis.RZ.value], angles_2[Axis.RZ.value])
        )
