# Generated by Django 5.0.7 on 2024-10-16 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_classe_section_alter_classe_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='students',
            field=models.ManyToManyField(related_name='students', to='home.student'),
        ),
    ]
