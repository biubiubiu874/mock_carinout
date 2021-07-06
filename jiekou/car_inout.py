import json
from flask import Flask,request,jsonify
import homework3 as open_interface
app = Flask(__name__)
AkeParking=open_interface.ParkingLot("AKE测试停车场",500,500,1.5,3)
# Car_class={}
# 车辆进场接口
@app.route('/car_in',methods=["POST"])
def car_in():
    car_number=request.json.get("car_number")
    car_type=request.json.get("car_type")
    Car=open_interface.Car(car_number,car_type)
    AkeParking.in_car(Car)
    res={"msg":"ok"}
    return jsonify(res)
# 车辆离场接口
@app.route('/car_out',methods=["POST"])
def car_out():
    leavecar_number=request.json.get("car_number")
    accout_leavecar=AkeParking.out_car(leavecar_number)
    if accout_leavecar != "0":
        return jsonify(accout_leavecar)
    else:
        res={"msg":"该车没有进场记录，请走人工验证放行"}
        return jsonify(res)
# 获取在场车辆记录接口
@app.route('/get_in_car_list',methods=["POST"])
def get_in_car_list():
    res=AkeParking.in_car_info()
    return jsonify(res)
# 获取离场车辆记录接口
@app.route('/get_out_car_list',methods=["POST"])
def get_out_car_list():
    res={"out_car_list":AkeParking.out_car_info()}
    return jsonify(res)
# 获取车场剩余临时车位接口
@app.route('/get_current_car_space_num',methods=["POST"])
def get_current_car_space_num():
    car_space_num=AkeParking.get_car_space_num()
    res={"current_car_space_num":car_space_num}
    return jsonify(res)
# 查费接口
@app.route('/get_charge',methods=["POST"])
def get_charge():
    moneycar_number=request.json.get("car_number")
    res = {"msg": AkeParking.get_charge_car(moneycar_number)}
    return jsonify(res)
# 缴费接口
@app.route('/paymoney',methods=["POST"])
def paypay():
    paymoneycar_number = request.json.get("car_number")
    res=AkeParking.paymoney(paymoneycar_number)
    return jsonify(res)
if __name__ == '__main__':
    app.run()