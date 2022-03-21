from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('owner/<str:pk>', views.owner, name='owner'),
    path('update_owner', views.ownerUpdate, name='update_owner'),

    
    path('my_components', views.my_components, name='my_components'),
    path('create_component/<str:pk_test>', views.createComponent, name='create_component'),
    path('update_component/<str:pk>', views.updateComponent, name='update_component'),
    path('delete_component/<str:pk>', views.deleteComponent, name='delete_component'),

]