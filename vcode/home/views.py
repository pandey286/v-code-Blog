from ast import Return
from turtle import title
from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post


# Create your views here.

# HTML Pages
def home(request):
    return render(request, 'home/home.html')
   
def about(request):
    return render(request, 'home/about.html')   

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact= Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message have been send successfully")
    return render(request, 'home/contact.html')
    
def search(request):
    # allPosts = Post.objects.all()
    query = request.GET['query']
    if len(query)>50:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent).union(allPostsAuthor)
    
    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)
    

# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        # Get the post paramters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous input

        # Username should be under 10 character
        if len(username) > 10:
            messages.error(request,"Username must be less then 10 character")
            return redirect('/')

        #  Username should contain alphabet and number
        if not username.isalnum():
            messages.error(request,"Username should contain letters and number")
            return redirect('/')

        # if password don't match
        if pass1 != pass2:
            messages.error(request,"Password do not match ")
            return redirect('/')
        

        # Create the User
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your v/Code account has been successfully created")
        return redirect('/')

    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        # Get the post paramters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username= loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('/')
        else:
            messages.warning(request, "Invalid Credintials (Username or Password); Please try to login again")
            return redirect('/')

    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('/')

