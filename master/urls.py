from django.urls import path, include

from . import views

urlpatterns = [
    path('ping/', views.ping),

    path('users/', views.users),
    path('user/<int:userId>/', views.user),

    path('materials/<int:is_real_material>/', views.materials),
    path('material/1/<int:real_material_id>', views.real_material),

    path('quotations/as/<str:role>/', views.quotations),
    path('quotation/as/<str:role>/<int:quotation_id>/', views.quotation),
]
