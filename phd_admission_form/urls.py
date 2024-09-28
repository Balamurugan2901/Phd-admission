"""
URL configuration for phd_admission_form project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path #type:ignore
from applications import views #type:ignor
from applications.admin import admin_site

urlpatterns = [
    path('rit_admin/', admin_site.urls),
    path('rit_admin/admin_portal',views.admin_portal,name="admin_portal"),
    path('signup', views.signup, name="signup"),
    path('scholar_signup/', views.scholar_signup, name='scholar_signup'),
    path('', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('index/',views.index,name='index'),
    path('personal/', views.personal, name='personal'),
    path('School_form/', views.School_form, name='School_form'),
    path('bachelor/', views.bachelor, name='bachelor'),
    path('master/', views.Masterform, name='Masterform'),
    path('experience/', views.experience, name='experience'),
    path('guide/', views.guide_view, name='guide_view'),
    path('Dcmember', views.dc_member_view, name='dc_member_view'),
    path('approval_view/', views.approval_view, name='approval_view'),
    path('generate_pdf', views.generate_pdf, name='generate_pdf'),
    path('check_form',views.check_form,name='check_form'),
    path('approving',views.approving,name='approving'),
    path('PhD_Status',views.PhD_Status,name='PhD_Status'),
    path('signup/', views.defaultUser, name='add_signup'),


    path('Dcmembers/check_register_number', views.check_register_number, name="check_register_number"),
    path('generate_qrcode/', views.generate_qrcode, name='generate_qrcode'),
    path('display_qrcode/', views.display_qrcode, name='display_qrcode'),



        path('check_form',views.check_form,name='check_form'),
        path('edit_form/', views.edit_form, name="edit_form"),

    path('upload_image/<path:register_number>/', views.upload_image, name='upload_image'),



]
