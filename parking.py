# ##flask 실행

# from flask import Flask, render_template, request, jsonify
# import function as func
# from urllib.parse import urlencode, unquote
# import threading


# app = Flask(__name__)  # Initialize app


# # html이 로드될때 db에 먼저 접근
# # 주차되어 있는 자리와 등록된 차량의 수를 return
# # 나중에 차량의 수 -> 차량번호list로 바꿔야함
# # num_infocar : 등록된 차량의 수, list_park : 주차되어 있는 자리 -> 7에서 빼서 OLED에 사용가능
# @app.route("/", methods=["GET", "POST"])
# def index():
#     num = func.info_len()
#     list_park = func.info_carzone()
#     func.led_result()
#     func.OLED_show()
#     # 주차자리 남은 개수따라 led표시, OLED표시
#     # len(list_park) -> 0개면 led 빨강 아니면 초록
#     # 코드(함수)
#     data = {"num_infocar": num, "list_carzone": list_park}
#     return render_template("park.html", test=data)


# # 등록차량 멤버 html
# @app.route("/member", methods=["GET", "POST"])
# def park_member():
#     num = func.info_len()
#     car_list, handi_list = func.info_car_list()
#     data = {"num_infocar": num, "list_car": car_list, "handi": handi_list}
#     return render_template("member.html", li_data=data)


# # 정보처리 및 전달
# @app.route("/server_endpoint", methods=["POST"])
# def server_endpoint():
#     try:
#         data = request.get_json()
#         datalist = data.split()
#         move_bar = threading.Thread(target=func.move_motor)
#         # 주차선 색 바꾸기
#         if len(datalist) == 2:
#             try:
#                 if datalist[1] == "red":
#                     func.delete_zone(datalist[0])
#                     move_bar.start()
#                 else:
#                     func.add_zone(datalist[0])

#             except Exception as e:
#                 return jsonify({"error": str(e)})
#             finally:
#                 move_bar.join()
#                 result_data = {"message": "데이터 처리완료"}
#                 return jsonify(result_data)
#         # 입차확인(차량번호 체크), 차단봉 열기
#         else:
#             check = func.check_car_no(data)
#             result_data = {"message": "데이터 처리완료", "exist_car": check}
#             # result_data = {"message": "데이터 처리완료"}
#             return jsonify(result_data)
#     except Exception as e:
#         return jsonify({"error": str(e)})


# # 정보처리 및 전달(차량등록 팝업에서 보냄) return 없으면 안됨
# # data = "'차량번호' '버튼기능(add,del)' '핸디여부(true,false)'"
# @app.route("/m_server_endpoint", methods=["POST"])
# def m_server_endpoint():
#     # 동작을 실행했으면 True반환, 새로고침 아니면 False 반환 아무동작x
#     exist = True
#     try:
#         # 차 넘버를 받아와서 등록되어있는 차넘버들과 비교
#         data = request.get_json()
#         list_data = data.split()
#         list_carno = func.info_car_list()
#         # 등록버튼눌렸을 경우
#         if list_data[1] == "add":
#             # list_carno -> 튜플로 리턴([차량번호],[핸디여부])
#             if list_data[0] in list_carno[0]:
#                 exist = False
#                 result_data = {
#                     "message": "데이터 처리완료",
#                     "work": exist,
#                 }  # false로 반환(아무작업 안 함)
#                 return jsonify(result_data)
#             # 등록
#             else:
#                 num = func.info_len()
#                 # 등록 최대 15대까지만 가능
#                 if num > 14:
#                     exist = False
#                     result_data = {
#                         "message": "데이터 처리완료",
#                         "work": exist,
#                     }  # true로 반환(등록 완료)
#                     return jsonify(result_data)
#                 else:
#                     func.add_car_no(list_data[0], list_data[2])
#                     result_data = {
#                         "message": "데이터 처리완료",
#                         "work": exist,
#                     }  # true로 반환(등록 완료)
#                     return jsonify(result_data)
#         # 삭제버튼
#         else:
#             if list_data[0] not in list_carno[0]:  # 등록안되어 있는 차
#                 exist = False
#                 result_data = {
#                     "message": "데이터 처리완료",
#                     "work": exist,
#                 }  # false로 반환(아무작업 안 함)
#                 return jsonify(result_data)
#             else:
#                 func.delete_car_no(list_data[0])
#                 result_data = {"message": "데이터 처리완료", "work": exist}  # true로 반환(삭제완료)
#                 return jsonify(result_data)
#     except Exception as e:
#         return jsonify({"error": str(e)})


# if __name__ == "__main__":
#     app.run(host="0.0.0.0")
