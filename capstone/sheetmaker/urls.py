from django.urls import path 
from . import views

# Creating urls

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),

    path('generateNewSet', views.generateNewSet, name='generateNewSet'),

    # Paths for everything regarding multiplication
    path('multiplication', views.multiplication, name='multiplication'),
    path('multiplication/<int:id>/<str:action>', views.multiplication_view, name='multiplication_view'),
    path('createMultiplication', views.createNewMultiplicationSet, name='createMultiplication'),
    path('deleteMultiplication', views.deleteMultiplicationSet, name='deleteMultiplication'),
    path('editMultiplication', views.editMultiplicationSet, name='editMultiplication'),

    # Paths for everything regarding division
    path('division', views.division, name='division'),
    path('division/<int:id>/<str:action>', views.division_view, name='division_view'),
    path('createDivision', views.createNewDivisionSet, name='createDivision'),
    path('deleteDivision', views.deleteDivisionSet, name='deleteDivision'),
    path('editDivision', views.editDivisionSet, name='editDivision'),

    # Paths for everything regarding arithmetic (addition and subtraction)
    path('arithmetic', views.arithmetic, name='arithmetic'),
    path('arithmetic/<int:id>/<str:action>', views.arithmetic_view, name='arithmetic_view'),
    path('createArithmetic', views.createNewArithmeticSet, name='createArithmetic'),
    path('deleteArithmetic', views.deleteArithmeticSet, name='deleteArithmetic'),
    path('editArithmetic', views.editArithmeticSet, name='editArithmetic')
]