from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .forms import CustomerForm, UserForm, PLotForm, CarForm, CarHistoryForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers
from django.conf import settings
import os
from .models import Customer, Temp_car_history, User, Temp_car, PLot, Slot
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from . import models
import operator
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.hashers import make_password
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView,
)
from socket import *
import time
import threading
import pandas as pd
import math

# from .socker_server_test import start_monitor
def timestamp_now():
    return str(datetime.now().timestamp())


def time_str_now():
    return datetime.now().strftime("%Y.%m.%d %H:%M:%S")


def from_stamp_to_string(stamp):
    
    return datetime.fromtimestamp(float(stamp)).strftime("%Y.%m.%d %H:%M:%S")


def from_obj_to_str(time):
    return time.strftime("%Y.%m.%d %H:%M:%S")


def cal_discount(money_amount):
    if int(money_amount) >= 1000:
        if int(money_amount) >= 2000:
            if int(money_amount) >= 3000:
                return 7
            else:
                return 8
        else:
            return 9


def from_str_to_obj(formatted_str_time):
    return datetime.strptime(formatted_str_time, "%Y.%m.%d %H:%M:%S")

def action_payment(plate):
    print("The car " + plate + " paied!")

def cal_total_cost(time_spent, discount):
    discount=discount/10
    rem = time_spent % 24
    days = (time_spent - rem) / 24
    if rem >= 5:
        hours_charge = 5 * days + 5
    else:
        hours_charge = days * 5 + rem
    return hours_charge * 10 * discount
    
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:  # super manager
                return redirect("dashboard")
            elif user.is_user:  # commen manager
                return redirect("dashboard")
            else:
                return redirect("login")
        else:
            messages.error(request, "Wrong username or password!")

    return redirect("home")


def logout_view(request):
    logout(request)
    return redirect("/")


def home(request):
    return render(request, "basic_web/login.html")


def signup(request):
    return render(request, "basic_web/login.html")


"""
Home page 
"""


@login_required
def dashboard(request):
    # total_it = Customer.objects.aggregate(Sum("total_cost"))

    # print(total_it.get("total_cost__sum"))
    # total_it = total_it.get("total_cost__sum")

    # total_cost = total_it
    # cars = Customer.objects.all().count()
    
    slot_num=Slot.objects.all().count()
    slot_all=Slot.objects.all().values()
    free_list=[]
    for i in range(0,slot_num):
        if slot_all[i]['is_free']:
            free_list.append(slot_all[i]['idn'])
    num_free=len(free_list)   
    free_list.sort()
    str_free_list=""
    for j in free_list:
        str_free_list=str_free_list+str(j)+" "

    cars = Temp_car.objects.all().count()
    users = User.objects.all().count()
    customers = Customer.objects.all().count()
    cars_history = Temp_car_history.objects.all().count()
    context = {
        "slots":"空闲车位："+str(num_free)+"/"+str(slot_num)+"，空闲车位："+str_free_list,
        "users": users,
        "cars": cars,
        "customers": customers,
        "cars_history": cars_history,
    }

    return render(request, "basic_web/dashboard.html", context)


"""
NOTE: add_customer(.html) was changed from ass_vehicle
Pass the values to the rendered add_customer.html
The last two item: cost per day, is every componenet of the car checked before (actually useless)
"""


def add_customer(request):
    topup = {"topup": ["充值", 1000, 2000, 3000]}
    return render(request, "basic_web/add_customer.html", topup)


"""
NOTE: save_customer changed from save_vehicle
Obtain informatin of the new customer from POST request
"""


def save_customer(request):
    if request.method == "POST":
        discount = 10
        full_name = request.POST["full_name"]
        plate = request.POST["plate"]
        balance = request.POST["balance"]
        print("Type of balance: " + str(type(balance)))
        # 时间一律先使用datetime.now().replace(tzinfo=timezone.utc)生成时间对象，之后可以根据需要调用timestamp()或者strftime()
        discount = cal_discount(balance)

        print("Balance: " + str(balance))
        print("Discount: " + str(discount))
        timenow = datetime.now()
        card_number = timestamp_now()
        phone_number = request.POST["phone_number"]
        comment = request.POST["comment"]
        date_time = datetime.utcnow()  # datetime.utcnow().replace(tzinfo=timezone.utc).strftime("%Y.%m.%d %H:%M:%S")
        if Customer.objects.filter(plate=plate).exists():
            messages.error(request, "创建失败！已存在该车牌号。")
            return redirect("add_customer")
        a = Customer(
            full_name=full_name,
            phone_number=phone_number,
            plate=plate,
            reg_date=date_time,
            comment=comment,
            balance=balance,
            discount=discount,
            card_number=card_number,
        )
        a.save()
        messages.success(request, "新会员注册成功！")
        return redirect("customer")


