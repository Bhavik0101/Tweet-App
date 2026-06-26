from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet
from .forms import TweetForm,UserRegistration
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.
def index(request):
    return render(request,'index.html')

def tweet_list(request):
    tweets=Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})

#Forms concept simplified:-
#1.)Sabse pehle agar forms handle kr rahe toh if else mai request method handle krenge 
#2.) same view se do cheese ho skti hai isliye request method handle krna zaruri hai 
#3.) Agar request GET hai iska mtlb user data fetch krna chahtta hai toh usse bas form return krdo
#4.) Agar POST hai iska mtlb user data bhejna chahta hai toh request.POST se sara data form ka ek variable mai lelo
#5.)aur phir agar form valid hai toh save kro aur return krdo agar krna h toh 
@login_required 
def tweet_create(request):
    if request.method=="POST":
        form =TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')


    else:
        form=TweetForm()
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form=TweetForm(instance=tweet)

    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_delete.html',{'tweet':tweet})

def register(request):
    if request.method=="POST":
        form=UserRegistration(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form=UserRegistration()
    return render(request,'registration/register.html',{'form':form})