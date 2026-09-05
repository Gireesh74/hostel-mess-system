from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'), 
    path('home/', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('attendance/', views.attendance, name='attendance'),
    path('complaint/', views.complaint, name='complaint'),
    path('rating/', views.rating, name='rating'),
    path('bill/', views.bill, name='bill'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),

]