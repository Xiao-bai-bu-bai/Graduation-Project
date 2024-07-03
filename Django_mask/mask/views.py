from django.shortcuts import render, redirect
from django import forms
from mask import models
from django.urls import reverse


class LoginForm(forms.Form):
    """登录表单"""
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': "form-control", "placeholder": '输入用户名'})
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '输入密码'}, render_value=True)
    )


# 注册表单
class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = "__all__"
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入用户名'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '输入密码'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '输入年龄'}),
        }


def login(request):
    """用户登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'form': form})

    form = LoginForm(data=request.POST)
    if request.method == "POST":
        if not form.is_valid():
            return render(request, "login.html", {'form': form})

    user = form.cleaned_data['username']
    pwd = form.cleaned_data['password']
    admin_object = models.Admin.objects.filter(username=user, password=pwd).first()

    user_info = {}  # 定义一个空字典，用于存储用户信息

    if admin_object:
        user_info = {'name': admin_object.username}

    if user_info:
        request.session['info'] = user_info
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/home/")
    else:
        return render(request, 'login.html', {"form": form, 'error': "用户名或密码错误"})


def logout(request):
    """退出登录"""
    if 'info' in request.session:
        del request.session['info']
    return redirect(reverse('login_name'))


def home(request):
    """首页"""
    return render(request, "口罩检测系统.html")


def register(request):
    """用户注册"""
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'mask_logon.html', {'form': form})
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('login_name'))
    return render(request, 'mask_logon.html', {'form': form})
