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
from applications.form import userform,SchoolDetailsForm,Index,Personal_Detail,BachelorEducationForm,Master,DCMemberForm,GuideDetailsForm,ProfessionalExperienceForm
from applications.models import User,PersonalDetails,BachelorEducationDetails,MasterEducationDetails,DCMember,GuideDetails,Experience_Details,ApplicationDetails
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
    if request.method == 'POST':
        form = Index(request.POST, request.FILES)
        if form.is_valid():
            # Get the Department from the form's cleaned data
            Department = form.cleaned_data['Department']
            print(f"Department: {Department}")

            # Generate the current date and format the application number
            current_date = datetime.now()
            year = current_date.year
            month = current_date.strftime("%B")

            # Retrieve and increment the application number for the department
            try:
                # Attempt to find an existing application for this department
                application_data = ApplicationDetails.objects.get(Department=Department)
                application_data.counter += 1
                application_data.save()
                print(f"Updated counter for Department: {application_data.counter}")
            except ApplicationDetails.DoesNotExist:
                # If no entry exists, create a new one with a counter of 1
                application_data = ApplicationDetails(Department=Department, counter=1)
                application_data.save()
                print(f"Created new counter for Department: {application_data.counter}")

            # Generate the application number
            appno = f"{application_data.counter:05d}"
            application_no = f"{year}-{year+1}/{month}/{dept_code[Department]}/{appno}"
            print(f"Generated application number: {application_no}")

            # Assign the generated application number to the form instance
            form.instance.application_no = application_no
            print(f"Application number set in form: {form.instance.application_no}")

            # Save the form data to the database
            form.save()
            print("Form saved successfully.")

            # Redirect to the personal details page
            return redirect('personal')
        else:
            # Handle form errors
            messages.error(request, 'Please correct the errors below.')
            print("Form errors: ", form.errors)  # Debugging: will appear in server logs

    else:
        form = Index()

    return render(request, 'application/index.html', {'form': form})


def personal(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = Personal_Detail(request.POST)
        if form.is_valid():
            user_data.update(form.cleaned_data)
            request.session['user_data'] = user_data
            form.save(commit=False)
            return redirect('School_form')  # Replace with the actual URL name for the next page
    else:
        form = Personal_Detail()
    return render(request, 'application/personal.html', {'form': form})

# def personal(request):
#     if request.method == 'POST':
#         form = Personal_Detail(request.POST)
#         if form.is_valid():
#             # Save the form data to the database
#             personal_detail_instance = form.save()

#             # Optional: If you need to store any information in the session
#             request.session['user_data'] = form.cleaned_data

#             # Redirect to the next form or page
#             return redirect('School_form')  # Replace with the actual URL name for the next page
#         else:
#             # Handle form errors
#             messages.error(request, 'Please correct the errors below.')
#             print("Form errors: ", form.errors)  # Debugging: will appear in server logs

#     else:
#         form = Personal_Detail()

#     return render(request, 'application/personal.html', {'form': form})


def School_form(request):
    user_data = request.session.get('user_data', {})

    if request.method == 'POST':
        form = SchoolDetailsForm(request.POST)
        # print("POST data: ", request.POST)  # Useful for debugging

        if form.is_valid():
            # Update session with cleaned data
            user_data.update(form.cleaned_data)
            request.session['user_data'] = user_data

            # Save the form data (commit=True by default saves it to the database)
            form.save(commit=False)

            messages.success(request, 'School details saved successfully.')

            # Redirect based on the highest qualification
            highest_qualification = request.session.get('highest_qualification')
            print("Highest Qualification:", highest_qualification)  # Debugging line
            if highest_qualification == "Bachelor's":
                return redirect('bachelor')
            else:
                return redirect('Masterform')
        else:
            print("Form errors: ", form.errors)  # Debugging: will appear in server logs
            messages.error(request, 'Please correct the errors below.')

    else:
        form = SchoolDetailsForm()

    return render(request, 'application/School_form.html', {'form': form})

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


def experience(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = ProfessionalExperienceForm(request.POST)
        if form.is_valid():
            user_data.update(form.cleaned_data)
            request.session['user_data'] = user_data
            form.save(commit=False)
            return redirect('next_page_url')  # Replace with the actual URL name for the next page
    else:
        form = ProfessionalExperienceForm()
    return render(request, 'application/experience.html', {'form': form})

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
def dc_member_view(request):
    user_data = request.session.get('user_data', {})

    if request.method == 'POST':
        form = DCMemberForm(request.POST)

        if form.is_valid():
            # Save DC Member details
            dc_member_instance = form.save()

            # Save all other forms using the session data
            try:
                # Save Personal Details
                personal_data = request.session.get('personal_data')
                if personal_data:
                    personal_form = Personal_Detail(personal_data)
                    if personal_form.is_valid():
                        personal_form.save()

                # Save School Details
                school_data = request.session.get('school_data')
                if school_data:
                    school_form = SchoolDetailsForm(school_data)
                    if school_form.is_valid():
                        school_form.save()

                # Save Bachelor's Education Details
                bachelor_data = request.session.get('bachelor_data')
                if bachelor_data:
                    bachelor_form = BachelorEducationForm(bachelor_data)
                    if bachelor_form.is_valid():
                        bachelor_form.save()

                # Save Master's Education Details
                master_data = request.session.get('master_data')
                if master_data:
                    master_form = Master(master_data)
                    if master_form.is_valid():
                        master_form.save()

                # Save Professional Experience Details
                experience_data = request.session.get('experience_data')
                if experience_data:
                    experience_form = ProfessionalExperienceForm(experience_data)
                    if experience_form.is_valid():
                        experience_form.save()

                # Save Guide Details
                guide_data = request.session.get('guide_data')
                if guide_data:
                    guide_form = GuideDetailsForm(guide_data)
                    if guide_form.is_valid():
                        guide_form.save()

                messages.success(request, 'All data has been saved successfully!')

                # Clear the session data after saving
                request.session.flush()

                # Redirect to a success page
                return redirect('success_page')  # Replace 'success_page' with the actual URL name

            except Exception as e:
                # Handle any errors that occur during saving
                messages.error(request, f'An error occurred: {e}')

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = DCMemberForm()

    return render(request, 'application/Dcmember.html', {'form': form})

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