"""
Unpaied vehicles 
Direct to "list of unpaied vehicles", or "no vehicle"
"""


class Vehicle(ListView):

    model = Temp_car
    template_name = "basic_web/list_vehicle.html"
    context_object_name = "cars"
    paginate_by = 10

    def get_queryset(self):
        return Temp_car.objects.all()


"""
Paied vehicles (new)
Direct to "list of paied vehicles", or "no vehicle"
"""

# TODO 待更改
class VehicleHistory(ListView):

    model = Temp_car_history
    template_name = "basic_web/list_vehicle_his.html"
    context_object_name = "cars_history"
    paginate_by = 10

    def get_queryset(self):
        return Temp_car_history.objects.all()


class CustomerView(ListView):

    model = Customer
    template_name = "basic_web/list_customer.html"
    context_object_name = "customers"
    paginate_by = 10

    def get_queryset(self):
        return Customer.objects.filter(balance__gt=0)


"""
Floating window of vehicle list 
"""


class VehicleReadView(BSModalReadView):

    model = Temp_car
    template_name = "basic_web/view_vehicle.html"


class CustomerReadView(BSModalReadView):

    model = Customer
    template_name = "basic_web/view_customer.html"


"""
Floating window of vehicle list
"""


class VehicleHistoryReadView(BSModalReadView):
    model = Temp_car_history
    template_name = "basic_web/view_vehicle_his.html"


# TODO use ajax implement hot update (partial refresh)

"""
Floating window of edition of a vehicle's info
Used the defined form
"""


class VehicleUpdateView(BSModalUpdateView):

    model = Temp_car
    template_name = "basic_web/update_vehicle.html"
    form_class = CarForm
    success_message = "车辆信息更新成功!"
    success_url = reverse_lazy("vehicle")


class VehicleHistoryUpdateView(BSModalUpdateView):

    model = Temp_car_history
    template_name = "basic_web/update_vehicle_his.html"
    form_class = CarHistoryForm
    success_message = "车辆记录编辑成功!"
    success_url = reverse_lazy("vehicle_his")


class CustomerUpdateView(BSModalUpdateView):

    model = Customer
    template_name = "basic_web/update_customer.html"
    form_class = CustomerForm
    success_message = "会员信息更新成功！"
    success_url = reverse_lazy("customer")
    # redirect("customer")


"""
Floating window of "delete" msg box
"""


class VehicleDeleteView(BSModalDeleteView):
    model = Temp_car
    template_name = "basic_web/delete_vehicle.html"
    form_class = CarForm
    success_url = reverse_lazy("vehicle")
    success_message = "车辆删除成功！"
    # messages.success(request, "Vehicle Registered Successfully")


class VehicleHistoryDeleteView(BSModalDeleteView):
    model = Temp_car_history
    template_name = "basic_web/delete_vehicle_his.html"
    form_class = CarHistoryForm
    success_url = reverse_lazy("vehicle_his")
    success_message = "车辆记录删除成功！"


class CustomerDeleteView(BSModalDeleteView):
    model = Customer
    template_name = "basic_web/delete_customer.html"
    form_class = CustomerForm
    success_url = reverse_lazy("customer")
    success_message = "会员删除成功！"


