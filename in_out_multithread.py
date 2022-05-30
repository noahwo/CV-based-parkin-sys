 
from nis import cat
from time import sleep
import time
import RPi.GPIO as GPIO
import hyperlpr
import cv2
import re
from matplotlib import pyplot as plt
import threading
import sqlite3

"""
PS: vcc and gnd not need anymore cuz of the external power supply. One gnd needed.
# a 外 b 内
入口 sersor_a: signal: 7 (bcm: 4)
入口 sersor_b: signal: 11 (bcm: 17)
入口 servo1:   signal: 12 (bcm: 18)
# c 外 d 内
出口 sersor_c: signal: 15 (bcm: 22)
出口 sersor_d: signal: 13 (bcm: 27)
出口 servo2:   signal: 16 (bcn: 23)

servo: 红色电压  粽色地线  橙色信号
高电平—— 1, 低电平—— 0
顺时针, 距离加；
逆时针, 距离减
"""
# plate_pattern=re.compile("/^([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[a-zA-Z](([DF]((?![IO])[a-zA-Z0-9](?![IO]))[0-9]{4})|([0-9]{5}[DF]))|[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1})$/")
plate_pattern = "[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[a-zA-Z](([DF]((?![IO])[a-zA-Z0-9](?![IO]))[0-9]{4})|([0-9]{5}[DF]))|[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}"

GPIO.setmode(GPIO.BCM)

sensor_a = 4
sensor_b = 17
servo1 = 18
sensor_c = 22
sensor_d = 27
servo2 = 23

