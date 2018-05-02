from django.urls import path, include

from . import views

urlpatterns = [
    path('ping/', views.ping),

    path('users/', views.users),
    path('user/<int:userId>/', views.user),

    path('materials/<int:is_real_material>/', views.materials),
    path('material/1/<int:real_material_id>', views.real_material),
]