def file_upload(request):
    if request.method == "GET":
        return render(request, "basic_web/upload_customers.html")
    else:
        # name=request.POST.get('name')
        myfile = request.FILES.get("myfile")
        # 姓名	 车牌	余额	折扣	电话	注册时间	卡号	备注
        data = pd.read_excel(myfile)
        df = pd.DataFrame(data)
        df = df.fillna(" ")
        for i in range(df.shape[0]):
            if (
                df.loc[i][0] == ""
                or df.loc[i][0] == " "
                or df.loc[i][1] == " "
                or df.loc[i][2] == " "
                or df.loc[i][4] == " "
                or df.loc[i][4] == " "
            ):
                messages.error(request, "导入失败，姓名，车牌，余额和电话字段必须有效！")
                return redirect("file_upload")

            full_name = df.loc[i][0]
            plate = df.loc[i][1]
            balance = df.loc[i][2]  # int
            discount = df.loc[i][3]  # int
            phone_number = df.loc[i][4]
            reg_time = df.loc[i][5]

            card_number = str(df.loc[i][6])
            if card_number != " ":
                pass
            else:
                card_number = str(timestamp_now())

            comment = df.loc[i][7]
            try:
                reg_time = from_str_to_obj(reg_time)

            except Exception as e:

                reg_time = datetime.fromtimestamp(float(card_number))

            print(
                "#LOG: \n name: "
                + str(df.loc[i][0])
                + ", balance: "
                + str(df.loc[i][2])
                + ", reg_time: "
                + str(df.loc[i][5])
                + ", card_number: "
                + str(df.loc[i][6])
                + ", type: "
                + str(type(df.loc[i][6]))
            )

            if df.loc[i][3] != " ":
                discount = int(df.loc[i][3])
                # print(full_name + " has discount of " + str(discount))
            else:
                discount = cal_discount(balance)
                
            if Customer.objetcs.filter(plate=plate).exists():
                messages.error(request, "上传失败！车牌号"+plate+"已存在。")
                
                return redirect("add_customer")
            a = Customer(
                full_name=full_name,
                phone_number=phone_number,
                plate=plate,
                reg_date=reg_time,
                comment=comment,
                balance=balance,
                discount=discount,
                card_number=card_number,
            )
            a.save()
        messages.success(request, "会员批量导入成功！")
        return redirect("customer")


def pay(request, pk):
    success_msg= pay_action(pk)
    messages.success(request, success_msg)
    return redirect("vehicle")


def pay_action(pk):
    # list of car obj: list(Temp_car.objects.filter(id=pk).values())[0]

    car_object_list = list(Temp_car.objects.filter(id=pk).values())[0]
    plate = car_object_list["plate"]

    enter_time = car_object_list["enter_time"]
    print("no error here in 447")
    time_spent = math.ceil(((datetime.now() - enter_time).seconds) / 3600)
    exit_time = datetime.now()
    print("no error here in 449")
    
    try:
        card_number = car_object_list["card_number"]
    except:
        card_number = None
        
    if card_number is not None:
        card = Customer.objects.filter(card_number=card_number)
        customer_qset = list(Customer.objects.
                             filter(card_number=card_number).values())[0]
        balance = customer_qset["balance"]
        discount = customer_qset["discount"]
        print("no error here in 457, balance is "+str(balance))
        total_cost = cal_total_cost(time_spent, discount)
        balance = balance - total_cost
        print("no error here in 460")
        if balance < 0:
            complement = str(0 - balance)
            balance = 0
            msg2 = " 余额不足，还需支付" + complement + "元."
            Customer.objects.filter(id=pk).delete()
            action_payment(plate)
        else:
            Customer.objects.filter(card_number=card_number).update(balance=balance)
            msg2=""
        payment_method = "自动"
    else:
        payment_method = "手动"
        total_cost=cal_total_cost(time_spent, 10)
        msg2 = " 支付" + str(total_cost) + "元."

    a = Temp_car_history(
        plate=plate,
        # card=card,
        card_number=card_number,
        enter_time=enter_time,
        exit_time=exit_time,
        total_cost=total_cost,
        time_spent=time_spent,
    )
    a.save()
    Temp_car.objects.filter(id=pk).delete()
    success_msg="车辆" + plate + payment_method + "支付成功!" + msg2
    return success_msg


def start_monitor():
    thread_monitor_gate = threading.Thread(target=monitor_gate)
    thread_monitor_slots = threading.Thread(target=monitor_slots)
    thread_monitor_gate.start()
    thread_monitor_slots.start()
    print("Sensor monitor starting...")


