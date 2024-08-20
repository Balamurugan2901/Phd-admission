import re
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
from django.core.paginator import Paginator
from django.conf import settings
from applications.form import userform,SchoolDetailsForm,Index,Personal_Detail,BachelorEducationForm,Master,DCMemberForm,GuideDetailsForm
from applications.models import User,PersonalDetails,BachelorEducationDetails,MasterEducationDetails,DCMember,GuideDetails
from django.contrib import messages
# import pandas as pd
# from num2words import num2words
# from django.core.mail import send_mail
# Create your views here.
dept_code={"ARTIFICIAL INTELLIGENCE AND DATA SCIENCE":"AD",
                "CIVIL ENGINEERING":"CE",
                "COMPUTER SCIENCE AND BUSINESS SYSTEM":"CB",
                "COMPUTER SCIENCE AND ENGINEERING":"CSE",
                "ELECRICAL AND ELECTRONICS ENGINEERING":"EEE",
                "ELECTRONICS AND COMMUNICATION ENGINEERING":"ECE",
                "INFORMATION TECHNOLOGY":"IT",
                "MECHANICAL ENGINEERING":"MECH",}

def index(request):
    user_data = request.session.get('user_data', {})

    if request.method == 'POST':
        form = Index(request.POST, request.FILES)
        if form.is_valid():
            user_data.update(form.cleaned_data)
            request.session['user_data'] = user_data
            form.save()
            # Store Highest Qualification in the session for later use
            highest_qualification = form.cleaned_data.get('Highest_Qualification')
            request.session['highest_qualification'] = highest_qualification

            return redirect('personal')  # Redirect to the personal details page

    else:
        form = Index()

    return render(request, 'application/index.html', {'form': form})

def personal(request):
    user_data = request.session.get('user_data', {})

    if request.method == 'POST':
        form = Personal_Detail(request.POST)
        # print("POST data: ", request.POST)  # Print POST data to check what's being submitted
        if form.is_valid():
            user_data.update(form.cleaned_data)
            request.session['user_data'] = user_data
            form.save(commit=False)

            messages.success(request, 'Personal details saved successfully.')
            # Redirect based on the highest qualification
            highest_qualification = request.session.get('highest_qualification')
            if highest_qualification == "Bachelor's":
                print("working.......")
                return redirect('bachelor')
            # elif highest_qualification == "Master's":
            #     return redirect('Masterform')
            else:
                print("working.wewe.............")
                return redirect('Masterform')  # If neither, redirect to a default page
        else:
            print("Form errors: ", form.errors)  # Print form errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = Personal_Detail()

    return render(request, 'application/personal.html', {'form': form})
# def index(request):
#     user_data = request.session.get('user_data', {})

#     if request.method == 'POST':
#         form = Index(request.POST, request.FILES)
#         if form.is_valid():
#             user_data.update(form.cleaned_data)
#             request.session['user_data'] = user_data

#             # Check for 'next_page' in the POST data to decide redirection
#             if 'next_page' in request.POST and request.POST['next_page'] == 'Personal':
#                 # Save the data if necessary
#                 count = Index.objects.count()
#                 year = datetime.now().strftime("%Y")
#                 mon = datetime.now().strftime("%B")
#                 app_no = f'{year}-{int(year)+1}/{mon}/{count}'
#                 # Optionally save form data or do something with app_no
#                 # form.save()  # Uncomment if you need to save the form data

#                 return redirect('personal')  # Make sure 'personal_form' is the correct URL name

#     return render(request, 'application/index.html', {'user_data': user_data})

# def Personal(request):
#     if request.method == 'POST':
#         form = Personal_Detail(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Personal details saved successfully.')
#             return redirect('next_page')  # Replace 'next_page' with the actual URL name for the next page
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = Personal_Detail()

#     return render(request, 'application/personal.html', {'form': form})

# def bachelor(request):
#     if request.method == 'POST':
#         form = BachelorForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Bachelor details saved successfully.')
#             return redirect('next_page')  # Replace with the actual next page URL
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = BachelorForm()

#     return render(request, 'application/bachelor.html', {'form': form})

def home(request):
    return render(request,'application/home.html')

