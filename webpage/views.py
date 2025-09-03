def logout_view(request):
    auth_logout(request)
    messages.success(request, 'ออกจากระบบเรียบร้อยแล้ว')
    return redirect('home')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def home(request):
    tab = request.GET.get('tab', 'login')
    context = {'tab': tab}
    if request.user.is_authenticated:
        context['current_user'] = request.user.username
    return render(request, 'home.html', context)

def base(request):
    return render(request, 'base.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'เข้าสู่ระบบสำเร็จ ยินดีต้อนรับ {username}')
            return redirect('home')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
            return redirect('/?tab=login')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('reg_username')
        password = request.POST.get('reg_password')
        password2 = request.POST.get('reg_password2')
        if password != password2:
            messages.error(request, 'รหัสผ่านไม่ตรงกัน')
            return redirect('/?tab=register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'ชื่อผู้ใช้นี้ถูกใช้แล้ว')
            return redirect('/?tab=register')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        # login อัตโนมัติหลังสมัครสมาชิก
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'สมัครสมาชิกสำเร็จ! ยินดีต้อนรับ {username}')
            return redirect('home')
        else:
            messages.success(request, 'สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
            return redirect('/?tab=login')
    else:
        return redirect('home')
