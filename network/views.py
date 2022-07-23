from enum import auto
from genericpath import exists
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from numpy import TooHardError
from django import forms
import json
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt

from .models import *

def index(request):
    objects = Post.objects.all().order_by("-date")
    page_number = request.GET.get('page',1)
    p = Paginator(objects,10)
    try: 
        page = p.page(page_number)
    except EmptyPage:
        page = p.page(1)
    page_obj = p.get_page(page_number)
    return render(request, "network/index.html",{
        "form" : NewPostForm(),
        # "post" : Post.objects.all().order_by('-date'),
        "post": page_obj,
        "page": page,
        "page_count":p.num_pages

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

# Display user's profile 
def profile(request, username):
    user_id = User.objects.filter(username=username)[:1]
    followee_info = User.objects.get(username=username)
    follower_info = User.objects.get(id=request.user.id)
    following = Connection.objects.filter(follower_id = user_id).count()
    follower = Connection.objects.filter(following_id = user_id).count()
    # Check if the current user already follows the clicked on profile
    check = Connection.objects.filter(follower_id = follower_info ,following_id = followee_info).count()
    if check == 1:
        #Found instance
        flag = 1
    elif check == 0: 
        #Did not find instance
        flag = 0
        
    return render(request, "network/profile.html",{
        "user": User.objects.get(id=user_id),
        "post" : Post.objects.all().filter(user=user_id).order_by('-date'),
        "followers": follower,
        "following": following,
        "flag":check,
        "message":check,
    })
    
# Follow user 
def follow(request, username):
    user_id = User.objects.filter(username=username)[:1]
    followee_info = User.objects.get(username=username)
    follower_info = User.objects.get(id=request.user.id)
    # follower_post = Post.objects.get(user = request.user)
    # followee_post = Post.objects.get(user = user_id)
    following = Connection.objects.filter(follower_id = user_id).count()
    follower = Connection.objects.filter(following_id = user_id).count()
    check = Connection.objects.filter(follower_id = follower_info ,following_id = followee_info).count()
    if check > 0:
        return render(request,"network/profile.html",{
            "flag":1,
            "message":"Already follow this user",
            "user": User.objects.get(id=user_id),
            "followers": follower,
            "following": following,
            "post" : Post.objects.all().filter(user=user_id).order_by('-date'),
            "flag":1
        })
    elif check == 0:
        # TODO Needs to figure out how to add post connection to connections to referrence in the following tab
        f = Connection(follower_id = follower_info ,following_id = followee_info)
        # f.following_id_post.set(followee_post)
        # f.follower_id_post.set(follower_post)
        f.save() 

        following = Connection.objects.filter(follower_id = user_id).count()
        follower = Connection.objects.filter(following_id = user_id).count()   
        return render(request,"network/profile.html",{
            "message":"Adding Follower",
            "user": User.objects.get(id=user_id),
            "post" : Post.objects.all().filter(user=user_id).order_by('-date'),
            "followers": follower,
            "following": following,
            "flag":1,
        })

# Unfollow user
def unfollow(request, username): 
    user_id = User.objects.filter(username=username)[:1]
    followee_info = User.objects.get(username=username)
    follower_info = User.objects.get(id=request.user.id)
    f = Connection.objects.filter(follower_id = follower_info ,following_id = followee_info)
    f.delete() 
    following = Connection.objects.filter(follower_id = user_id).count()
    follower = Connection.objects.filter(following_id = user_id).count()
    #TODO: Need to render the current page and simple change the button text to follow
    return render(request,"network/profile.html",{
       "user": User.objects.get(id=user_id),
        "flag":0,
        "followers": follower,
        "following": following,
        "post" : Post.objects.all().filter(user=user_id).order_by('-date'),
        "message":"In the unfollow views",
    })

# Display post from users being followed only
def following(request, username):
    # user_id = User.objects.get(username=username)
    # print("user_id: ",request.user.id)
    following = Connection.objects.raw('SELECT id, following_id_id FROM network_connection WHERE follower_id_id = %s'% (request.user.id))
    # print("following: ",following)

    list = []
    following_list = []
    counter=0
    for user in following:
        # print("user: ",user.id)
        user2 = Connection.objects.filter(id=user.id)
        list.append(user2)
        following_list.append(list[counter][0].following_id.id)
        # print("following list",following_list)
        counter +=1
    # print(len(following_list))
    if len(following_list)==1:
        following_list.append(0)
        # print(len(following_list))
    following_list = tuple(following_list)
    # print(following_list)
    return render(request, "network/following.html",{
        "user": User.objects.get(id=request.user.id),
        # "list":list,
        "post" : Post.objects.raw('SELECT * FROM network_post WHERE user_id IN %s' %(following_list,))
    })

#TODO: Need to get post id to filter which post I want to edit
@csrf_exempt
@login_required
def edit(request,id):

    print("id: ",id)
    # Get contents of email
    data = json.loads(request.body)
    body = data.get("body", "")

    # Get user
    user = User.objects.get(username=request.user.username)
    print(user.username)
    # GET post
    post = Post.objects.get(id=id)
    print(post.post)
    post.post = body
    post.save()
# #####
    objects = Post.objects.all().order_by("-date")
    page_number = request.GET.get('page',1)
    p = Paginator(objects,10)
    try: 
        page = p.page(page_number)
    except EmptyPage:
        page = p.page(1)
    page_obj = p.get_page(page_number)
    return render(request, "network/index.html",{
        "form" : NewPostForm(),
        "post": page_obj,
        "page": page,
        "page_count":p.num_pages
    })
@csrf_exempt
@login_required
def like(request,id):
    print("id: ",id)
    # Get contents of email
    data = json.loads(request.body)
    body = data.get("body", "")
    # Get user
    user = User.objects.get(username=request.user.username)
    print(user.username)
    # GET post
    post = Post.objects.get(id=id)
  
    post.likes += 1
    print(post.likes)
    post.save(update_fields=["likes"])
###
    objects = Post.objects.all().order_by("-date")
    page_number = request.GET.get('page',1)
    p = Paginator(objects,10)
    try: 
        page = p.page(page_number)
    except EmptyPage:
        page = p.page(1)
    page_obj = p.get_page(page_number)
    return render(request, "network/index.html",{
        "form" : NewPostForm(),
        "post": page_obj,
        "page": page,
        "page_count":p.num_pages
        })

