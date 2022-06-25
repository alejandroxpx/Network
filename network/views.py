from genericpath import exists
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from numpy import TooHardError
from django import forms
import datetime

from .models import *

def index(request):
    return render(request, "network/index.html",{
        "form" : NewPostForm(),
        "post" : Post.objects.all().order_by('-date'),

    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

class NewPostForm(forms.Form):
    post = forms.CharField(label="",max_length=128)

# Render all post created by this user and other users
def addPost(request):

    if request.method == "POST":
        form = NewPostForm(request.POST)

        if form.is_valid():
            new_post = form.cleaned_data["post"]
            posts = Post(user=request.user,post=new_post,date=datetime.datetime.now())
            posts.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"network/index.html",{
                "form":form
            })
    return render(request, "network/index.html",{
        "form": NewPostForm(),
        "post": Post.objects.all(),
    })

# def create_profile(request,username):
    profile = Profile.objects.get(username)
    profile.save()
    return render(request, "network/register.html")

# Display user's profile 
def profile(request, username):
    user_id = User.objects.filter(username=username)[:1]
    followee_info = User.objects.get(username=username)
    follower_info = User.objects.get(id=request.user.id)
    following = Connection.objects.filter(follower_id = user_id).count()
    follower = Connection.objects.filter(following_id = user_id).count()
    # Check if the current user already follows the clicked on profile
    check = Connection.objects.filter(follower_id = follower_info ,following_id = followee_info).count()
    if check > 0:
        flag = True
    else: 
        flag = None
        
    return render(request, "network/profile.html",{
        "user": User.objects.get(id=user_id),
        "post" : Post.objects.all().filter(user=user_id).order_by('-date'),
        "followers": follower,
        "following": following,
        "flag":flag,
    })

#TODO Show post from following group only
def following(request, username):
    # follower = User.objects.get(username = username)
    # following = Connection.objects.filter(follower_id=follower)

    return render(request, "network/following.html",{
    # "post" : Post.objects.filter(user=following)
    })
    
# Follow the user 
def follow(request, username):
    followee_info = User.objects.get(username=username)
    follower_info = User.objects.get(id=request.user.id)
    check = Connection.objects.filter(follower_id = follower_info ,following_id = followee_info).count()
    if check > 0:
        return render(request,"network/layout.html",{
            "flag":True,
        })
    elif check == 0:
        f = Connection(follower_id = follower_info ,following_id = followee_info)
        f.save()    
    return render(request,"network/layout.html")


def unfollow(request, username):
    followee_info = User.objects.get(username=username)
    follower_info = User.objects.get(id=request.user.id)
    f = Connection.objects.get(follower_id = follower_info ,following_id = followee_info)
    f.delete()   
    #TODO: Need to render the current page and simple change the button text to follow
    return render(request,"network/profile.html")