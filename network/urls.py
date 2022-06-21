from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/",views.addPost, name="addPost"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>",views.profile, name = "profile"),
    path("following/<str:username>",views.following, name="following"),
    # path("register", views.create_profile, name = "create_profile"),
    # Will need to change the link to stay on the followee profile and change the button from follow to following
    path("follow/<str:username>",views.follow, name="follow"),
]
