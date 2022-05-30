from django.forms.utils import ValidationError
from basic_web.models import User, Customer,PLot, Temp_car, Temp_car_history
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer, User
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth import get_user_model
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class CustomerForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["phone_number"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["plate"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["comment"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["balance"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["discount"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["card_number"].widget.attrs = {"class": "form-control col-md-6"}

    class Meta:
        model = Customer
        fields = (
            "full_name",
            "plate",
            "balance",
            "discount",
            "card_number",
            "phone_number",
            "comment",
        )

class CarForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        self.fields["plate"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["enter_time"].widget.attrs = {"class": "form-control col-md-6"}
        # self.fields["time_spent"].widget.attrs = {"class": "form-control col-md-6"}
        # self.fields["total_cost"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["card_number"].widget.attrs = {"class": "form-control col-md-6"}

    class Meta:
        model = Temp_car
        fields = (
            "plate",
            "enter_time",
            # "time_spent",
            # "total_cost",
            "card_number",
        )
        
class CarHistoryForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(CarHistoryForm, self).__init__(*args, **kwargs)
        self.fields["plate"].widget.attrs = {"class": "form-control col-md-6"}
        # self.fields["enter_time"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["exit_time"].widget.attrs = {"class": "form-control col-md-6"}

        self.fields["time_spent"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["total_cost"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["card_number"].widget.attrs = {"class": "form-control col-md-6"}

    class Meta:
        model = Temp_car_history
        fields = (
            "plate",
            # "enter_time",
            "exit_time",
            "time_spent",
            "total_cost",
            "card_number",
        )
        
class PLotForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(PLotForm, self).__init__(*args, **kwargs)
        self.fields["total_space"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["used_space"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["avai_space"].widget.attrs = {"class": "form-control col-md-6"}

    class Meta:
        model = PLot
        fields = (
            "total_space",
            "used_space",
            # "avai_space",
        )

class UserForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs = {"class": "form-control col-md-6"}
    
        self.fields["email"].widget.attrs = {"class": "form-control col-md-6"}
        self.fields["password"].widget.attrs = {"class": "form-control col-md-6"}

    class Meta:
        model = User
        fields = ("username", "email", "password")
