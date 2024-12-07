# Generated by Django 5.0.7 on 2024-10-18 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_remove_student_sections_student_sections'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='sections',
        ),
        migrations.AddField(
            model_name='section',
            name='students',
            field=models.ManyToManyField(related_name='students', to='home.student'),
        ),
    ]