def School_form(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = SchoolDetailsForm(request.POST)
        if form.is_valid():
            user_data.update(form.cleaned_data)
            request.session['user_data'] = user_data
            form.save(commit=False)
            return redirect('next_page_url')  # Replace with the actual URL name for the next page
    else:
        form = SchoolDetailsForm()
    return render(request, 'application/school_form.html', {'form': form})

def dc_member_view(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = DCMemberForm(request.POST)
        if form.is_valid():
            user_data.update(form.cleaned_data)
            request.session['user_data'] = user_data
            form.save(commit=False)
            return redirect('success_page')  # Redirect to a success page or the next step
    else:
        form = DCMemberForm()

    return render(request, 'application/Dcmember.html', {'form': form})

def bachelor(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = BachelorEducationForm(request.POST)
        if form.is_valid():
            user_data.update(form.cleaned_data)
            request.session['user_data'] = user_data
            form.save(commit=False)
            return redirect('guide_view')  # Redirect to a success page
    else:
        form = BachelorEducationForm()

    return render(request, 'application/Bachelor.html', {'form': form})

def Masterform(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = Master(request.POST)
        if form.is_valid():
            user_data.update(form.cleaned_data)
            request.session['user_data'] = user_data
            form.save(commit=False)
            return redirect('guide_view')  # Redirect to a success page
    else:
        form = Master()

    return render(request, 'application/Master.html', {'form': form})

def guide_view(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = GuideDetailsForm(request.POST)
        if form.is_valid():
            user_data.update(form.cleaned_data)
            request.session['user_data'] = user_data
            form.save(commit=False)
            messages.success(request, 'Guide details saved successfully.')
            return redirect('dc_member_view')  # Replace 'some_default_page' with the actual page you want to redirect to
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GuideDetailsForm()

    return render(request, 'application/guide.html', {'form': form})

def encrypt_password(raw_password):
    # Implement your password encryption algorithm (e.g., using hashlib)
    import hashlib
    return hashlib.sha256(raw_password.encode()).hexdigest()

def signup(request):
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
            password = form.cleaned_data['Password']
            confirm_password = form.cleaned_data['confirm_Password']

            if password == confirm_password:
                encrypted_password = encrypt_password(password)

                # Save the encrypted password to your user model
                user = form.save(commit=False)  # Don't save the form yet
                user.Password = encrypted_password
                user.confirm_Password = encrypted_password

                user.save()

                # Redirect to a success page or login page
                return redirect('login')
            else:
                # Passwords don't match, return an error
                form.add_error('confirm_password', 'Passwords do not match')
                return render(request, "Auth/signup.html", {'form': form})
        else:
            return render(request, "application/error.html", {'form': form})
    else:
        form = userform()

    return render(request, "auth/signup.html", {'form': form})


def login(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        password = request.POST.get('password')
        print(staff_id,password)
        # Fetch the user from the database
        try:
            user = User.objects.get(staff_id=staff_id)
        except User.DoesNotExist:
            # User not found, show an error message
            error_message = 'Invalid staff_id or password.'
            return render(request, "auth/login.html", {'error_message': error_message})

        # Check if the password matches
        if user.Password == encrypt_password(password):
            name=user.Name
            # Passwords match, log in the user
            # Set session variables or use Django's login system as needed
            request.session['user_id'] = user.id
            user = get_object_or_404(User, staff_id=staff_id)
            user_dict = {
            'id': user.id,
            'staff_id': user.staff_id,
            'name': user.Name,
            'user_name': user.user_name,
            'Department' : user.Department,
            'email' : user.email,
            'role' : user.role,
            'Password' : user.Password,
            'confirm_Password' : user.confirm_Password           }

            request.session['user_data'] = user_dict
            return redirect('index')
        else:
            # Passwords don't match, show an error message
            error_message = 'Invalid username or password.'
            return render(request, "Auth/login.html", {'error_message': error_message})

    return render(request, "Auth/login.html")
def logout(request):

    print('logout function called')
    auth_logout(request)
    messages.success(request,'You were logged out')
    request.session.flush()  # Flush all session data
    return render(request, "auth/login.html")

