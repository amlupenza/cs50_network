from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from datetime import datetime
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import User


def index(request):
    # get user
    user = request.user
    # get user's followings
    followingAccounts = Account.objects.filter(user=user)
    # get all users that user is following
    followingUsers = [account.target for account in followingAccounts]
     #list of followings posts
    followingPosts = Post.objects.filter(author__in=followingUsers).order_by('-time')
    return render(request, "network/index.html", {
        'posts': Post.objects.all().order_by('-time'),
        'followingPosts': followingPosts
    })

# Tweet view
def tweet(request):
    if request.method == 'POST':
        tweet = request.POST['tweet']
        if tweet:
            author = request.user
            now = datetime.now()
            post = Post(author=author, tweet=tweet, time=now)
            post.save()
            return HttpResponseRedirect(reverse('index'))
        messages.error(request,"You can't post an empty tweet")
        return HttpResponseRedirect(reverse('index'))
    messages.error(request, "Invalid request method")
    return HttpResponseRedirect(reverse('index'))

# profile view
def profile(request, profile_id):
        # get user
        profile = User.objects.get(pk=profile_id)
        # check profile is not none
        if profile:
            # check if user is following any account
            if Account.objects.filter(user=profile).exists():
                followings = Account.objects.filter(user=profile).count()
            else:
                followings = 0
            # check if account is being followed
            if profile.followers:
                followers = profile.followers.all().count()
            else:
                followers = 0
        
            # get all posts of the user
            posts = Post.objects.filter(author=profile).order_by('-time')
            if Account.objects.filter(user=request.user, target=profile).exists():
            # get an account that represents a follow relationship btn user and profile account
                account = Account.objects.get(user=request.user, target=profile)
                followed = account.is_following
            else:
                followed = False
            # render a profile page
            return render(request, 'network/profile.html', {
            'profile' : profile,
            "followings" : followings,
            'followers' : followers,
            'followed' : followed,
            'posts' : posts
            })
        else:
            messages.error(request, 'Profile does not exist')
            return HttpResponseRedirect(reverse('index'))
   

# follow function
@require_POST
@csrf_exempt
def follow_user(request, account_id):
    #get user who made the request to follow the target
    user = request.user
    # user to follow or unfollow
    target = User.objects.get(pk=account_id)
    print(target)
    #check if user is already following the target
    try:
        # get an account
        account = Account.objects.get(user=user, target=target)
        # delete the account that represents following relationship
        account.delete()
        return JsonResponse({
            'followed': False,
            'followers': target.followers.count(),
            'followings': Account.objects.filter(user=target).count()
            })
    # if account doesn't exist
    except ObjectDoesNotExist:
        # create a new account object that represent the following relationship
        Account.objects.create(user=user, target=target, is_following=True)
        # return a JSON response with the follow status
        return JsonResponse({
            'followed': True,
            'followers': target.followers.count(),
            'followings': Account.objects.filter(user=target).count()
            })


   
        

    
    
# like_post function
def like_post(request,post_type,post_id):
    ...
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
    return HttpResponseRedirect(reverse("login"))


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
        # create an account
        account = Account(user=request.user)
        # save the account
        account.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
