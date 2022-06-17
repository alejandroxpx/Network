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

def create_profile(request,username):
    if request.method == "POST":
        try:
            profile = Profile.objects.get(username)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Profile not created."
            })
        # login(request, user)
    #     return HttpResponseRedirect(reverse("index"))
    # else:
    #     return render(request, "network/register.html")


# Display user's profile 
def profile(request, username):
    user_id = User.objects.filter(username=username)[:1]
    # This uses the Profile model so look at that and dont think about the User model.
    follower = Profile.objects.get(user=1)
    return render(request, "network/profile.html",{
        "profile": Profile.objects.all(),
        "user": User.objects.get(id=user_id),
        "post" : Post.objects.all().filter(user=user_id).order_by('-date'),
        "followers": follower.followers.all().count(),
        "following": follower.following.all().count(),
    })

# Need to filter out the post from the people who they follow only
def following(request, username):
    user_id = User.objects.filter(username=username)[:1]
    return render(request, "network/following.html",{
    "post" : Profile.objects.all().filter(user=user_id).order_by('followers'),
    })

def follow(request,follower,followee):
    #TODO: Need to add the followee to the followers manytomany field 
    follower_id = User.objects.filter(username=follower)[:1] 
    follower_profile = Profile.objects.filter(user = follower_id)[:1]

    followee_id = User.objects.filter(username=followee)[:1] 
    followee_profile = Profile.objects.filter(user = followee_id)[:1]

    # PROBLEM

   
    return render(request, "network/profile.html")