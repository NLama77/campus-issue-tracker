from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('report/',views.report_issue, name="report_issue"),
    path('issue/<int:issue_id>/', views.issue_detail, name='issue_detail'),
    path('vote/<int:issue_id>/', views.vote_issue, name='vote_issue'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'), 
    path('register/', views.register, name='register'),
]