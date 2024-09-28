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
from applications.form import userform,SchoolDetailsForm,Index,Personal_Detail,BachelorEducationForm,Master,DCMemberForm,GuideDetailsForm,ProfessionalExperienceForm,ScholarForm,Status_form
from applications.models import approver,User,PersonalDetails,BachelorEducationDetails,MasterEducationDetails,DCMember,GuideDetails,Experience_Details,ApplicationDetails,SchoolDetails,Scholar,phd_status,departments,defaultUsers

# views.py
import qrcode
import io ,base64
import datetime

from django.contrib import messages
import pandas as pd
from num2words import num2words
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.
# dept_code={"ARTIFICIAL INTELLIGENCE AND DATA SCIENCE":"AD",
#                 "CIVIL ENGINEERING":"CE",
#                 "COMPUTER SCIENCE AND BUSINESS SYSTEM":"CB",
#                 "COMPUTER SCIENCE AND ENGINEERING":"CSE",
#                 "ELECRICAL AND ELECTRONICS ENGINEERING":"EEE",
#                 "ELECTRONICS AND COMMUNICATION ENGINEERING":"ECE",
#                 "INFORMATION TECHNOLOGY":"IT",
#                 "MECHANICAL ENGINEERING":"MECH",}
def generate_unique_admission_number(request):
    user_data = request.session.get('user_data', {})

    # Safely access department from user_data
    dept = user_data.get('Department')

    if not dept:
        raise ValueError("Department information is missing from session data.")

    # Get current year and next year
    current_year_last_two_digits = datetime.datetime.now()
    current_year = current_year_last_two_digits.strftime("%Y")
    month = current_year_last_two_digits.strftime("%B")
    next_year = str(int(current_year) + 1)

    # Get the last admission number to ensure sequential numbering
    last_admission = ApplicationDetails.objects.order_by('-application_no').first()

    if last_admission:
        try:
            # Extract the numeric part from the admission number
            last_number = int(last_admission.application_no.split('/')[-1])
        except (ValueError, IndexError):
            # Handle case where admission number is improperly formatted
            last_number = 0
    else:
        last_number = 0  # Start numbering from 1 if there are no previous records

    # Increment and format the new number as 3 digits (e.g., 001, 002, etc.)
    new_number = last_number + 1
    formatted_number = f"{new_number:03d}"

    # Look up department code based on the department name
    try:
        get_dept = departments.objects.get(department=dept)
        dept_code = get_dept.dept_code
    except departments.DoesNotExist:
        raise ValueError(f"Department '{dept}' not found in the departments table.")

    # Create the admission number in the desired format
    admission_number = f"{current_year}-{next_year}/{month}/{dept_code}/{formatted_number}"

    print(admission_number)  # For debugging purposes
    return admission_number


def index(request):
    user_data = request.session.get('user_data', {})

    if request.method == 'POST':
        form = Index(request.POST)
        if form.is_valid():
            # Generate a unique admission number
            admissionno = generate_unique_admission_number(request)

            # Store form data in the session if needed
            request.session['index'] = form.cleaned_data
            request.session['index']['date_of_birth'] = form.cleaned_data['date_of_birth'].isoformat()

            # Redirect to the personal page
            return redirect('personal')
        else:
            context = {'form': form, 'return_url': reverse('index')}
            return render(request, 'application/error.html', context)

    else:
        form = Index()

    context = {
        'form': form,
        'name': user_data.get('name', 'Guest'),
        'Department': user_data.get('Department', 'Not Assigned'),
        'role': user_data.get('role', 'Not Assigned'),
    }

    return render(request, 'application/index.html', context)