def monitor_gate():
    while True:
        tcp_server = socket(AF_INET, SOCK_STREAM)
        tcp_server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        # default as localhost
        ip = ""
        port = 1999
        tcp_server.bind((ip, port))
        # .listen * maximum connections
        tcp_server.listen(128)
        print("#LOG: Accepting new gate monitor...")
        # accept new connections(sockets) and store
        client_socket, client_addr = tcp_server.accept()
        print(
            "\n#LOG: Gate monitor "
            + str(client_addr).split("'")[1]
            + ":"
            + str(port)
            + " connected at "
            + datetime.now().strftime("%H:%M:%S")
        )
        try:
            while True:
                from_client_msg = client_socket.recv(4096).decode("utf-8")

                if not (len(from_client_msg) == 0 or from_client_msg.isspace()):

                    # print("TEST: received msg from client:"+str(from_client_msg))
                    # string解析回list of string
                    received_car = eval(from_client_msg)
                    print("# 收到socket msg:"+str(received_car))
                    #  Retrieve plate string
                    plate_ = received_car[0]
                    # Convert string timestamp to float
                    print("no error here in 531")
                    time_car_enter_timestamp = float(received_car[1])
                    action3 = received_car[2]
                    is_in = bool(received_car[3])
                    print("no error here in 530, is_in :"+str(is_in))
                    if is_in:
                        enter_time = datetime.fromtimestamp(time_car_enter_timestamp)
                        print("no error here in 533")
                        try:
                            card_object = list(
                                Customer.objects.filter(plate=plate_).values()
                            )[0]
                            print("no error here in 538")
                            card_number = card_object["card_number"]
                            print("++"+str(card_object))
                        except:
                            card_object =None
                            
                        if card_object and card_object is not None:
                            a = Temp_car(plate=plate_,enter_time=enter_time,card_number=card_number,)
                        else:
                            a = Temp_car(
                                plate=plate_,
                                enter_time=enter_time,
                            )
                        a.save()
                        print(
                            "#LOG: PLot: "
                            + plate_
                            + " "
                            + action3
                            + "\t"
                            + from_obj_to_str(enter_time)
                        )
                    else:
                        car = list(Temp_car.objects.filter(plate=plate_).values())[0]
                        car_id = car["id"]
                        print("no error here in 575")
                        pay_action(car_id)
                    # Reply with task result
                    client_socket.send(("ok").encode("utf-8"))
                else:
                    client_socket.close()
                    break
        except KeyboardInterrupt:
            print("Socket closed by keyboard interrupt!")
        except BrokenPipeError:
            print("Socket closed by client!")
        except Exception as e:
            print("Socket closed by error: " + str(e))
        finally:
            if getattr(client_socket, "_closed") == False:
                client_socket.close()

def monitor_slots():
    while True:
        tcp_server2 = socket(AF_INET, SOCK_STREAM)
        tcp_server2.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        ip = ""
        port = 2001
        tcp_server2.bind((ip, port))
        tcp_server2.listen(128)
        print("#LOG: Accepting new slots monitor...")
        client_socket2, client_addr2 = tcp_server2.accept()
        
        print("\n#LOG: Slots monitor "+ str(client_addr2).split("'")[1]+ ":"+ str(port)+ " connected at "+ datetime.now().strftime("%H:%M:%S"))
        
        try:
            while True:
                from_client_msg2 = client_socket2.recv(4096).decode("utf-8")

                slots_list_str = eval(from_client_msg2)
                # print("# Slot monitor 收到:"+str(slots_list_str))
                free_list=list(slots_list_str)
                list1=[1,2,3,4,5,6,7,8,9]
                occupied_list=list(set(list1).difference(set(free_list)))
                # Slot.objects.all().delete()
                for i in free_list:
                    Slot.objects.filter(idn=i).update(is_free=True)
                  
                for j in occupied_list:
                    Slot.objects.filter(idn=j).update(is_free=False)
                        
                client_socket2.send(("ok").encode("utf-8"))
              
        except KeyboardInterrupt:
            print("Socket closed by keyboard interrupt!")
        except BrokenPipeError:
            print("Socket closed by client!")
        except Exception as e:
            print("Socket closed by error: " + str(e))
        finally:
            if getattr(client_socket2, "_closed") == False:
                client_socket2.close()
    
class UserView(ListView):
    model = User
    template_name = "basic_web/list_user.html"
    context_object_name = "users"
    paginate_by = 5

    def get_queryset(self):
        return User.objects.order_by("-id")

class UserUpdateView(BSModalUpdateView):
    model = User
    template_name = "basic_web/update_user.html"
    form_class = UserForm
    success_message = "用户信息更新成功！"
    success_url = reverse_lazy("users")

class UserReadView(BSModalReadView):
    model = User
    template_name = "basic_web/view_user.html"

class DeleteUser(BSModalDeleteView):
    model = User
    template_name = "basic_web/delete_user.html"
    success_message = "用户删除成功！"
    success_url = reverse_lazy("users")



def create(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password = make_password(password)

        a = User(

            username=username,
            email=email,
            password=password,
            is_admin=True,
        )
        a.save()
        messages.success(request, "管理员添加成功！")
        return redirect("users")

    else:

        return render(request, "basic_web/add_user.html")


start_monitor()
