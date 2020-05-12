from django.shortcuts import render,redirect
from blogApp2.models import blogpost,profile
from blogApp2.forms import saveblog,updateblog,profileUpdate
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponseRedirect,HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
import os
import json
import datetime



# Create your views here.

def index(req):
   
    
    #print(post)
    return render(req,'index.html')
def login_view(req):
    if req.method =='POST':
        username = req.POST['username']
        #print(username)
        #print(User.objects.filter().exists())
        name = str(username)
        password = req.POST['password']
        #auth = False
        #print('password:',password)
        user = authenticate(username=username,password=password)
        #pwd = authenticate()
        #print(user)

        if user is not None :
            print(user.is_authenticated)
            login(req,user)
            
            return redirect(reverse('home',kwargs={'u':user}))
        else:
            return render(req,'login.html',{'error':'user and password does not match'})
       


    return render(req,'login.html')


def signup(req):
    if req.method =='POST':
        first_name = req.POST['first name']
        last_name = req.POST['last name']
        username = req.POST['username']
        password = req.POST['password']
        if first_name !=" " and last_name !=" " and username !=" " and password!=" ":
            if User.objects.filter(username=username).exists():
                 return render(req,'signup.html',{'error':"user already exists"})
            else:
                user = User.objects.create_user(username = username ,password=password,first_name=first_name,last_name=last_name)
                #pro_pic = profile.objects.create(username=user.username)
                user.save()
                pr = profile(username=username)
                pr.save()
                return redirect(reverse(login_view))
        else:
            #print(form1)
            print("enter valid details")
            #print(user.errors)
            return render(req,'signup.html',{'error':"pls feel all details"}) 

   
            
    

    return render(req,'signup.html')

@login_required
def logout_view(req):
    logout(req)
    return redirect(reverse('index'))
@login_required

def home(req,u):
    if User.objects.filter(username=u).exists():
        print(User.is_authenticated)
        if User.is_authenticated:
            pr = profile.objects.filter(username=u)    

            print(u)
            posts = blogpost.objects.all().order_by("time").reverse()
            
            return render(req,'home.html',{'u':u,'blogs':posts,'pr':pr})
        else:
           return HttpResponse("<h1>User Not Found</h1>")
    else:
        return HttpResponse("<h1>User Not Found</h1>")
  
  

   
            
    
    
   
@login_required
def post_blog(req,u):
    if User.objects.filter(username=u).exists():
        if req.method == 'POST':
            #print(req.POST['title'])
            #print(req.POST['content'])
            #print(req.FILES['pic'])
            
            form2 = saveblog(req.POST,req.FILES)
            
            #print("files: ",req.FILES)
            if form2.is_valid():
                inst = form2.save(commit=False)
                inst.author = req.user
                inst.save()
                return redirect(reverse('home',kwargs={'u':u}))
            else:
                return render(req,'post-blog.html',{'error':form2.errors,'u':u})
    else:
        return HttpResponse("<h1>User Not Found</h1>")
  
  
        
    
    
    return render(req,'post-blog.html',{'u':u})
@login_required 
def view_blog(req,a,u):
    if User.objects.filter(username=u).exists():
        
        post=blogpost.objects.filter(title=a)
        #print(post)
        #print("post: ",post)

        return render(req,'view_blog.html',{'b':post,'u':u})
    else:
        return HttpResponse("<h1>User Not Found</h1>")
  
  
@login_required 
def profile_view(req,u,msg=None):
    if User.objects.filter(username=u).exists():
        user = User.objects.filter(username=u)
        user = user.values('first_name','last_name')
        
        for i in user:
            first_name =i['first_name']
            last_name = i['last_name']
        
        post=blogpost.objects.filter(author=u).order_by("time").reverse()
        pro_pic = profile.objects.filter(username=u)

        

        return render(req,'profile.html',{'b':post,'u':u,'fn':first_name,'ln':last_name,'p':pro_pic})
    else:
        return HttpResponse("<h1>User Not Found</h1>")
  
  
       
