## db접근, 기능구현
import pymysql

# # GPIO연결
# import RPi.GPIO as GPIO
# import time
# import threading

# #OLED관련 import
# import board
# import busio
# import adafruit_ssd1306
# from PIL import Image, ImageDraw, ImageFont

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)


# # 차단바 올렸다 내리는 함수
# ##90도(10.5) : 차단바 close
# ##0도(5.5) : 차단바 open
# def move_motor():
#     motor_pin = 26
#     GPIO.setup(motor_pin, GPIO.OUT)
#     p = GPIO.PWM(motor_pin, 50)
#     # 차단바 올림
#     p.start(0)
#     p.ChangeDutyCycle(10.5)
#     time.sleep(1)
#     # 차단바 내림
#     p.ChangeDutyCycle(5.5)
#     time.sleep(0.5)
#     p.stop()


# ##led제어
# def led_result():
#     # 23초록, 24노랑, 25빨강
#     # 노란색은 장애인 전용 조회하여 자리가 있으면 불이 들어오고 없으면 꺼짐
#     led_pins = [23, 24, 25]
#     GPIO.setup(led_pins, GPIO.OUT)
#     carzone_red = led_zone()
#     carzone_all = info_carzone()
#     # 모든 자리 사용중(장애인전용 차량자리 제외), 자리없음
#     if len(carzone_red) == 6:
#         GPIO.output(23, GPIO.LOW)
#         GPIO.output(25, GPIO.HIGH)
#     # 자리 있음
#     else:
#         GPIO.output(23, GPIO.HIGH)
#         GPIO.output(25, GPIO.LOW)
#     #####장애인전용자리 'car7' -> led 노란색 on (자리 있음)
#     if "car7" not in carzone_all:
#         GPIO.output(24, GPIO.HIGH)
#     else:
#         GPIO.output(24, GPIO.LOW)


# db연결
def connect_db():
    try:
        connect_db = pymysql.connect(
            user="hp",
            password="1234",
            host="127.0.0.1",
            db="mobledb",
            charset="utf8",
        )
        return connect_db
    except pymysql.Error as e:
        print("error : " + str(e))
        return None


# # car info : 차량번호가 저장되어있는 table
# # parkingzone : 주차자리 div 이름이 저장되어 있는 table
# # 주차등록이 되어있는 차량수 return 멤버에서 15까지만 저장
# def info_len():
#     sensor_db = connect_db()
#     cursor = sensor_db.cursor()
#     sql = "SELECT count(*) FROM car_info"
#     cursor.execute(sql)
#     len = cursor.fetchall()
#     sensor_db.close()
#     return len[0][0]


# # 등록되어있는 차넘버 리스트 리턴
# def info_car_list():
#     sensor_db = connect_db()
#     cursor = sensor_db.cursor()
#     sql = "SELECT * FROM car_info"
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     car_list = []
#     handi_list = []
#     # 0번은 차량번호, 1번은 핸디여부
#     for car_no in data:
#         car_list.append(car_no[0])
#         handi_list.append(car_no[1])
#     sensor_db.close()
#     return car_list, handi_list


# # 현재 사용중인 주차자리 표시 및 html에 전달
# # 로딩 될때 사용
# def info_carzone():
#     list_park_no = []
#     sensor_db = connect_db()
#     cursor = sensor_db.cursor()
#     sql = "SELECT pzone FROM parkingzone"  # sql 명령문
#     cursor.execute(sql)  # sql 실행
#     park = cursor.fetchall()
#     for i in range(len(park)):
#         list_park_no.append(park[i][0])
#     sensor_db.close()
#     return list_park_no


# # carzone 7제외 사용중인 주차자리 수 리턴 -> led 초록 빨강제어
# def led_zone():
#     list_park_no = []
#     sensor_db = connect_db()
#     cursor = sensor_db.cursor()
#     sql = "SELECT pzone FROM parkingzone where pzone not like 'car7'"  # sql 명령문
#     cursor.execute(sql)  # sql 실행
#     park = cursor.fetchall()
#     for i in range(len(park)):
#         list_park_no.append(park[i][0])
#     sensor_db.close()
#     return list_park_no


# def add_car_no(car_no, bcheck):  # 차 넘버 sql에 저장
#     sensor_db = connect_db()
#     cursor = sensor_db.cursor()
#     sql = "insert into car_info(car_no, handi) values('%s', '%s')" % (car_no, bcheck)
#     cursor.execute(sql)
#     sensor_db.commit()
#     sensor_db.close()


# def delete_car_no(car_no):  # 차 넘버 sql에서 지우기
#     sensor_db = connect_db()
#     cursor = sensor_db.cursor()
#     sql = "delete from car_info where car_no = '%s'" % car_no
#     cursor.execute(sql)
#     sensor_db.commit()
#     sensor_db.close()


# def add_zone(park_zone):  # 사용할 주차라인을 db에 추가
#     sensor_db = connect_db()
#     cursor = sensor_db.cursor()
#     sql = "insert into parkingzone(pzone) values('%s')" % park_zone
#     try:
#         cursor.execute(sql)
#         sensor_db.commit()
#     except Exception as e:
#         sensor_db.rollback()
#         print("error : ", str(e))
#     finally:
#         sensor_db.close()


# def delete_zone(park_zone):  # 빠져나간 주차라인을 db에서 삭제
#     sensor_db = connect_db()
#     cursor = sensor_db.cursor()
#     sql = "delete from parkingzone where pzone='%s'" % park_zone
#     try:
#         cursor.execute(sql)
#         sensor_db.commit()
#     except Exception as e:
#         sensor_db.rollback()
#         print("error : ", str(e))
#     finally:
#         sensor_db.close()


# ##차량번호 확인, 자리확인
# def check_car_no(car_no):
#     move_bar = threading.Thread(target=move_motor)
#     bcheck = False
#     sensor_db = connect_db()  # db연결
#     cursor = sensor_db.cursor()
#     sql = "select count(*) from car_info where car_no = '%s'" % car_no
#     try:
#         cursor.execute(sql)
#         list_car_no = cursor.fetchall()
#         # list_car_no[0][0] = 1이면 등록되어있는 차, 모터 움직임
#         # 0이 나오면 등록이 되어있지 않은 차
#         if list_car_no[0][0] == 1:
#             bcheck = True
#             # 모터 움직임. 쓰레드로 2초 올렸다가 알아서 내려감
#             move_bar.start()
#     except Exception as e:
#         print("error : ", str(e))
#     finally:
#         sensor_db.close()
#         move_bar.join()
#         return bcheck


# # OLED 표시, 일반 차량만
# def OLED_show():
#     num = len(led_zone())
#     # I2C 버스 초기화
#     i2c = busio.I2C(board.SCL, board.SDA)
#     # SSD1306 OLED 디스플레이 초기화
#     oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
#     # 이미지 생성
#     image = Image.new("1", (oled.width, oled.height))
#     draw = ImageDraw.Draw(image)
#     if num == 6:  # 자리없음, 사용중인자리가 6개
#         # 폰트 크기 설정, 텍스트 표시
#         font = ImageFont.truetype("NanumGothic.ttf", 50)
#         draw.text((0, 0), " 만차", font=font, fill=255)
#     else:
#         font = ImageFont.truetype("NanumGothic.ttf", 23)
#         draw.text((0, 0), "   주차가능\n남은자리 : %d" % (6 - num), font=font, fill=255)
#     # 이미지를 디스플레이에 표시
#     oled.image(image)
#     oled.show()


# # 종료시 GPIO 클린업
# def cleanup():
#     GPIO.Cleanup()
