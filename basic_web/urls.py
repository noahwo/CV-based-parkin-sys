from django.urls import path, include
from . import views
from django.contrib import admin


app_name='basic_web'

urlpatterns = [
    # path('',views.login, name='home'),
    path('admin/', admin.site.urls),
    path('login/',views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('',views.home, name ='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pay/<int:pk>', views.Pay, name='pay'),
    
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('save_vehicle/', views.save_vehicle, name='save_vehicle'),
    path('vehicle/', views.Vehicle.as_view(), name='vehicle'),
    path('view_vehicle/<int:pk>', views.VehicleReadView.as_view(), name='view_vehicle'),
    path('view_car/<int:pk>', views.CarReadView.as_view(), name='view_car'),
    path('update_vehicle/<int:pk>', views.VehicleUpdateView.as_view(), name='update_vehicle'),
    path('update_car/<int:pk>', views.CarUpdateView.as_view(), name='update_car'),
    path('delete_vehicle/<int:pk>', views.VehicleDeleteView.as_view(), name='delete_vehicle'),
    path('delete_car/<int:pk>', views.CarDeleteView.as_view(), name='delete_car'),
    
    path('view_user/<int:pk>', views.UserReadView.as_view(), name='view_user'),
    path('users/', views.UserView.as_view(), name='users'),
    path('inoice/<int:pk>', views.GeneratePdf.as_view(), name='invoice'),
    path('user_update/<int:pk>', views.UserUpdateView.as_view(), name='user_update'),
    path('delete_user/<int:pk>', views.DeleteUser.as_view(), name='delete_user'),
    path('create/create', views.create, name='create'),
]