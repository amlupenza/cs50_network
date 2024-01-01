from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
import json

from .models import User


def index(request):

    # get posts
    posts = Post.objects.all().order_by('-time')
    # paginator for all posts
    paginator = Paginator(posts,10)
    
    page_number = request.GET.get('page')
    #page object for all posts
    page_obj = paginator.get_page(page_number)
    
    
    return render(request, "network/index.html", {
        
        'page_obj' : page_obj,
        'all_posts' : True
    })

# Following view
@login_required
def following(request):
    # get user 
    user = request.user
    # check if user is following any user
    if Account.objects.filter(user=user).exists():
        followingAccounts = Account.objects.filter(user=user)
        followingUsers = [account.target for account in followingAccounts]
    else:
        messages.error(request, 'Sorry, no posts for accounts you are following')
        return HttpResponseRedirect(reverse('index'))
    posts = Post.objects.filter(author__in=followingUsers)
    # get paginator object
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    # page object for posts
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        'page_obj': page_obj,
        'all_posts': False
    })


# Tweet view
@login_required
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
@login_required
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
@login_required
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

# edit view
@csrf_exempt
@login_required
def edit_post(request,post_id):
        # try if post exists
        try:
            # get the post
            post = Post.objects.get(pk=post_id)

        except ObjectDoesNotExist:
            messages.error(request, 'Sorry, post you are accesing does not exist')
            return HttpResponseRedirect(reverse('index'))
        
        if request.method == 'POST':
            print('post went through')
            data = json.loads(request.body)
            newPost = data['newPost']
            # update tweet to newpost
            post.tweet = newPost
            print(post.tweet)
            # save new post
            post.save()
            return HttpResponseRedirect(reverse('index'))

    
        return JsonResponse({
            'tweet' : post.tweet,
            'author' : post.author.username.capitalize(),
        })

   
          
    
# like_post function
@ require_POST
@csrf_exempt
@login_required
def like_post(request,post_type,post_id):
    # get user
    user = request.user
    print('like view accessed')
    
    if post_type.lower() == 'comment': 
        # get the comment
        comment = Comment.objects.get(id=post_id)
        # check if this comment is in the user's liked comments (if user haven't liked the comment)
        if user not in comment.liked_by.all():
            # add user to the liked by list
            comment.liked_by(user).add()
            # increase comment likes by 1
            comment.likes += 1
            # save the comment
            comment.save()
            return JsonResponse({
                'liked' : True,
                'likes': comment.likes.count(),
                'post_type': 'comment'
            })
        # else if user liked the comment
        else:
            # remove user from the comment like_by list ( make user unlike the comment)
            comment.liked_by(user).remove()
            # decrease comment likes by 1
            comment.likes -= 1
            # save the comment
            comment.save()
            return JsonResponse({
                'liked' : False,
                'likes': comment.likes.count(),
                'post_type': 'comment'
            })

    elif post_type.lower() == 'post':
        # get the post
        post = Post.objects.get(pk=post_id)
        # check if this post is in the user's liked posts (if user haven't liked the post)
        if user not in post.liked_by.all():
            # add user to the post's liked by
            post.liked_by.add(user)
            # increase the post likes by 1
            post.likes += 1
            # save the post
            post.save()
            print(f'This post has {post.likes} likes')
            return JsonResponse({
                'liked' : True,
                'likes': post.likes,
                'post_type': 'post'
                
            })
        else:
            # remove user from the liked post
            post.liked_by.remove(user)
            # decrease the post like by 1
            post.likes -= 1
            # save the post
            post.save()
            print(f'This post has {post.likes} likes')
            return JsonResponse({
                'liked': False,
                'likes': post.likes,
                'post_type': 'post'
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
        #account = Account(user=request.user)
        # save the account
        #account.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
