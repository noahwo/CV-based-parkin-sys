"""learndjango_b URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from learndjango_b import testdb
from basic_web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('pay/<int:pk>', views.pay, name='pay'),
    
    path('add_customer/', views.add_customer, name='add_customer'),
    path('save_customer/', views.save_customer, name='save_customer'), 
    path('customer/', views.CustomerView.as_view(), name='customer'),
    path('view_customer/<int:pk>', views.CustomerReadView.as_view(), name='view_customer'),
    path('update_customer/<int:pk>', views.CustomerUpdateView.as_view(), name='update_customer'),
    path('delete_customer/<int:pk>', views.CustomerDeleteView.as_view(), name='delete_customer'),
    path('file_upload/',views.file_upload,name='file_upload'),
 
    path('vehicle/', views.Vehicle.as_view(), name='vehicle'),
    path('view_vehicle/<int:pk>', views.VehicleReadView.as_view(), name='view_vehicle'),
    path('update_vehicle/<int:pk>', views.VehicleUpdateView.as_view(), name='update_vehicle'),
    path('delete_vehicle/<int:pk>', views.VehicleDeleteView.as_view(), name='delete_vehicle'),
    
    path('vehicle_history/', views.VehicleHistory.as_view(), name='vehicle_his'),
    path('view_vehicle_history/<int:pk>', views.VehicleHistoryReadView.as_view(), name='view_vehicle_his'),
    path('update_vehicle_history/<int:pk>', views.VehicleHistoryUpdateView.as_view(), name='update_vehicle_his'),
    path('delete_vehicle_history/<int:pk>', views.VehicleHistoryDeleteView.as_view(), name='delete_vehicle_his'),

    path('users/', views.UserView.as_view(), name='users'),
    path('view_user/<int:pk>', views.UserReadView.as_view(), name='view_user'),
    path('user_update/<int:pk>', views.UserUpdateView.as_view(), name='user_update'),
    path('delete_user/<int:pk>', views.DeleteUser.as_view(), name='delete_user'),
    path('create/create', views.create, name='create'),
    ]