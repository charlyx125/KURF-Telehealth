"""telehealth URL Configuration

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
from django.urls import path
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('patient_sign_up/', views.PatientSignUpView.as_view(), name='patient_sign_up'),
    path('doctor_sign_up/', views.DoctorSignUpView.as_view(), name='doctor_sign_up'),
    path('start_chat/', views.StartChatView.as_view(), name='start_chat'),
    path('show_chat/<int:chat_id>/', views.ShowChatView.as_view(), name='show_chat'),
    path('chat_list/', views.ChatListView.as_view(), name='chat_list'),
    path('reply_chat/<int:chat_id>', views.ReplyChatView.as_view(), name='reply_chat'),
]