def personal(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = Personal_Detail(request.POST)
        if form.is_valid():


            # Optional: If you need to store any information in the session
            request.session['personal_data'] = form.cleaned_data

            # Redirect to the next form or page
            return redirect('School_form')  # Replace with the actual URL name for the next page
        else:
            context = {'form': form, 'return_url': reverse('personal')}
            return render(request, 'application/error.html', context)

    else:
        form = Personal_Detail()
    context = {
        'form' : form,
        'name' : user_data.get('name'),
        'department' : user_data.get('Department'),
        'role' : user_data.get('role')
    }
    return render(request, 'application/personal.html', context)

import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages

def School_form(request):
    user_data = request.session.get('user_data', {})

    # Path to the CSV file
    excel_file_path = 'C:/Users/Administrator/Downloads/Phd-admission-main/Phd-admission-main/df.csv'

    # Read the CSV file and handle errors if the file is empty
    try:
        df = pd.read_csv(excel_file_path)
    except pd.errors.EmptyDataError:
        # Handle the case where the CSV file is empty by creating an empty DataFrame
        df = pd.DataFrame(columns=['School_Name'])

    # Extract the school names from the 'School_Name' column into a list
    school_names = df['School_Name'].tolist()

    if request.method == 'POST':
        form = SchoolDetailsForm(request.POST)
        if form.is_valid():

            # Optional: If you need to store any information in the session
            request.session['School_data'] = form.cleaned_data
            index = request.session.get('index', {})
            highest_qualification = index.get('highest_qualification')

            print("Highest Qualification:", highest_qualification)  # Debugging line
            if highest_qualification == "Bachelor's":
                return redirect('bachelor')
            else:
                return redirect('Masterform')

        else:
            context = {'form': form, 'return_url': reverse('School_form')}
            return render(request, 'application/error.html', context)

    else:
        form = Personal_Detail()

    context = {
        'form': form,
        'name': user_data.get('name'),
        'department': user_data.get('Department'),
        'role': user_data.get('role'),
        'school_names': school_names,  # Pass the school names to the template
    }

    return render(request, 'application/School_form.html', context)

def bachelor(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = BachelorEducationForm(request.POST)
        if form.is_valid():


            # Optional: If you need to store any information in the session
            request.session['bachelor_data'] = form.cleaned_data

            # Redirect to the next form or page
            return redirect('experience')  # Replace with the actual URL name for the next page
        else:
            context = {'form': form, 'return_url': reverse('bachelor')}
            return render(request, 'application/error.html', context)

    else:
        form = BachelorEducationForm()

    context = {
        'form' : form,
        'name' : user_data.get('name'),
        'department' : user_data.get('Department'),
        'role' : user_data.get('role')

    }
    return render(request, 'application/Bachelor.html', {'form': form})


from decimal import Decimal

def Masterform(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = Master(request.POST)
        if form.is_valid():
            # Convert Decimal fields to string or float before saving to session
            master_data = form.cleaned_data

            for key, value in master_data.items():
                if isinstance(value, Decimal):
                    master_data[key] = float(value)  # or str(value) if you prefer strings

            # Store the serialized master_data in session
            request.session['master_data'] = master_data

            # Redirect to the next form or page
            return redirect('experience')  # Replace with the actual URL name for the next page
        else:
            context = {'form': form, 'return_url': reverse('Masterform')}
            return render(request, 'application/error.html', context)

    else:
        form = Master()

    context = {
        'form': form,
        'name': user_data.get('name'),
        'department': user_data.get('Department'),
        'role': user_data.get('role')
    }
    return render(request, 'application/Master.html', context)


def experience(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = ProfessionalExperienceForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            # experience_detail_instance = form.save()
            # Optional: If you need to store any information in the session
            request.session['experience_data'] = form.cleaned_data
            print(request.session.get('experience_data'),'-'*10)
            # Redirect to the next form or page
            return redirect('guide_view')  # Replace with the actual URL name for the next page
        else:
            context = {'form': form, 'return_url': reverse('experience')}
            return render(request, 'application/error.html', context)
    else:
        form = ProfessionalExperienceForm()
    context = {
        'form' : form,
        'name' : user_data.get('name'),
        'department' : user_data.get('Department'),
        'role' : user_data.get('role')

    }
    return render(request, 'application/experience.html', {'form': form})


def guide_view(request):
    user_data = request.session.get('user_data', {})
    if request.method == 'POST':
        form = GuideDetailsForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            # guide_detail_instance = form.save()

            # Optional: If you need to store any information in the session
            request.session['guide_data'] = form.cleaned_data

            # Redirect to the next form or page
            return redirect('dc_member_view')  # Replace with the actual URL name for the next page
        else:
            context = {'form': form, 'return_url': reverse('guide_view')}
            return render(request, 'application/error.html', context)

    else:
        form = GuideDetailsForm()
    context = {
        'form' : form,
        'name' : user_data.get('name'),
        'department' : user_data.get('Department'),
        'role' : user_data.get('role')

    }
    return render(request, 'application/guide.html', {'form': form})


def dc_member_view(request):
    user_data = request.session.get('user_data', {})
    index = request.session.get('index', {})
    personal_data = request.session.get('personal_data', {})
    School_data = request.session.get('School_data', {})
    bachelor_data = request.session.get('bachelor_data', {})
    master_data = request.session.get('master_data', {})
    experience_data = request.session.get('experience_data', {})
    guide_data = request.session.get('guide_data', {})


    print(index,personal_data,School_data,bachelor_data,master_data,experience_data,guide_data)

    if request.method == 'POST':
        form = DCMemberForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            app_no=generate_unique_admission_number(request)
            # Optional: If you need to store any information in the session
            request.session['dc_member_data'] = form.cleaned_data
            dc_member_data = request.session.get('dc_member_data', {})
            ApplicationDetails.objects.create(**index, application_no=app_no)
            PersonalDetails.objects.create(**personal_data, application_no=app_no)
            BachelorEducationDetails.objects.create(**bachelor_data, application_no=app_no)
            MasterEducationDetails.objects.create(**master_data, application_no=app_no)
            SchoolDetails.objects.create(**School_data, application_no=app_no)
            Experience_Details.objects.create(**experience_data, application_no=app_no)
            GuideDetails.objects.create(**guide_data, application_no=app_no)
            DCMember.objects.create(**dc_member_data, application_no=app_no)
            approver.objects.create(application_no=app_no,
                                    coordinate_approval="Pending",
                                    hod_approval='Pending',
                                    vp_approval="Pending",
                                    principal_approval='Pending')

            print(dc_member_data)

            # Redirect to the next form or page
            return redirect('display_qrcode')  # Replace with the actual URL name for the next page
        else:
            context = {'form': form, 'return_url': reverse('dc_member_view')}
            return render(request, 'application/error.html', context)

    else:
        form = DCMemberForm()
    context = {
        'form' : form,
        'name' : user_data.get('name'),
        'department' : user_data.get('Department'),
        'role' : user_data.get('role')

    }
    return render(request, 'application/Dcmember.html', {'form': form})



def approval_view(request):
    print("Testing1")
    user_data=request.session.get('user_data', {})
    staff_role=user_data['role']
    user_dept=user_data['Department']
    print(staff_role,user_dept,"DJFISAHFKUASHF")
    selected_department = request.GET.get('department', None)
    print(selected_department,"fdsafjshdf")
    if selected_department:
        application = ApplicationDetails.objects.filter(department=selected_department)
        if staff_role == "HOD":
            doc={'data':[],'message':[]}
            for app in application:
                documnet=approver.objects.filter(application_no=app.application_no,hod_approval="Pending",vp_approval="Pending",principal_approval="Pending").exclude(coordinate_approval="Pending").first()

                if documnet:
                    doc_data=ApplicationDetails.objects.get(application_no=documnet.application_no)
                    if user_dept==doc_data.department:
                        print("rghfgfgfgfgf")
                        doc['data'].append(doc_data)
                        doc['message'].append(doc_data.application_no)
                    else:
                        doc['data'].append(app)
                        doc['message'].append(None)
                else:
                        doc['data'].append(app)
                        doc['message'].append(None)
            applications=doc
        if staff_role=="Principal":
            doc={'data':[],'message':[]}
            for app in application:
                documnet=approver.objects.filter(application_no=app.application_no,principal_approval="Pending").exclude(vp_approval="Pending",hod_approval="Pending",coordinate_approval="Pending").first()
                if documnet:
                    doc_data=get_object_or_404(ApplicationDetails,application_no=documnet.application_no)

                    doc['data'].append(doc_data)
                    doc['message'].append(doc_data.application_no)
                else:
                    doc['data'].append(app)
                    doc['message'].append(None)

            applications=doc

        if staff_role=="vice_principal":
            doc={'data':[],'message':[]}
            for app in application:
                documnet=approver.objects.filter(application_no=app.application_no,vp_approval="Pending").exclude(hod_approval="Pending",coordinate_approval="Pending").first()
                if documnet:
                    doc_data=get_object_or_404(ApplicationDetails,application_no=documnet.application_no)

                    doc['data'].append(doc_data)
                    doc['message'].append(doc_data.application_no)
                else:
                    doc['data'].append(app)
                    doc['message'].append(None)
            applications=doc

        if staff_role =="Coordinator":
            doc={'data':[],'message':[]}
            for app in application:
                print(app.application_no)
                documnet=approver.objects.filter(application_no=app.application_no,coordinate_approval="Pending").first()
                print(documnet.application_no,"fdshfsagfjgs")

                if documnet:
                    doc_data=get_object_or_404(ApplicationDetails,application_no=documnet.application_no)

                    doc['data'].append(doc_data)
                    doc['message'].append(doc_data.application_no)
                else:
                    doc['data'].append(app)
                    doc['message'].append(None)
            # else:
            #     for app in application:
            #         doc.append()\
            applications=doc
            print(doc,"fhjsadjskafjks")
    elif selected_department=="All" or selected_department==None:
        print("sdfkjas")
        if staff_role=="Principal":
            doc={'data':[],'message':[]}

            documnet=approver.objects.filter(principal_approval="Pending").exclude(vp_approval="Pending")
            print(documnet,"sdakfhkasjdhfjks")

            count=documnet.count()
            print(documnet,count,"dvshjkgdfg")


            if documnet:

                print("fsdfjkdjdshgjfd")
                for app in documnet:
                    print(app.application_no,"dsjfkdjshkhdsg")

                    doc_data=get_object_or_404(ApplicationDetails,application_no=app.application_no)

                    if doc_data not in doc['data']:
                        doc['data'].append(doc_data)
                        doc['message'].append(doc_data.application_no)
                else:
                    if doc_data not in doc['data']:
                        doc['data'].append(doc_data)
                        doc['message'].append(None)
            applications=doc
            print("fdshjkashja",applications)
        if staff_role=="vice_principal":
            doc={'data':[],'message':[]}

            documnet=approver.objects.filter(vp_approval="Pending").exclude(hod_approval="Pending")
            count=documnet.count()
            print(documnet,count,"dvshjkgdfg")


            if documnet:

                print("fsdfjkdjdshgjfd")
                for app in documnet:
                    print(app.application_no,"dsjfkdjshkhdsg")

                    doc_data=get_object_or_404(ApplicationDetails,application_no=app.application_no)

                    print("rghfgfgfgfgf")
                    if doc_data not in doc['data']:
                        doc['data'].append(doc_data)
                        doc['message'].append(doc_data.application_no)
                else:
                   if doc_data not in doc['data']:
                        doc['data'].append(doc_data)
                        doc['message'].append(None)
            applications=doc

        if staff_role =="Coordinator":
            doc={'data':[],'message':[]}

            documnet=approver.objects.filter(coordinate_approval="Pending")
            count=documnet.count()
            print(documnet,count,"dvshjkgdfg")


            if documnet:

                print("fsdfjkdjdshgjfd",documnet)
                for app in documnet:
                    print(app.application_no,"dsjfkdjshkhdsg")

                    doc_data=get_object_or_404(ApplicationDetails,application_no=app.application_no)
                    if doc_data not in doc['data']:
                        doc['data'].append(doc_data)
                        doc['message'].append(doc_data.application_no)
                else:
                    if doc_data not in doc['data']:
                        doc['data'].append(doc_data)
                        doc['message'].append(None)


            else:
                doc=None
            applications=doc
        if staff_role == "HOD":
            doc={'data':[],'message':[]}

            documnet=approver.objects.filter(hod_approval="Pending").exclude(coordinate_approval="Pending")

            if documnet:
                print("fsdfjkdjdshgjfd")
                for app in documnet:
                    print(app.application_no,"dsjfkdjshkhdsg")

                    doc_data=get_object_or_404(ApplicationDetails,application_no=app.application_no)

                    print("rghfgfgfgfgf")
                    if doc_data not in doc['data']:
                        doc['data'].append(doc_data)
                        doc['message'].append(doc_data.application_no)
                else:
                    if doc_data not in doc['data']:
                        doc['data'].append(doc_data)
                        doc['message'].append(None)
            else:
                doc=None
            applications=doc
    else:
        applications=None

    context = {
        'applications': applications,
        'selected_department': selected_department,
        'role':staff_role,
        'dept':user_dept,

    }
    print(applications,"hfdsjkhfjkshfkhd")

    return render(request, 'application/Approve.html', context)

def approving(request):
    print("fdslhfksjahdfjk")
    user_data=request.session.get('user_data', {})
    staff_role=user_data['role']
    user_dept=user_data['Department']
    appliction_no= request.GET.get("application_no")
    print(appliction_no,"fdshfkjasfkjg")
    data=get_object_or_404(approver,application_no=appliction_no)

    if data:
        if staff_role=="Coordinator":
            data.coordinate_approval="Approved"
            data.save()
        if staff_role=="HOD":
            print("dsagdasgfhsadfh")
            data.hod_approval="Approved"
            data.save()
        if staff_role=="vice_principal":
            print("dsagdasgfhsadfh")
            data.vp_approval="Approved"
            data.save()
        if staff_role=="Principal":
            print("dsagdasgfhsadfh")
            data.principal_approval="Approved"
            data.save()
        return redirect('approval_view')



def PhD_Status(request):
    if request.method == 'POST':
        form = Status_form(request.POST)
        if form.is_valid():
            form.save()  # Save the instance to the database
            return redirect('success_page')  # Replace 'success_page' with your actual success page URL name
    else:
        form = Status_form()
    return render(request, 'application/PhD_Status.html', {'form': form})



def encrypt_password(raw_password):
    # Implement your password encryption algorithm (e.g., using hashlib)
    import hashlib
    return hashlib.sha256(raw_password.encode()).hexdigest()


def defaultUser(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        department = request.POST.get('Department')
        email = request.POST.get('email')
        role = request.POST.get('role')

        # Save the data to the Staff model
        data=defaultUsers.objects.create(
            staff_id=staff_id,
            Department=department,
            email=email,
            role=role
        )
        data.save()
        return redirect('login')  # Redirect to login or another page after saving

    return render(request, 'application/adduser.html')


def signup(request):
        if request.method == 'POST':
            form = userform(request.POST)
            if form.is_valid():
                password = form.cleaned_data['Password']
                confirm_password = form.cleaned_data['confirm_Password']

                if password == confirm_password:
                    encrypted_password = encrypt_password(password)

                    # Get the staff_id, department, email, and role from the form
                    staff_id = form.cleaned_data['staff_id']
                    department = form.cleaned_data['Department']
                    email = form.cleaned_data['email']
                    role = form.cleaned_data['role']

                    # Check if the values exist in the defaultUsers table
                    if defaultUsers.objects.filter(
                        staff_id=staff_id,
                        Department=department,
                        email=email,
                        role=role
                    ).exists():
                        # Values match, save to the User table
                        user = form.save(commit=False)  # Don't save the form yet
                        user.Password = encrypted_password
                        user.confirm_Password = encrypted_password

                        user.save()

                        # Redirect to a success page or login page
                        return redirect('login')
                    else:
                        # Show an error if no matching records found
                        messages.error(request, "The provided details do not match any existing records.")
                        return render(request, "auth/signup.html", {'form': form})
                else:
                    # Passwords don't match, return an error
                    form.add_error('confirm_Password', 'Passwords do not match')
                    return render(request, "auth/signup.html", {'form': form})
            else:
                return render(request, "application/error.html", {'form': form})
        else:
            form = userform()

        return render(request, "auth/signup.html", {'form': form})

def scholar_signup(request):
    if request.method == 'POST':
        form = ScholarForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['Password']
            confirm_password = form.cleaned_data['confirm_Password']

            if password == confirm_password:
                # Encrypt the password
                encrypted_password = encrypt_password(password)

                # Save the encrypted password to the model
                scholar = form.save(commit=False)
                scholar.Password = encrypted_password
                scholar.confirm_Password = encrypted_password
                scholar.save()

                messages.success(request, "Scholar registered successfully!")
                return redirect('login')  # Redirect to login or any other page
            else:
                form.add_error('confirm_Password', 'Passwords do not match.')
    else:
        form = ScholarForm()

    return render(request, 'Auth/scholar_signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        password = request.POST.get('password')
        print(staff_id, password)

        # Fetch the user from Scholar table
        try:
            user = Scholar.objects.get(user_name=staff_id)

            # Fetch user_name from ApplicationDetails if needed
            try:
                user_name = ApplicationDetails.objects.get(name=staff_id)
            except ApplicationDetails.DoesNotExist:
                user_name = None

            if user_name and user_name.name == user.user_name:
                print('Username exists in both Scholar and ApplicationDetails.')
                return render(request, "application/PhD_Status.html")

            # Check if the password matches (assuming encrypt_password is a valid function)
            if user.Password == encrypt_password(password):
                # Set session data
                request.session['user_name'] = user.user_name
                user_dict = {
                    'user_name': user.user_name,
                    'Department': user.Department,
                    'email': user.email_id,
                    'register_number': user.register_number,
                    'Password': user.Password,
                    'confirm_Password': user.confirm_Password,
                }
                request.session['user_data'] = user_dict
                return redirect('index')
            else:
                # Password does not match
                error_message = 'Invalid password.'
                return render(request, "Auth/login.html", {'error_message': error_message})

        # If Scholar user does not exist, check User table
        except Scholar.DoesNotExist:
            try:
                print("akakakaka")
                # Attempt to fetch user from User table
                user = User.objects.get(staff_id=staff_id)

                # Check password and set session data
                if user.Password == encrypt_password(password):
                    request.session['user_id'] = user.staff_id
                    user_dict = {
                        'staff_id': user.staff_id,
                        'name': user.Name,
                        'user_name': user.user_name,
                        'Department': user.Department,
                        'email': user.email,
                        'role': user.role,
                        'Password': user.Password,
                        'confirm_Password': user.confirm_Password
                    }
                    request.session['user_data'] = user_dict
                    return redirect('approval_view')
                else:
                    error_message = 'Invalid password.'
                    return render(request, "Auth/login.html", {'error_message': error_message})

            except User.DoesNotExist:
                # Neither Scholar nor User found
                error_message = 'Invalid staff_id or password.'
                return render(request, "Auth/login.html", {'error_message': error_message})

    return render(request, "Auth/login.html")

def logout(request):

    print('logout function called')
    auth_logout(request)
    messages.success(request,'You were logged out')
    request.session.flush()  # Flush all session data
    return render(request, "auth/login.html")
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from io import BytesIO  # Add this import statement
import os

def generate_pdf(request):
    register_number=request.GET.get('reg_no')
    print(register_number,"sahfkjshfkjdasghfjg")
    buffer = BytesIO()
    Register = ApplicationDetails.objects.get(register_number=register_number)
    application_no = Register.application_no
    print(application_no)

    # Fetch PersonalDetails based on the application_no
    personal = PersonalDetails.objects.filter(application_no=application_no).first()
    bachelor = BachelorEducationDetails.objects.filter(application_no=application_no).first()
    master = MasterEducationDetails.objects.filter(application_no=application_no).first()
    dc = DCMember.objects.filter(application_no=application_no).first()
    guide = GuideDetails.objects.filter(application_no=application_no).first()
    school = SchoolDetails.objects.filter(application_no=application_no).first()
    experience = Experience_Details.objects.filter(application_no=application_no).first()
    print(experience.start_year1)
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)

    # Draw the content on the PDF
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 30, "APPLICATION FOR ADMISSION TO Ph.D. PROGRAMMES")
    
    # Reference and Application Numbers
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, height - 117, "Reference No.:")
    p.drawString(124,height-115,Register.application_no)
    p.line(123 , height - 117 , 200, height - 117)
    p.drawString(350, height - 117, "Application No.:")
    p.line(430 , height - 117 , 570, height - 117)
    p.drawString(431, height - 115 , Register.application_no)
    # Research Department Information
    p.drawString(50, height - 130, "Name of the Research Department:")
    p.line(220 , height - 130 , 340, height - 130)
    p.drawString(220, height-130 ,Register.department)
    p.drawString(350, height - 130, "AU Research centre recognition no:")
    
    
    p.drawString(50, height - 143, "Name and Designation of the research supervisor at RIT:")
    p.line(320 , height - 145 , 580, height - 145)
    p.drawString(50, height - 155, "Area of Research: ")
    p.drawString(139,height-153,Register.area_research)
    p.line(137 , height - 157 , 300, height - 157)
    p.drawString(350, height - 155, "Ph.D. Register No: ")
    p.drawString(440,height-155,Register.register_number)
    
    p.rect(40, height - 305, 530, 140)


    # Applicant Information
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, height - 180, " Name:")
    p.line(100 , height - 180 , 350, height - 180)
    p.drawString(101,height-178,Register.name)
    p.drawString(300, height - 195, " Age:")
    p.line(330 , height - 180 , 450, height - 180)
    p.drawString(330,height-196,str(Register.age))
    p.drawString(50, height - 195, " Date of Birth:")
    p.rect(120, height - 200, 150, 15)
    p.drawString(140,height-195,str(Register.date_of_birth))
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, height - 215, " Address for communication:")
    p.line(50 , height - 230 , 250, height - 230)
    p.drawString(55,height-228,personal.permanent_address_street_name)
    p.drawString(55,height-241,personal.permanent_address_state)
    p.drawString(268,height-228,personal.communication_address_location)
    p.drawString(268,height-241,personal.communication_address_state)
    p.line(50 , height - 245 , 250, height - 245)
    p.drawString(50, height - 260, " Pincode:")
    p.rect(100, height - 265, 150, 15)
    p.drawString(105,height-260,str(personal.permanent_address_pincode))
    p.drawString(316,height-260,str(personal.communication_address_pincode))
    # p.drawString(50, height - 275, " Mobile No:")
    # p.line(100 , height - 280 , 250, height - 280)
    # p.drawString(105,height-278,personal.mobile_number)
    # p.drawString(315,height-278,personal.mobile_number)
    p.drawString(50, height - 275, " Mail id:")
    p.line(100 , height - 280 , 250, height - 280)
    p.drawString(105,height-278,Register.self_email_id)
    
    
    
    p.drawString(260, height - 215, " Permanent Address:")
    p.line(260 , height - 230 , 450, height - 230)
    p.line(260 , height - 245 , 450, height - 245)
    p.drawString(260, height - 260, " Pincode:")
    p.rect(310, height - 265, 140, 15)
    p.drawString(260, height - 275, " Mobile No:")
    p.line(310 , height - 280 , 450, height - 280)
    p.drawString(315,height-278,personal.mobile_number)
    # p.drawString(260, height - 290, " Mail id:")
    # p.line(295 , height - 295 , 450, height - 295)


    p.rect(40, height - 330, 530, 25)
    p.drawString(50, height - 320, " Types of Registration:")
    p.rect(40, height - 465, 530, 110)
    p.drawString(170,height-320,Register.type_of_registration)
    
    p.drawString(50, height - 350, " School Details")

    p.drawString(230, height - 370, " SSLC:")
    p.drawString(440, height - 370, " HSC:")
    p.line(40 , height - 375 , 570, height - 375)
    p.line(40 , height - 390 , 570, height - 390)
    p.line(40 , height - 405 , 570, height - 405)
    p.line(40 , height - 420 , 570, height - 420)
    p.line(40 , height - 435 , 570, height - 435)
    p.line(40 , height - 450 , 570, height - 450)
    
    p.line(130 , height - 355 , 130, height - 465)
    p.line(350 , height - 355 , 350, height - 465)
    


    p.drawString(50 ,height - 385, " School" )
    p.drawString(140,height-388,school.school_name_10th)
    p.drawString(358,height-388,school.school_name_12th)

    p.drawString(50 ,height - 400, " Year of passing" )
    p.drawString(140,height-403,str(school.year_of_passing_10th))
    p.drawString(358,height-403,str(school.year_of_passing_12th))
    
    p.drawString(50 ,height - 415, " Studied In" )
    p.drawString(140,height-418,school.std_studied_in_10th)
    p.drawString(358,height-418,school.std_studied_in_12th)
    
    p.drawString(50 ,height - 430, " Medium of Study" )
    p.drawString(140,height-433,school.medium_of_study_10th)
    p.drawString(358,height-433,school.medium_of_study_12th)
    
    p.drawString(50 ,height - 445, " Type of Study" )
    p.drawString(140,height-448,school.school_type_10th)
    p.drawString(358,height-448,school.school_type_12th)
    
    p.drawString(50 ,height - 460, " Total Mark" )
    p.drawString(140,height-463,str(school.total_mark_10th))
    p.drawString(358,height-463,str(school.total_mark_12th))
    
    
    
    p.drawString(50, height - 490, " Higher Studies")
    p.rect(40, height - 635, 530, 140)

    p.drawString(230, height - 510, " Bachelors")
    p.drawString(440, height - 510, " Masters")
    p.line(40 , height - 515 , 570, height - 515)
    p.line(40 , height - 535 , 570, height - 535)
    p.line(40 , height - 555 , 570, height - 555)
    p.line(40 , height - 575 , 570, height - 575)
    p.line(40 , height - 595 , 570, height - 595)
    p.line(40 , height - 615 , 570, height - 615)
    
    p.line(130 , height - 635 , 130, height - 495)
    p.line(350 , height - 635 , 350, height - 495)
    
    p.drawString(50 ,height - 530, " Degree" )
    p.drawString(358,height-533,master.master_degree)
    
    
    p.drawString(50 ,height - 550, " Branch" )
    p.drawString(358,height-553,master.master_discipline)
    
    p.drawString(50 ,height - 570, " University" )
    p.drawString(358,height-573,master.master_university)
    
    p.drawString(50 ,height - 590, " Year Of Passing" )
    p.drawString(358,height-593,str(master.master_year))
    
    p.drawString(50 ,height - 610, " CGPA" )
    p.drawString(358,height-613,str(master.master_cgpa))
    
    p.drawString(50 ,height - 630, " Class" )
    p.drawString(358,height-633,master.master_class)
    
    p.drawString(50, height - 700, " Professional Experience")
    p.rect(40, height - 800, 530, 90)
    p.line(100 , height - 710 , 100, height - 800)
    p.line(250 , height - 710 , 250, height - 800)
    p.line(350 , height - 710 , 350, height - 800)
    p.line(480 , height - 710 , 480, height - 800)
    p.line(415 , height - 725 , 415, height - 800)
    
    p.line(40 , height - 740 , 570, height - 740)
    p.line(40 , height - 760 , 570, height - 760)
    p.line(40 , height - 780 , 570, height - 780)
    p.line(350 , height - 725 , 480, height - 725)

    p.drawString(60 ,height - 730, " Area" )
    p.drawString(140 ,height - 730, " Organization" )
    p.drawString(112,height-755,experience.name_of_the_organization1)
    p.drawString(112,height-776,experience.name_of_the_organization2)
    p.drawString(112,height-796,experience.name_of_the_organization3)
    p.drawString(270 ,height - 730, " Designation" )
    p.drawString(275,height-756,experience.designation1)
    p.drawString(275,height-776,experience.designation2)
    p.drawString(275,height-796,experience.designation3)
    p.drawString(395 ,height - 720, " Period" )
    p.drawString(510 ,height - 730, " Nature" )
    p.drawString(482,height-757,experience.nature_of_work1)
    p.drawString(482,height-776,experience.nature_of_work2)
    p.drawString(482,height-796,experience.nature_of_work3)
    p.drawString(365 ,height - 735, " From" )
    p.drawString(373,height-757,str(experience.start_year1))
    p.drawString(373,height-776,str(experience.start_year2))
    p.drawString(373,height-796,str(experience.start_year3))
    p.drawString(435 ,height - 735, " To" )
    p.drawString(438,height-755,str(experience.to1))
    p.drawString(438,height-776,str(experience.to2))
    p.drawString(438,height-796,str(experience.to3))





    
    # Finalize the PDF
    p.showPage()
    
    p.setFont("Helvetica-Bold", 10)
    p.rect(30 , height - 530 , 540 , 500)
    p.drawString(50, height - 70, "a). Father's /")
    p.drawString(60, height - 80, "Husband Name")
    p.drawString(170,height-73 , personal.father_name)
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, height - 100, "b). Father's / Husband")
    p.drawString(60, height - 110, "Occupation")
    p.drawString(170,height-103 , personal.father_occupation)
    
    p.drawString(50, height - 130, "c). Mother's Name")
    p.drawString(170,height-123,personal.mother_name)
    
    p.drawString(50, height - 150, "d). Place of Brith")
    p.drawString(170,height-143,personal.place_of_birth)
    
    p.drawString(50, height - 170, "e). Mother Tongue")
    p.drawString(170,height-163, personal.mother_tongue)
    
    p.drawString(60, height - 190, " Professional")
    p.drawString(50, height - 200, "f). Society")
    p.drawString(60, height - 210, " Membership, if any")
    p.drawString(170,height-193,personal.mother_tongue)


    p.drawString(350, height - 70, "g). Nationality")
    p.drawString(450,height-73,personal.nationality)
    
    p.drawString(350, height - 100, "h). State to which the")
    p.drawString(360, height - 110, " applicant Belongs")
    p.drawString(452,height-108,personal.state_of_origin)

    p.drawString(350, height - 130, "i). Maritial Status")
    p.drawString(450,height-128,personal.marital_status)

    p.drawString(350, height - 150, "j). Gender:")
    p.drawString(450,height-148,personal.gender)

    p.drawString(350, height - 170, "k). Whethere appeared in GATE:")
    p.drawString(505,height-170,personal.appeared_in_gate)

    p.drawString(350, height - 190, "l). Whethere Physically Challenged:")
    p.drawString(520,height-190,personal.physically_challenged)

    p.line(170 , height - 75 , 330, height - 75)
    p.line(170 , height - 105 , 330, height - 105)
    p.line(170 , height - 125 , 330, height - 125)
    p.line(170 , height - 145 , 330, height - 145)
    p.line(170 , height - 165 , 330, height - 165)
    p.line(170 , height - 195 , 330, height - 195)
    p.line(450 , height - 75 , 560, height - 75)
    p.line(450 , height - 110 , 560, height - 110)
    p.line(450 , height - 130 , 560, height - 130)
    p.line(450 , height - 150 , 560, height - 150)
    
    p.drawString(50, height - 230, "Consent of the Supervisor / Joint Supervisor")
    p.drawString(50, height - 400, "Details of DC Members")



    p.rect(40, height - 385, 520, 145)
    p.line(40 , height - 255 , 560, height - 255)
    p.line(40 , height - 270 , 560, height - 270)
    p.line(40 , height - 285 , 560, height - 285)
    p.line(40 , height - 310 , 560, height - 310)
    p.line(40 , height - 325 , 560, height - 325)
    p.line(40 , height - 340 , 560, height - 340)
    p.line(40 , height - 370 , 560, height - 370)
    p.line(180 , height - 240 , 180, height - 385)
    p.line(380 , height - 240 , 380, height - 385)

    p.drawString(70, height - 250, "Particulars")
    p.drawString(230, height - 250, "Research Guide")
    p.drawString(430, height - 250, "Co-Guide")

    p.setFont("Helvetica", 10)

    p.drawString(50, height - 265, "Name")
    p.drawString(190,height-266,guide.guide_name)
    p.drawString(400,height-266,guide.co_guide_name)
    p.drawString(50, height - 280, "Designation")
    p.drawString(190,height-281,guide.guide_designation_and_department[:27])
    
    p.drawString(190,height-291,guide.guide_designation_and_department[27:])
    p.drawString(400,height-281,guide.co_guide_designation_and_department[:27])
    p.drawString(400,height-291,guide.co_guide_designation_and_department[27:])
    p.drawString(50, height - 295, "Anna University Research")
   
    p.drawString(50, height - 305, "Recongnition number")
    p.drawString(190,height-301,guide.guide_recognition_number)
    p.drawString(400,height-301,guide.co_guide_recognition_number)
    p.drawString(50, height - 320, "College/Organizaton Address")
    p.drawString(190,height-321,guide.guide_college_organization_address)
    p.drawString(400,height-321,guide.co_guide_college_organization_address)
    p.drawString(50, height - 335, "Area of Research")
    
    p.drawString(50, height - 350, "Number of Research")
    
    p.drawString(50, height - 365, "Scholars")
    
    p.drawString(50, height - 380, "Signature")
   

    p.setFont("Helvetica-Bold", 10)
    
    
    p.rect(40, height - 510, 520, 100)
    p.line(40 , height - 430 , 560, height - 430)
    p.line(40 , height - 450 , 560, height - 450)
    p.line(40 , height - 470 , 560, height - 470)
    p.line(40 , height - 490 , 560, height - 490)
    p.line(180 , height - 410 , 180, height - 510)
    p.line(380 , height - 410 , 380, height - 510)


    p.drawString(70, height - 425, "Particulars")
    p.drawString(230, height - 425, "DC Member 1")
    p.drawString(430, height - 425, "DC Member 2")
    p.drawString(50, height - 445, "Name")
    p.drawString(190,height-444,dc.name1)
    p.drawString(400,height-444,dc.name2)
    p.drawString(50, height - 465, "Desgination")
    p.drawString(190,height-464,dc.designation_and_department1)
    p.drawString(400,height-464,dc.designation_and_department2)
    p.drawString(50, height - 485, "OrganiZation Address")
    p.drawString(190,height-484,dc.college_organization_address1)
    p.drawString(400,height-484,dc.college_organization_address1)
    p.drawString(50, height - 505, "Area Of Research")
    p.drawString(190,height-504,dc.area_of_research1)
    p.drawString(400,height-504,dc.area_of_research2)



    p.drawString(250, height - 560, "DECLARATION")
    
    p.setFont("Helvetica", 10)

    p.drawString(100, height - 575, "I hereby declare that all the information provided in this application for admission to the Ph.D.")
    p.drawString(70, height - 585, "programme is accurate and truthful to the best of my knowledge.")
    p.drawString(100, height - 605, "I commit to upholding the highest standards of academic integrity and research ethics as outlined")
    p.drawString(70, height - 615, "in the R&D Policy of Ramco Institute of Technology.")



    # End the second page
    p.showPage()
    p.save()

    # Get the value of the buffer and close it
    pdf = buffer.getvalue()
    buffer.close()

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="{}.pdf"'   # This will prompt a download

    return response



    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="e_approval.pdf"'
    response.write(pdf)
    return response





