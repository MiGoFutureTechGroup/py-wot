from django.urls import path, include

from . import views

urlpatterns = [
    path('ping/', views.ping),

    path('users/', views.users),
    path('users/new/user', views.new_user),
    path('users/new/role', views.new_role),
    path('users/<int:userId>/', views.user),

    path('join/', views.join),
    path('login/', views.login),
    path('logout/', views.logout),
    path('change_password/', views.change_password),

    path('materials/1/', views.materials_real),
    path('materials/0/', views.materials_abstract),
    path('material/1/<int:real_material_id>', views.real_material),

    path('quotations/as/<str:role>/', views.quotations),
    path('quotation/as/<str:role>/<int:quotation_id>/', views.quotation),
]
