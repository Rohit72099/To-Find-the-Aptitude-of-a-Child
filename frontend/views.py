from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')
    
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def children_list(request):
    return render(request, 'children_list.html')


@login_required(login_url='login')
def children_add(request):
    return render(request, 'children_add.html')


@login_required(login_url='login')
def children_edit(request, child_id):
    return render(request, 'children_edit.html', {'child_id': child_id})


@login_required(login_url='login')
def children_assessments(request, child_id):
    return render(request, 'assessments_list.html', {'child_id': child_id})


@login_required(login_url='login')
def assessments_list(request):
    return render(request, 'assessments_list.html')


@login_required(login_url='login')
def test_start(request, assessment_id):
    return render(request, 'test_taking.html', {'assessment_id': assessment_id})


@login_required(login_url='login')
def test_taking(request):
    return render(request, 'test_taking.html')


@login_required(login_url='login')
def results_list(request):
    return render(request, 'results_list.html')


@login_required(login_url='login')
def results(request, session_id):
    return render(request, 'results.html', {'session_id': session_id})