for sensor in [sensor_a, sensor_b, sensor_c, sensor_d]:
    GPIO.setup(sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(servo1, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)

servo_pwm1 = GPIO.PWM(servo1, 50)  # 50HZ
servo_pwm2 = GPIO.PWM(servo2, 50)  # 50HZ


gate_args1 = [sensor_a, sensor_b, servo1, servo_pwm1, 0, "in"]  # 0 is camera id
gate_args2 = [sensor_c, sensor_d, servo2, servo_pwm2, 2, "out"]


from socket import *

while True:

    # 1.创建套接字
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    # 2.准备连接服务器，建立连接
    serve_ip = "192.168.63.216"
    serve_port = 1989  # 端口，比如8000
    try:
        tcp_socket.connect((serve_ip, serve_port))
        break
    except Exception as e:
        print("Failed to connect to server by error: " + str(e))
        time.sleep(5)


def main():
    # existance_init()

    # threadLock = threading.Lock()
    # threads = []
    # thread_entrance=gateThread("entrance-thread",gate_args1)
    # thread_extrance=gateThread("extrance-thread",gate_args2)

    thread_entrance = threading.Thread(target=run_gate, args=(gate_args1,))
    thread_extrance = threading.Thread(target=run_gate, args=(gate_args2,))
    thread_entrance.start()
    thread_extrance.start()
    # for t in threads:
    #     t.join()


def run_gate(gate_args):
    sensor1 = gate_args[0]
    sensor2 = gate_args[1]
    servo = gate_args[2]
    servo_pwm = gate_args[3]
    cam_id = gate_args[4]

    if gate_args[5] == "in":
        action = "驶入"
    else:
        action = "离开"

    servo_pwm.start(0)

    print("cam_id: " + str(cam_id))

    try:
        while True:
            if GPIO.input(sensor1) == 0:
                cap = cv2.VideoCapture(cam_id)

                if cap.isOpened():
                    ret, frame = cap.read()
                    cap.release()
                    if ret:  # If video fame is captured.
                        try:
                            # with Supress_print():
                            plate_ = hyperlpr.HyperLPR_plate_recognition(frame, 0)[0][0]
                            if plate_:  # If the plate is recognized to a string
                                if (
                                    re.match(plate_pattern, plate_) is not None
                                ):  # If the plate string is legal
                                    print("Plate: " + plate_)
                                    plate_ = str(plate_)

                                    # Check if the plate already exists, and do the corresponding task.
                                    if gate_args[5] == "in":
                                        existance = come_check_plate_existance(plate_)
                                        if existance is True:
                                            print(
                                                "The car " + plate_ + " already exists!"
                                            )
                                            continue
                                    else:
                                        existance = leave_check_plate_existance(plate_)
                                        if existance is False:
                                            print(
                                                "The car " + plate_ + " does not exist!"
                                            )
                                            continue

                                    #  Send message to server and get the returned message.
                                    send_msg = "车辆 \'"  + plate_ + "\' " + action + "."
                                    time_note = (
                                        " - "
                                        + time.strftime(
                                            "%Y-%m-%d %H:%M:%S",
                                            time.localtime(time.time()),
                                        )
                                        + "\n"
                                    )

                                    print(send_msg + time_note)

                                    tcp_socket.send(
                                        (send_msg + time_note).encode("gbk")
                                    )

                                    from_server_msg = tcp_socket.recv(4096)

                                    print(
                                        "From server: " + from_server_msg.decode("gbk")
                                    )

                                    # Operate the hardware to open the boom gate
                                    open(sensor2, servo_pwm)
                                else:
                                    print(
                                        "Invalid format of recognized string: " + plate_
                                    )
                            else:
                                print("Plate does not exist or not recognized!")
                                continue
                        except:
                            continue
                        # print(plate_)
                    else:
                        print("No video frame captured!")
                        continue
                else:
                    print("Camera " + str(cam_id) + " is not working!")
                if cap:
                    cap.release()
    except KeyboardInterrupt:
        print("Stopped by keyboard interrupt!")
    except BrokenPipeError:
        print("Stopped by client!")
    except Exception as e:
        print("Stopped by error: " + str(e))
    finally:
        servo_pwm.stop()
        GPIO.cleanup()
        tcp_socket.close()
        # if cap:
        #     cap.release()


def rotate(angle, servo_pwm):  # 定义函数，输入角度，即可自动转向，0-180度，如0、90、180
    servo_pwm.ChangeDutyCycle(2.5 + angle / 360 * 20)
    sleep(0.1)
    servo_pwm.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
    sleep(0.1)


def open(sensor2, servo_pwm):
    rotate(90, servo_pwm)
    sleep(2)
    while GPIO.input(sensor2) == 0:
        # print("sensor2 activated!")
        sleep(1)
    sleep(1)
    rotate(0, servo_pwm)
    sleep(0.5)


def existance_init():
    conn = sqlite3.connect("existance.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS EXISTANCE")
    c.execute(
        """CREATE TABLE EXISTANCE
            (PLATE CHAR(50) PRIMARY KEY    NOT NULL);
            """
    )
    print("数据表创建成功")
    conn.commit()
    conn.close()


def existance_select(keyword):

    conn = sqlite3.connect("existance.db")
    c = conn.cursor()
    cursor = c.execute("SELECT * from EXISTANCE where plate='" + keyword + "'")
    i = 0
    for row in cursor:
        if row is not None:
            i = i + 1
    if i == 0:
        # print("No " + keyword + " found in parking lot.")
        existance = False
    else:
        existance = True
    conn.close()
    return existance


def existance_insert(keyword):
    conn = sqlite3.connect("existance.db")
    c = conn.cursor()
    c.execute("INSERT INTO EXISTANCE (PLATE) VALUES ('" + keyword + "')")
    conn.commit()
    conn.close()


def existance_delete(keyword):
    conn = sqlite3.connect("existance.db")
    c = conn.cursor()
    c.execute("DELETE FROM EXISTANCE WHERE PLATE ='" + keyword + "'")
    conn.commit()
    conn.close()


def come_check_plate_existance(plate):
    existance = existance_select(plate)
    if existance == True:
        print("Sorry, the car " + plate + " is already found in the parking lot.")
    else:
        existance_insert(plate)
        print("The plate " + plate + " is entering.")

    return existance


def leave_check_plate_existance(plate):
    existance = existance_select(plate)
    if existance == True:
        existance_delete(plate)
        print("The plate " + plate + " is leaving.")
    else:
        print("Sorry, the car " + plate + " is not found in the parking lot.")
    return existance


if __name__ == "__main__":

    main()