import qrcode


# URL to encode in the QR code
QR_URL = "http://172.16.71.76:8000/Dcmembers/check_register_number"

def generate_qrcode(request):
    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(QR_URL)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Save the image in memory
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response



def display_qrcode(request):
    context = {'qr_url': QR_URL}
    return render(request, 'application/display_qrcode.html', context)




# import tkinter as tk
# from tkinter import messagebox


def check_register_number(request):
    if request.method == 'POST':
        register_number = request.POST.get('register_number')
        if ApplicationDetails.objects.filter(register_number=register_number).exists():
            return redirect('upload_image',register_number)
        else:
            return HttpResponse("Register number does not exist.")
    return render(request, 'application/check_register_number.html')




def edit_form(request):
    return render(request, 'application/edit_form.html')



def check_form(request):
    if request.method == 'POST':
        register_number = request.POST.get('register_number')
        if ApplicationDetails.objects.filter(register_number=register_number).exists():
            return redirect('upload_image', register_number=register_number)
        else:
            return HttpResponse("Register number does not exist.")

    return render(request, 'application/RegisterNumber.html')


# -----------------------------------------

def save_uploaded_images(file_dict, admission_number):

    # Use current year if 'year' is not provided
    year = datetime.now().year
    profile_images_directory = os.path.join(settings.MEDIA_ROOT, 'profile_images', str(year), str(admission_number))
    os.makedirs(profile_images_directory, exist_ok=True)

    file_paths = {}

    for field_name, file_obj in file_dict.items():
        base_file_name = f'{admission_number}_{field_name}_{file_obj.name}'
        file_path = os.path.join(profile_images_directory, base_file_name)

        # Check if the file already exists, if yes, append a number
        counter = 1
        while os.path.exists(file_path):
            new_file_name = f'{admission_number}_{field_name}_{counter}_{file_obj.name}'
            file_path = os.path.join(profile_images_directory, new_file_name)
            counter += 1

        with open(file_path, 'wb') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        # Store relative path to media root
        file_paths[field_name] = os.path.relpath(file_path, settings.MEDIA_ROOT)

    return file_paths

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .form import UploadImageForm
from .models import ApplicationDetails

