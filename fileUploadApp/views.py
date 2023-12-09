from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import User, UploadedFile
from .forms import FileUploadForm, SignUpForm
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UploadedFile, FileShare
from django.contrib.auth.models import User

def developer(request):
    return render(request, 'developer.html')

def url_check(request):
    if request.user.is_anonymous:
        return redirect('user_login')
    else:
        return redirect('file_list')
@csrf_exempt
def share_files_api(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        selected_users = request.POST.getlist('selected_users[]')  # Get selected user IDs as a list
        shared_by = request.user

        file = UploadedFile.objects.get(id=file_id)
        users_to_share = User.objects.filter(id__in=selected_users)
        for user in users_to_share:
            existing_share = FileShare.objects.filter(file=file, shared_with=user).exists()
            if not existing_share:
                FileShare.objects.create(file=file, shared_by=shared_by, shared_with=user)
        return JsonResponse({'message': 'File shared successfully!'})
    return JsonResponse({'error': 'Invalid request'})

def share_files(request):
    files = UploadedFile.objects.filter(user=request.user)
    all_users = User.objects.filter(is_superuser = False).exclude(id=request.user.id)
    return render(request, 'share.html', {'files': files, 'all_users': all_users})

def search_users(request):
    return render(request, 'search_user.html')

def search_results(request):
    query = request.GET.get('query',None)
    if query:
        users = (
            User.objects
            .filter(username__icontains=query, is_superuser=False)
            .annotate(total_files=Count('uploadedfile'))
            .order_by('-total_files')
        )
    else:
        users = (
            User.objects
            .filter(is_superuser=False)
            .annotate(total_files=Count('uploadedfile'))
            .order_by('-total_files')
        )
        
    return render(request, 'search_results.html', {'users': users})

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! Please log in.")
            return redirect('user_login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('file_list')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url='user_login')
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadedFile(file=request.FILES['file'], user=request.user)
            new_file.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'fileUpload.html', {'form': form})

@login_required(login_url='user_login')
def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)
    sharedFiles = FileShare.objects.filter(shared_with=request.user)
    return render(request, 'fileList.html', {'files': files, 'sharedFiles':sharedFiles})
