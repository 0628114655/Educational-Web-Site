from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns=[
    path('', views.home, name = 'home'),
    path('announce/', views.announce, name = 'announce'),
    path('course_res/', views.course_res, name = 'course_res'),
    path('search/', views.search, name = 'search'),
    path('course/<int:id>', views.course, name = 'course'),
    path('signup/', views.signup, name = 'signup'),
    path('signin/', views.signin, name = 'signin'),
    path('signout/', views.signout, name = 'signout'),
    path('homeWork/', views.homeWork, name = 'homeWork'),
    path('UserInfo/', views.UserInfo, name = 'UserInfo'),
    path('exams/', views.exams, name = 'exams'),
    path('exam_marks/', views.exam_marks, name = 'exam_marks'),
    path('exam_research/', views.exam_research, name = 'exam_research'),
    path('exam_search_result/', views.exam_search_result, name = 'exam_search_result'),
    path('exam_correction/<int:id>', views.exam_correction, name = 'exam_correction'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='pages/change_password.html',
        success_url='/change-password/done/' 
    ), name='password_change'),
    path('change-password/done/', PasswordChangeDoneView.as_view(
        template_name='pages/password_change_done.html'
    ), name='password_change_done'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)