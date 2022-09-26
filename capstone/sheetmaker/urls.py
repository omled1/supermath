from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('multiplication', views.multiplication, name='multiplication'),
    path('division', views.division, name='division'),
    path('arithmetic', views.arithmetic, name='arithmetic'),
    path('history', views.history, name='history')
]