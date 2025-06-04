from django.shortcuts import render
from . models import Photo, User, UserProfile, Comment, Like
from . forms import PhotoForm
# Create your views here.

from django.shortcuts import render, redirect 
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages

from .forms import SignUpForm, ProfileEditForm

def register(request): 
    if request.method == 'POST': 
        form = SignUpForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('login') 
    else: 
 
        form = SignUpForm() 
    return render(request, 'registration/register.html', {'form': form})

 
def custom_logout(request): 
    logout(request) 
    return redirect('login') 

def home(request):
    # Get all photos ordered by upload date (newest first)
    photos = Photo.objects.all().order_by('-upload_date')
    return render(request, 'home.html', {
        'photos': photos,
        'user': request.user
    })

@login_required
def photo_list(request):
    # Filter photos to only show those belonging to the logged-in user
    photos = Photo.objects.filter(user=request.user).order_by('-upload_date')
    return render(request, 'photo_list.html', {
        'photos': photos,
        'user': request.user
    })

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    context = {
        'photo': photo,
        'user': request.user,  # Explicitly pass the user
    }
    print(f"Photo user: {photo.user}, Current user: {request.user}")  # Debug print
    return render(request, 'photo_detail.html', context)

@login_required
def photo_delete(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    
    # Check if the current user is the owner
    if request.user != photo.user:
        messages.error(request, "You don't have permission to delete this photo.")
        return redirect('photo_list')
    
    if request.method == 'POST':
        photo.delete()
        messages.success(request, "Photo deleted successfully.")
        return redirect('photo_list')
    
    return render(request, 'photo_delete.html', {'photo': photo})

@login_required
def photo_upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'photo_upload.html', {'form': form})

# def all_user_pictures(request):
#     users = UserProfile.objects.all()
#     return render(request, 'home.html', {'users': users})

def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile.html', {'user': user})

@login_required
def profile_edit(request, username):
    if request.user.username != username:
        return redirect('profile', username=request.user.username)
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'profile_edit.html', {'form': form})

@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    like, created = Like.objects.get_or_create(user=request.user, photo=photo)
    
    if not created:
        like.delete()
    return redirect('photo_detail', photo_id=photo_id)

@login_required
def comment_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment(user=request.user, photo=photo, content=content)
            comment.save()
    return redirect('photo_detail', photo_id=photo_id)

@login_required
def photo_edit(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    
    # Check if the current user is the owner
    if request.user != photo.user:
        messages.error(request, "You don't have permission to edit this photo.")
        return redirect('photo_detail', photo_id=photo_id)
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, "Photo updated successfully.")
            return redirect('photo_detail', photo_id=photo_id)
    else:
        form = PhotoForm(instance=photo)
    
    return render(request, 'photo_edit.html', {'form': form, 'photo': photo})