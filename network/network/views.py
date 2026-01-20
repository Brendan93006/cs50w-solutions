from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.select_related("creator").order_by("-timestamp")

    try:
        liked = []
        for post in posts:
            if Like.objects.filter(liker=request.user, post=post).exists():
                liked.append(post)
    except TypeError:
        liked = None
        
    page_number = request.GET.get('page')

    page = pagination(posts, page_number)

    return render(request, "network/index.html", { "page": page, "liked": liked })


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
    
@login_required
def create_post(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")
        
    content = request.POST.get("post_content")
    
    if not content:
        return HttpResponseBadRequest("Must Provide Content")
    
    Post.objects.create(creator=request.user, content=content)

    return redirect("index")


@login_required
def profile_view(request, username):
    if request.method == 'GET':

        user = User.objects.get(username=username)

        follows = Follow.objects.filter(followed=user, follower=request.user).exists()

        posts = Post.objects.filter(creator=user).order_by("-timestamp")

        liked = []
        for post in posts:
            if Like.objects.filter(liker=request.user, post=post).exists():
                liked.append(post)

        user_followers = user.followers.count()

        user_following = user.following.count()

        page_number = request.GET.get('page')

        page = pagination(posts, page_number)

        return render(request, "network/profile.html", { "username": user, "page": page, "followers": user_followers, "following": user_following, "follows": follows, "liked": liked })
    

@login_required
def toggle_follow(request, username):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    else:
        target = get_object_or_404(User, username=username)

        if target == request.user:
            return JsonResponse({"error": "cannot follow yourself"}, status=400)
        
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=target)

        if not created:
            follow.delete()
            following = False
        else:
            following = True

        return JsonResponse({
            "following": following,
            "followers_count": target.followers.count()
        })
    

@login_required
def following_view(request):
    if request.method == "GET":

        followed_users = User.objects.filter(followers__follower=request.user)

        posts = Post.objects.filter(creator__in=followed_users).order_by("-timestamp")

        page_number = request.GET.get('page')

        page = pagination(posts, page_number)

        liked = []
        for post in posts:
            if Like.objects.filter(liker=request.user, post=post).exists():
                liked.append(post)

        return render(request, "network/following.html", { "page": page, "liked": liked })


def pagination(posts, page_number):
    paginator = Paginator(posts, 10)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


@login_required
def edit_post(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT required"}, status=400)
    
    data = json.loads(request.body)

    content = data.get("content")

    post = Post.objects.get(id=post_id)

    if request.user != post.creator:
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    post.content = content

    post.save()

    return JsonResponse({"message": "Post updated"})


@login_required
def toggle_like(request, post_id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    
    post = Post.objects.get(id=post_id)
    
    like, created = Like.objects.get_or_create(liker=request.user, post=post)

    if created:
        like = True
    else:
        like.delete()
        like = False

    return JsonResponse({
        "like": like,
        "like_count": post.likes.count()
    })