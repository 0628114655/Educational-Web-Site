from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.utils import timezone

# Create your views here.

# الصفحة الرئيسية
def home (request): 
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info =  None
    context = {
        'user_info': user_info,
        'paragraphs' : Home.objects.all()
    }
    return render (request,'pages/home.html', context)

def announce (request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
        'announces': Announce.objects.all()
        }
    return render (request,'pages/announce.html', context)

# الدالة الخاصة بالبحث عن الدرس
def course_res (request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
    }
    return render (request,'pages/course_res.html', context)

# الدالة التي تظهر النتائج التي توافق البحث
def search(request):
    message = None
    result = None
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            result = Course.objects.filter(subject__icontains = query)
            if not result.exists():
                message = 'لا توجد نتيجة تطابق نص البحث.'
    else:
        message = 'النص الذي تم إدخاله غير صالح, المرجو إدخال نص آخر.'
    
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
        'message' : message,
        'result' : result
    }
    return render(request, 'pages/search.html', context)

# الدالة التي تظهر النتيجة التي تم اختيارها 
def course(request, id):
    course = Course.objects.get(id = id)
    images = Image.objects.filter(course = id)
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
        'images' : images,
        'course' : course
    }
    return render(request, 'pages/course.html', context)

# الدالة التي تعرض الواجبات الدراسية
def homeWork(request):
    try:
        now = time_zone.now().date()
        user = request.user
        user_info = UserProfile.objects.get(user = user)
        home_work = HomeWork.objects.filter(section__name = user_info.section, lastDate__gte = now)
        if not home_work.exists():
            message = 'لا توجد أي واجبات دراسية.'
        else:
            message = None
    except UserProfile.DoesNotExist:
        user_info = None
        home_work = None
        message = 'المرجو تسجيل الدخول للاطلاع على الواجبات الدراسية.'
    except Exception as e:
        print(f"Unexpected error: {e}")
        user = request.user
        user_info = UserProfile.objects.get(user = user)
        home_work = None
        message = 'حدث خطأ غير متوقع.'
    context = {
            'message' : message,
            'user_info': user_info,
            'home_work': home_work,
        }
    return render (request, 'pages/homeWork.html', context)

def signup(request):
    next = request.GET.get('next')
    form = UserRegistrationForm(request.POST, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        user.password = make_password(password)
        user.save()
        UserProfile.objects.create(
            user = user,
            firstname = form.cleaned_data.get('firstname'),
            lastname = form.cleaned_data.get('lastname'),
            section = form.cleaned_data.get('section'),
            image = form.cleaned_data.get('image'),
        )
        new_user = authenticate(username = username, password = password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/') 
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
        'form': form
    }   
    return render(request, 'pages/signup.html', context)

def signin(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username') 
        password = form.cleaned_data.get('password') 
        user = authenticate(username = username, password = password)
        login(request, user)
        if next:
            return redirect(next)
        else:
            return redirect('/')
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
        'form': form
    }   
    return render(request, 'pages/signin.html', context)

def signout(request):
    logout (request)
    return redirect('/signin/')

def UserInfo(request):
    user = request.user
    userData = UserProfile.objects.get(user = user)
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
        'user' : userData
    }
    return render (request, 'pages/userInfo.html', context)

# صفحة خاصة بعرض نماذج الامتحانات/تصحيح الامتحان/نقط الامتحان
def exams(request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
    }
    
    return render(request, 'pages/exams.html', context)
# الدالة الخاصة بالبحث عن تصحيح الامتحان
def exam_research(request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
    }
    return render(request, 'pages/exam/exam_research.html', context)

# الدالة التي تظهر النتائج التي توافق البحث
def exam_search_result(request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    result = None
    message = None
    exam_form = SearchForm(request.GET)
    if exam_form.is_valid():
        query = exam_form.cleaned_data.get('query')
        if query:
            result = ExamCorrection.objects.filter(content__contains = query)
            if not result.exists():
                    message = 'لا توجد نتيجة تطابق نص البحث.'
    else:
        message = 'النص الذي تم إدخاله غير صالح, المرجو إدخال نص آخر.'
    context = {
        'result' : result,
        'message' : message,
        'user_info': user_info,
    }
    return render(request, 'pages/exam/exam_research_result.html', context)

# الدالة التي تظهر النتيجة التي تم اختيارها 
def exam_correction(request, id):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    result = ExamCorrection.objects.get(id = id )
    context = {
        'user_info': user_info,
        'result' : result
    }
    return render(request, 'pages/exam/exam_correction.html', context)

# صفحة مخصصة لعرض نقط الامتحان
def exam_marks(request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user=user)
        mark = ExamMark.objects.filter(student__massar_num = user.username)
        if not mark.exists():
            mark = None
            message = 'لا توجد أية نقط امتحانات.'
        else:
            message = None
            print('mark is ', mark)
    except UserProfile.DoesNotExist:
            user_info = None
            mark = None
            message = 'المرجو تسجيل الدخول للاطلاع على نقط الامتحان.'
    except Exception as e:
            print(f"Unexpected error: {e}")
            user = request.user
            user_info = UserProfile.objects.get(user=user)
            mark = None
            message = 'حدث خطأ غير متوقع.'
    context = {
        'user_info' : user_info,
        'mark' :  mark,
        'message': message,
    }
    return render (request, 'pages/exam_marks.html', context)