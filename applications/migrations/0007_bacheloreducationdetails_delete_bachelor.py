# Generated by Django 4.2.5 on 2024-08-17 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0006_application_details_bachelor_dcmembers_details_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BachelorEducationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bachelor_degree', models.CharField(max_length=50)),
                ('bachelor_discipline', models.CharField(max_length=100)),
                ('bachelor_university', models.CharField(max_length=200)),
                ('bachelor_year', models.IntegerField()),
                ('bachelor_cgpa', models.DecimalField(decimal_places=2, max_digits=4)),
                ('bachelor_branch', models.CharField(max_length=100)),
                ('bachelor_class', models.CharField(max_length=50)),
                ('bachelor_semester_1', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bachelor_semester_2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bachelor_semester_3', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bachelor_semester_4', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bachelor_semester_5', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bachelor_semester_6', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bachelor_semester_7', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bachelor_semester_8', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bachelor_aggregate', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Bachelor',
        ),
    ]
