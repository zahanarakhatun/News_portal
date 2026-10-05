from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import News
from .forms import NewsForm, RegisterForm

# Create your views here.
def home(request):
    news_list = News.objects.all()
    return render(request, 'home.html', {'news_list': news_list})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news_detail.html', {'news': news})

@login_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'News created successfully!')
            return redirect('home')
    else:
        form = NewsForm()
    return render(request, 'news_form.html', {'form': form, 'title': 'Create News'})

@login_required
def news_update(request, pk):
    news = get_object_or_404(News, pk=pk)
    # Only author can edit
    if news.author != request.user:
        messages.error(request, "You are not allowed to edit this news!")
        return redirect('home')
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'News updated!')
            return redirect('news_detail', pk=pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news_form.html', {'form': form, 'title': 'Update News'})

@login_required
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if news.author != request.user:
        messages.error(request, "You are not allowed to delete this news!")
        return redirect('home')
    
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'News deleted!')
        return redirect('home')
    return render(request, 'news_confirm_delete.html', {'news': news})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})