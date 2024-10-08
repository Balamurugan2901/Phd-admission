# Generated by Django 4.2.5 on 2024-09-23 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationDetails',
            fields=[
                ('application_no', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('self_email_id', models.EmailField(blank=True, max_length=255, null=True)),
                ('type_of_registration', models.CharField(blank=True, max_length=500, null=True)),
                ('highest_qualification', models.CharField(blank=True, max_length=500, null=True)),
                ('department', models.CharField(blank=True, max_length=200, null=True)),
                ('research_supervisor', models.CharField(blank=True, max_length=200, null=True)),
                ('register_number', models.CharField(max_length=250, unique=True)),
                ('area_research', models.CharField(blank=True, max_length=200, null=True)),
                ('approval', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/')),
            ],
        ),
        migrations.CreateModel(
            name='approver',
            fields=[
                ('application_no', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('coordinate_approval', models.CharField(blank=True, max_length=200, null=True)),
                ('hod_approval', models.CharField(blank=True, max_length=200, null=True)),
                ('vp_approval', models.CharField(blank=True, max_length=200, null=True)),
                ('principal_approval', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BachelorEducationDetails',
            fields=[
                ('application_no', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('bachelor_degree', models.CharField(blank=True, max_length=50, null=True)),
                ('bachelor_discipline', models.CharField(blank=True, max_length=100, null=True)),
                ('bachelor_university', models.CharField(blank=True, max_length=200, null=True)),
                ('bachelor_year', models.IntegerField(blank=True, null=True)),
                ('bachelor_cgpa', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('bachelor_branch', models.CharField(blank=True, max_length=100, null=True)),
                ('bachelor_class', models.CharField(blank=True, max_length=50, null=True)),
                ('bachelor_aggregate', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DCMember',
            fields=[
                ('application_no', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('name1', models.CharField(blank=True, max_length=100, null=True)),
                ('designation_and_department1', models.CharField(blank=True, max_length=100, null=True)),
                ('college_organization_address1', models.CharField(blank=True, max_length=100, null=True)),
                ('area_of_research1', models.CharField(blank=True, max_length=100, null=True)),
                ('name2', models.CharField(blank=True, max_length=100, null=True)),
                ('designation_and_department2', models.CharField(blank=True, max_length=100, null=True)),
                ('college_organization_address2', models.CharField(blank=True, max_length=100, null=True)),
                ('area_of_research2', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='defaultUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', models.CharField(max_length=100)),
                ('Department', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='departments',
            fields=[
                ('dept_code', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('department', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Experience_Details',
            fields=[
                ('application_no', models.CharField(blank=True, max_length=500, primary_key=True, serialize=False)),
                ('professional_experience', models.CharField(max_length=255)),
                ('name_of_the_organization', models.CharField(max_length=255)),
                ('start_year', models.IntegerField()),
                ('end_year', models.IntegerField()),
                ('designation', models.CharField(max_length=255)),
                ('nature_of_work', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GuideDetails',
            fields=[
                ('application_no', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('guide_name', models.CharField(blank=True, max_length=255, null=True)),
                ('guide_designation_and_department', models.CharField(blank=True, max_length=255, null=True)),
                ('guide_recognition_number', models.CharField(blank=True, max_length=50, null=True)),
                ('guide_college_organization_address', models.CharField(blank=True, max_length=500, null=True)),
                ('number_of_research_scholar1', models.CharField(blank=True, max_length=500, null=True)),
                ('co_guide_name', models.CharField(blank=True, max_length=255, null=True)),
                ('co_guide_designation_and_department', models.CharField(blank=True, max_length=255, null=True)),
                ('co_guide_recognition_number', models.CharField(blank=True, max_length=50, null=True)),
                ('co_guide_college_organization_address', models.CharField(blank=True, max_length=500, null=True)),
                ('number_of_research_scholar2', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MasterEducationDetails',
            fields=[
                ('application_no', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('bachelor_degree', models.CharField(blank=True, max_length=50, null=True)),
                ('bachelor_discipline', models.CharField(blank=True, max_length=100, null=True)),
                ('bachelor_university', models.CharField(blank=True, max_length=200, null=True)),
                ('bachelor_year', models.IntegerField(blank=True, null=True)),
                ('bachelor_cgpa', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('bachelor_branch', models.CharField(blank=True, max_length=100, null=True)),
                ('bachelor_class', models.CharField(blank=True, max_length=50, null=True)),
                ('bachelor_aggregate', models.CharField(blank=True, max_length=50, null=True)),
                ('bachelor_others', models.CharField(blank=True, max_length=50, null=True)),
                ('master_degree', models.CharField(blank=True, max_length=10, null=True)),
                ('master_discipline', models.CharField(blank=True, max_length=100, null=True)),
                ('master_university', models.CharField(blank=True, max_length=100, null=True)),
                ('master_year', models.PositiveIntegerField(blank=True, null=True)),
                ('master_cgpa', models.FloatField(blank=True, null=True)),
                ('master_branch', models.CharField(blank=True, max_length=100, null=True)),
                ('master_class', models.CharField(blank=True, max_length=100, null=True)),
                ('master_aggregate', models.CharField(blank=True, max_length=100, null=True)),
                ('master_others', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('application_no', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('permanent_address_door_no', models.CharField(max_length=100)),
                ('permanent_address_street_name', models.CharField(max_length=500)),
                ('permanent_address_location', models.CharField(max_length=500)),
                ('permanent_address_state', models.CharField(max_length=500)),
                ('permanent_address_pincode', models.CharField(max_length=500)),
                ('mobile_number', models.CharField(max_length=10)),
                ('communication_address_door_no', models.CharField(blank=True, max_length=100, null=True)),
                ('communication_address_street_name', models.CharField(blank=True, max_length=500, null=True)),
                ('communication_address_location', models.CharField(blank=True, max_length=500, null=True)),
                ('communication_address_state', models.CharField(blank=True, max_length=500, null=True)),
                ('communication_address_pincode', models.CharField(blank=True, max_length=500, null=True)),
                ('communication_mobile_number', models.CharField(blank=True, max_length=10, null=True)),
                ('father_name', models.CharField(blank=True, max_length=255, null=True)),
                ('father_occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=255, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=255, null=True)),
                ('mother_tongue', models.CharField(blank=True, max_length=255, null=True)),
                ('professional_society_membership', models.CharField(blank=True, max_length=255, null=True)),
                ('nationality', models.CharField(blank=True, max_length=255, null=True)),
                ('state_of_origin', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('marital_status', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('appeared_in_gate', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('physically_challenged', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='phd_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_number', models.CharField(blank=True, max_length=250, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('venue', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scholar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('Department', models.CharField(max_length=100)),
                ('Password', models.CharField(max_length=100)),
                ('confirm_Password', models.CharField(max_length=100)),
                ('email_id', models.EmailField(blank=True, max_length=255, null=True)),
                ('register_number', models.CharField(blank=True, max_length=250, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolDetails',
            fields=[
                ('application_no', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('school_name_10th', models.CharField(blank=True, max_length=255, null=True)),
                ('year_of_passing_10th', models.IntegerField(blank=True, null=True)),
                ('std_studied_in_10th', models.CharField(blank=True, max_length=255, null=True)),
                ('medium_of_study_10th', models.CharField(blank=True, max_length=255, null=True)),
                ('school_type_10th', models.CharField(blank=True, max_length=255, null=True)),
                ('total_mark_10th', models.IntegerField(blank=True, null=True)),
                ('higher_studies', models.CharField(blank=True, max_length=255, null=True)),
                ('school_name_12th', models.CharField(blank=True, max_length=255, null=True)),
                ('year_of_passing_12th', models.IntegerField(blank=True, null=True)),
                ('std_studied_in_12th', models.CharField(blank=True, max_length=255, null=True)),
                ('medium_of_study_12th', models.CharField(blank=True, max_length=255, null=True)),
                ('school_type_12th', models.CharField(blank=True, max_length=255, null=True)),
                ('total_mark_12th', models.IntegerField(blank=True, null=True)),
                ('polytechnic_name', models.CharField(blank=True, max_length=255, null=True)),
                ('year_of_passing_diploma', models.IntegerField(blank=True, null=True)),
                ('studied_in_polytechnic', models.CharField(blank=True, max_length=255, null=True)),
                ('medium_of_study_polytechnic', models.CharField(blank=True, max_length=255, null=True)),
                ('total_mark_polytechnic', models.IntegerField(blank=True, null=True)),
                ('total_percentage_polytechnic', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=100)),
                ('staff_id', models.CharField(max_length=100)),
                ('Department', models.CharField(max_length=100)),
                ('Department_code', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
                ('Password', models.CharField(max_length=100)),
                ('confirm_Password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='applications.applicationdetails')),
            ],
        ),
    ]
