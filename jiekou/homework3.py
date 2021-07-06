import time
class ParkingLot():
    def __init__(self,parking_lot_name,car_space_total_num,current_car_space_num,charge_per_min,time_out):
        self.parking_lot_name=parking_lot_name
        self.car_space_total_num=car_space_total_num
        self.current_car_space_num=current_car_space_num
        self.charge_per_min=charge_per_min #每分钟收多少钱
        self.time_out=time_out #缴费后出场时间
        self.in_car_list=[]
        self.out_car_list=[]
    def in_car_info(self):
        res=[]
        for i in self.in_car_list:
            if i.leave_status==0:
                timeArray=time.localtime(i.realintime)
                otherStyleTime=time.strftime("进场时间为%Y-%m-%d %H:%M:%S",timeArray)
                res.append([i.car_plate,otherStyleTime])
        return res

    def in_car(self,incar):#车辆进场
        self.in_car_list.append(incar)
        incar.intimecar=int(time.time())
        incar.realintime=incar.intimecar #记录进场车辆的进场时间

    def get_should_pay(self,moneycar,outtime,intime):#获取应缴费用
        if (outtime-intime)%60 !=0:  #如果超过整数分钟，则计算时长+1
            moneycar.money=((outtime-intime)//60+1)*self.charge_per_min
        else:
            moneycar.money=((outtime-intime)//60)*self.charge_per_min
        return moneycar.money

    def out_car(self,outcar_plate): #车辆离场
        for l in self.in_car_list:
            if outcar_plate == l.car_plate:
                self.out_car_info(l)
                l.outtimecar=time.time()
                if (l.paymoneytime!=0) and ((time.time()-l.intimecar)<=(self.time_out*60)):  #判断是否缴过钱
                    l.leave_status=1
                    return {"msg":"一路顺风"}
                else:
                    l.money=0
                    l.money=l.money+self.get_should_pay(l,l.outtimecar,l.intimecar)
                    l.leave_status=1
                    return {"msg": l.car_plate + "缴费" + str(l.money) + "离场成功"}
        return "0"

    def out_car_info(self,out_car_obj=0):
        if out_car_obj!=0:
            timeArray2 = time.localtime(out_car_obj.intimecar)
            otherStyleTime2 = time.strftime("离场时间为%Y-%m-%d %H:%M:%S", timeArray2)
            self.out_car_list.append([out_car_obj.car_plate, out_car_obj.car_type, otherStyleTime2])
        else:
            return self.out_car_list

    def get_car_space_num(self): #获取剩余临时车位
        count=0
        for m in self.in_car_list:
            if m.leave_status==0:
                count=count+1
        self.current_car_space_num =self.car_space_total_num-count
        return self.current_car_space_num

    def get_charge_car(self,moneycar_plate):#查费，用当前时间减去进场时间
        for j in self.in_car_list:
            if moneycar_plate == j.car_plate: #判断该车是否在场
                if (j.paymoneytime != 0) and ((time.time() - j.intimecar) <= (self.time_out * 60)): #判断该车是否已缴费，且在设置的超时时间内。是就返回0，不是就计算费用
                    return "0"
                else:
                    self.money = self.get_should_pay(j, time.time(), j.intimecar)
                    return str(self.money)
        return "该车没有在场记录"


    def paymoney(self,paymoneycar_plate):#缴费接口，缴费后更新缴费时间
        for k in self.in_car_list:
            if paymoneycar_plate == k.car_plate:
                k.paymoneytime=time.time()
                k.money=k.money+self.get_should_pay(k,k.paymoneytime,k.intimecar)
                k.intimecar=k.paymoneytime
                return {"msg":k.car_plate+"已缴费"+str(k.money)}
        return {"msg": "该车没有在场记录"}

class Car():
    def __init__(self,car_plate,car_type,plate_color="蓝"):
        self.car_plate=car_plate
        self.car_type=car_type
        self.intimecar =0
        self.realintime=0
        self.outimecar =0
        self.money=0
        self.paymoneytime=0
        self.leave_status=0
        if self.car_type[0]=="新":
            self.plate_color="绿"
        else:
            self.plate_color=self.car_type[0]
