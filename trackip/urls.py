from django.contrib import admin
from django.urls import path
from blogapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('signup/', views.signup_user, name="signup"),
    path('addpost/', views.add_post, name="addpost"),
    path('update/<int:id>/', views.update_post, name="updatepost"),
    path('delete/<int:id>/', views.delete_post, name="deletepost"),
]
