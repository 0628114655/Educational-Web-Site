from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone as time_zone
from datetime import *


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length = 100)
    lastname = models.CharField(max_length = 100)
    section = models.CharField(max_length = 100, null = True, blank = True)
    image = models.ImageField(null = True, blank = True)
    def __str__(self):
        return self.firstname
    
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

class Announce(models.Model):
    title = models.CharField(max_length = 50)
    content = models.TextField(max_length = 500)
    def __str__(self):
        return self.title

class Home(models.Model):
    title = models.CharField(max_length = 50)
    text = models.TextField()
    def __str__(self):
        return self.title
    
class Course(models.Model):
    title = models.CharField(max_length = 100, null = True, blank = True)
    introduction = models.TextField(null = True, blank = True)
    subject = models.TextField( null = True, blank = True)
    conclusion = models.TextField(null = True, blank = True)
    def __str__(self):
        return self.title

class Subject(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length = 50)
    subjects = models.ManyToManyField(Subject, related_name= 'sections' )
    def __str__(self):
        return self.name  

class Student(models.Model):
    massar_num = models.CharField(max_length = 50, null = True, blank = True)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    student_id = models.CharField(max_length = 50)
    sections = models.ForeignKey(Section, related_name="students", blank = True, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Image(models.Model):
    title = models.CharField(max_length = 100, null = True , blank = True)
    course = models.ForeignKey(Course , on_delete = models.CASCADE)
    image = models.ImageField(null= True, blank=True)
    def __str__(self):
        return self.title
    @property
    def imgURL(self):
        if self.image.url:
            return self.image.url
        else:
            return ''
     
class HomeWork(models.Model):
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True, blank = True)
    title = models.CharField(max_length = 50, null = True)
    material =  models.ForeignKey(Subject, on_delete = models.CASCADE, null = True)
    content = models.TextField()
    section =  models.ManyToManyField(Section)
    lastDate = models.DateField(null = True)
    def __str__(self):
            return self.title
    
    @property
    def remain(self):
        delta = self.lastDate - time_zone.now().date()
        return delta.days
    
    @property
    def is_two_days(self):
       return self.lastDate - time_zone.now().date() <= timedelta(days = 3)

class ExamCorrection(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    material = models.ForeignKey(Subject, on_delete = models.SET_NULL, null = True)
    section = models.ManyToManyField(Section)
    date = models.DateField(null = True)
    margin1 = models.TextField(null = True, blank = True)
    margin2 = models.TextField(null = True, blank = True)
    margin3 = models.TextField(null = True, blank = True)
    margin4 = models.TextField(null = True, blank = True)
    margin5 = models.TextField(null = True, blank = True)
    def __str__(self):
        return self.title

class ExamMark(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    first_mark = models.FloatField(null=True, blank=True)
    second_mark = models.FloatField(null=True, blank=True)
    third_mark = models.FloatField(null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)  # إضافة حقل القسم
    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'
    

class Classe(models.Model):
    name = models.CharField(max_length=100, null = True)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL, related_name='classes')
    students = models.ManyToManyField(Student, related_name='classes')

    def __str__(self):
        if self.section:
            return f'Class: {self.name} in Section: {self.section.name}'
        else:
            return f'Class: {self.name} (No Section)'



