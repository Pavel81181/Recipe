from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>/', views.recipe_desc, name='recipe_desc'),
    path('recipe/add/', views.recipe_add, name='recipe_add'),
    path('recipe/edit/<int:recipe_id>/', views.recipe_edit, name='recipe_edit'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)