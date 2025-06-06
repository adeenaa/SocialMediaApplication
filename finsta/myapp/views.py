from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView,FormView,UpdateView,ListView,DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q

from myapp.forms import SignUpForm,SignInForm,ProfileEditForm,PostForm,CoverPicForm
from myapp.models import UserProfile,Posts,Comments




class SignUpView(CreateView):
    model=User
    form_class=SignUpForm
    template_name="register.html"
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"account has been created")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"failed to create account")
        return super().form_invalid(form)
    
class SignInView(FormView):
    
    template_name="login.html"
    form_class=SignInForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("index")
            messages.error(request,"invalid credential")
            return render(request,self.template_name,{"form":form})
        
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    context_object_name="posts"
    success_url=reverse_lazy("index")
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class ProfileEditView(UpdateView):
    form_class=ProfileEditForm
    template_name="profile-edit.html"
    model=UserProfile
    success_url=reverse_lazy("index")

def add_like_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    post_obj=Posts.objects.get(id=id)
    post_obj.liked_by.add(request.user)
    return redirect("index")

def add_comment_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    post_obj=Posts.objects.get(id=id)
    comment=request.POST.get("comment")
    Comments.objects.create(user=request.user,post=post_obj,comment_text=comment)
    return redirect("index")

def remove_comment_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    comment_obj=Comments.objects.get(id=id)
    if request.user == comment_obj.user:
        comment_obj.delete()
        return redirect("index")
    else:
        messages.error(request,"please contact admin")
        return redirect("signin")

class ProfileDetailView(DetailView):
    model=UserProfile
    template_name="profile.html"
    context_object_name="profile"

#profile/{id}/coverpic/change
def cover_pic_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    prof_obj=UserProfile.objects.get(id=id)
    form=CoverPicForm(instance=prof_obj,data=request.POST,files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("profile-detail",pk=id)
    return redirect("profile-detail",pk=id)

class  ProfileListView(ListView):
    model=UserProfile
    template_name="profile-list.html"
    context_object_name="profiles"

    def get_queryset(self):
        return UserProfile.objects.exclude(user=self.request.user)
    
    def post(self,request,*args,**kwargs):
        pname=request.POST.get("username")
        qs=UserProfile.objects.filter(Q(user__username__icontains=pname))|Q(user__firstname__icontains=pname)
        return render(request,self.template_name,{"profiles":qs})
    
    

def follow_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    profile_obj=UserProfile.objects.get(id=id)
    user_prof=request.user.profile
    user_prof.following.add(profile_obj)
    user_prof.save()
    return redirect("index")

def unfollow_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    profile_obj=UserProfile.objects.get(id=id)
    user_prof=request.user.profile
    user_prof.following.remove(profile_obj)
    user_prof.save()
    return redirect("index")

def post_delete_view(request,*args,**kwargs):
    post_id=kwargs.get("pk")
    post_obj=Posts.objects.get(id=post_id)
    post_obj.delete()
    return redirect("index")