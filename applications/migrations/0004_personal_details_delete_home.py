# Generated by Django 4.2.5 on 2024-08-16 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_home_aggregate_grade_home_branch_home_cgpa_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personal_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Apllication', models.CharField(max_length=500)),
                ('Name', models.CharField(max_length=500)),
                ('age', models.PositiveIntegerField()),
                ('date_of_birth', models.DateField()),
                ('self_email_id', models.EmailField(max_length=255)),
                ('type_of_registration', models.CharField(max_length=500)),
                ('highest_qualification', models.CharField(max_length=500)),
                ('permanent_address_door_no', models.CharField(max_length=100)),
                ('permanent_address_street_name', models.CharField(max_length=500)),
                ('permanent_address_location', models.CharField(max_length=500)),
                ('permanent_address_state', models.CharField(max_length=500)),
                ('permanent_address_pincode', models.CharField(max_length=500)),
                ('mobile_number', models.CharField(max_length=10)),
                ('communication_address_door_no', models.CharField(max_length=100)),
                ('communication_address_street_name', models.CharField(max_length=500)),
                ('communication_address_location', models.CharField(max_length=500)),
                ('communication_address_state', models.CharField(max_length=500)),
                ('communication_address_pincode', models.CharField(max_length=500)),
                ('communication_mobile_number', models.CharField(max_length=500)),
                ('degree', models.CharField(blank=True, choices=[('B.E', 'Part time'), ('B.tech', 'Full Time')], max_length=100, null=True)),
                ('discipline', models.CharField(blank=True, max_length=100, null=True)),
                ('university_college', models.CharField(blank=True, max_length=255, null=True)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('cgpa', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('branch', models.CharField(blank=True, max_length=100, null=True)),
                ('class_field', models.CharField(blank=True, max_length=100, null=True)),
                ('semester_1', models.PositiveIntegerField(blank=True, null=True)),
                ('semester_2', models.PositiveIntegerField(blank=True, null=True)),
                ('semester_3', models.PositiveIntegerField(blank=True, null=True)),
                ('semester_4', models.PositiveIntegerField(blank=True, null=True)),
                ('semester_5', models.PositiveIntegerField(blank=True, null=True)),
                ('semester_6', models.PositiveIntegerField(blank=True, null=True)),
                ('semester_7', models.PositiveIntegerField(blank=True, null=True)),
                ('semester_8', models.PositiveIntegerField(blank=True, null=True)),
                ('aggregate_grade', models.CharField(blank=True, max_length=100, null=True)),
                ('father_name', models.CharField(max_length=255)),
                ('father_occupation', models.CharField(max_length=255)),
                ('mother_name', models.CharField(max_length=255)),
                ('place_of_birth', models.CharField(max_length=255)),
                ('mother_tongue', models.CharField(max_length=255)),
                ('professional_society_membership', models.CharField(blank=True, max_length=255)),
                ('nationality', models.CharField(max_length=255)),
                ('state_of_origin', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('marital_status', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('appeared_in_gate', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('physically_challenged', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='home',
        ),
    ]