@login_required
def delete_blog(req,t,u):
    if User.objects.filter(username=u).exists():
        post=blogpost.objects.filter(title=t)
        post=blogpost.objects.filter(author=u)
        for i in post.values('pic'):
            i['pic']
            os.remove('media/'+i['pic'])
        
        
    
        #print("post1:",post)
        blogpost.objects.filter(title=t).delete()
        return redirect(reverse('profile',kwargs={'u':u}))
    else:
        return HttpResponse("<h1>User Not Found</h1>")
  
  

@login_required
def edit_blog(req,t,u):
    if User.objects.filter(username=u).exists():
        post=blogpost.objects.filter(title=t)
        #print(post)
        #print(post.values('pic'))
        p = post.values('pic')
        for i in p:
            image=i['pic']
        #print(image)

        if req.method=='POST':
            form2 = updateblog(req.POST,req.FILES)
           
            
            
            print(form2)
            print(form2.is_valid())
            print(form2.errors)
            if form2.is_valid():
                path = req.FILES.get('pic', False)
                print("path:",path)
             
                
                if path ==False:
                    print("yess")
                    blogpost.objects.filter(title=t).update(title=req.POST['title'],content=req.POST['content'],pic=image)
                else:
                    print("here..")
                    #blogpost.objects.filter(title=t,author=req.user).update(title=req.POST['title'],content=req.POST['content'],pic=image)
                    post.delete()
                    post_blog(req,u)                  
                        
                    
                return render(req,'edit.html',{'u':u,'b':post,'msg':"post has been updated"})
            else:
                return render(req,'edit.html',{'u':u,'b':post})
              
            """p=blogpost.objects.all().filter(title=t,author=u)
                
                p1=blogpost.objects.only('pic').filter(title=t,author=u)
                for i in p1:

                    print('p',i.pic)
                obj=blogpost.objects.filter(title=t,author=u)
                p.delete()
                obj.update(title=req.POST['title'],content=req.POST['content'],pic=req.FILES)
                form2.save(commit=True)"""
                
                    
                
                
            

            
            

        return render(req,'edit.html',{'u':u,'b':post})
    else:
        return HttpResponse("<h1>User Not Found</h1>")
  
  



@login_required
def edit_accounts(req,u):
    if User.objects.filter(username=u).exists() :
        
        #print("here..")
        uname = u
        #print(uname)
        u=User.objects.all().filter(username=u)
       
        
        
        if req.method=="POST":
            form = profileUpdate(req.POST,req.FILES ,instance=req.user)
            p = profile.objects.all()
            
            #print(req.FILES)
            #print(form)
            if form.is_valid():
                
                path = req.FILES.get('pic', False)
                print("path:",path)
             
                
                if path ==False:
                    
                    #print("yess")
                    u.update(first_name=req.POST['first_name'],last_name=req.POST['last_name'],username=req.POST['username'])
                    #print("done")
                    return render(req,'edit_profile.html',{'uname':uname,'u':u,'msg':"profile has been update"})
                else:
                    u.update(first_name=req.POST['first_name'],last_name=req.POST['last_name'],username=req.POST['username'])
                    print(" here...")
                    print(req.FILES['pic'])
                    profile.objects.filter(username=req.user).update(pic=req.FILES['pic'])
                    print("done")
                    
                   
                    return render(req,'edit_profile.html',{'uname':uname,'u':u,'msg':"profile has been update"})
                    
                    
    
        return render(req,'edit_profile.html',{'uname':uname,'u':u})
           
    return HttpResponse("<h1>User Not Found</h1>")


@login_required
def accounts(req,a,u):
    if User.objects.filter(username=a).exists():
       
        user = User.objects.filter(username=a)
       
        user = user.values('first_name','last_name')
        for i in user:
            first_name =i['first_name']
            last_name = i['last_name']
        
        
            
       
            
        
    
        post=blogpost.objects.filter(author=a).order_by("time").reverse()
        pro_pic = profile.objects.filter(username=a)
        if a==u:
              #return render(req,'profile.html',{'b':post,'u':u})
            return redirect(reverse('profile',kwargs={'u':u}))
        else:

        

            return render(req,'user_profile.html',{'b':post,'a':a,'u':u,'fn':first_name,'ln':last_name,'p':pro_pic})
    else:
        return HttpResponse("<h1>User Not Found</h1>")





        