def upload_image(request, register_number):
    print(register_number)
    application = ApplicationDetails.objects.get(register_number=register_number)

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            # Save the image in the appropriate folder
            folder_path = f"{application.register_number}/"
            image_instance.image.name = folder_path + image_instance.image.name
            image_instance.application = application
            image_instance.save()
            return HttpResponse("Image is Uploaded Successfully")  # Replace with your success URL
    else:
        form = UploadImageForm()

    return render(request, 'application/upload_image.html', {'form': form, 'application': application})


def delete_old_image(image_field):
    if image_field:
        image_path = image_field.path
        if os.path.exists(image_path):
            os.remove(image_path)


# def upload_images(request, Aadhaar_Number):
#     form_update = get_object_or_404(ApplicationDetails, register_number=register_number)
#     Name = form_update.Name
#     Department = form_update.Department
#     Quota = form_update.Quota

#     if request.method == 'POST':
#         form = UploadImagesForm(request.POST, request.FILES)
#         if form.is_valid():
#             file_paths = save_uploaded_images(request.FILES, Aadhaar_Number)

#             if 'image' in file_paths:
#                 old_profile_image = form_update.image
#                 form_update.image = file_paths.get('image')
#                 delete_old_image(old_profile_image)



#             form_update.save()

#             return render(request, "image/success.html", {'Name': Name, 'Department': Department, 'Quota': Quota})
#         else:
#             return render(request, "postform/error.html", {'form': form})
#     else:
#         form = UploadImagesForm()
#     return render(request, "image/image_form.html", {'form': form, 'Aadhaar_Number': Aadhaar_Number})
def admin_portal(request):
    return(request)