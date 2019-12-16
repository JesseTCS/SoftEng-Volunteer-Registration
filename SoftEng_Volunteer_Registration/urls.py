"""SoftEng_Volunteer_Registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth import views
from django.urls import path, include
import Registration.views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Registration.views.home, name='home'),
    path('Registration/<int:id>', Registration.views.details, name='details'),
    path('thanks/',Registration.views.thanks, name='thanks'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/profile/', Registration.views.profile, name='profile'),
    # path('accounts/logout/<str: irrelavant>', Registration.views.logout, name='logout'),
    path('dashboard/', Registration.views.dashboard, name='dashboard'),
    path('upload/', Registration.views.timelot_upload, name='upload'),
    path('create_user/', Registration.views.create_user, name='create_user'),
    path('group_register/<int:id>', Registration.views.group_register, name='group_register'),
    path('password-change/', views.PasswordChangeView.as_view, name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('test/', Registration.views.test, name='test'),
]
