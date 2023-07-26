from django.shortcuts import render,redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, RegistrationForm, PostSearchForm
from django.urls import reverse,reverse_lazy
from django.db.models import Q
from  django.contrib import messages
from datetime import datetime

from django.contrib.auth.decorators import login_required


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,DetailView,
                               CreateView,DeleteView,UpdateView,)


# Create your views here.

class RegistraionView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'baseapp/register.html'


def AboutView(request):

    return render(request, 'baseapp/about.html')

def PostListView(request):
    posts =  Post.objects.filter(published = True).order_by('-created_date')
    
    context ={
        'posts' : posts,
    }
    return render(request, 'baseapp/post_list.html', context)
        

def PostDetailView(request, pk):
    post = Post.objects.get(pk = pk)
    comments = Comment.objects.filter(post=post)
    context = {
        'post' : post,
        'comments' : comments,
    }
    return render(request, 'baseapp/post_detail.html', context)


def PostCreateView(request):
    form = PostForm()

    if request.method == 'POST':
        print('posting')
        form = PostForm(request.POST, request.FILES)
        print('oj')
        
        if form.is_valid():
            if 'save_button' in request.POST:
            # Save the post without publishing
                blog = form.save(commit=False)
                blog.published = False
                blog.save()
                blog.user = request.user
                
                # Now, save the tags for the blog post
                category = form.cleaned_data['category']

                blog.category.set(category)
                blog.save()
                  # Save the tags for the blog post
                print('ok')
                messages.success(request, "Submitted.")
                return redirect('post_detail', blog.id)
        
            elif 'publish_button' in request.POST:
                # Save and publish the post
                blog = form.save(commit=False)
                blog.published = True
                blog.save()
                blog.user = request.user
                blog.published_date = timezone.now()
                
                # Now, save the tags for the blog post
                category = form.cleaned_data['category']

                blog.category.set(category)  # Save the tags for the blog post
                blog.save()
                
                print('ok')
                messages.success(request, "Submitted.")
                return redirect('post_detail', blog.id)

    else:
        messages.error(request, "Invailed form.")
        print(form.errors, form.errors)

    context = {
        'form' : form,
    }
    return render(request, 'baseapp/post_form.html', context)

@login_required(login_url='login')
def PostUpdateView(request, pk):
    post = Post.objects.get(pk=pk)
    form = PostForm(instance = post)



    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            text = form.cleaned_data['category']
            form.save()
            print('ok')
            messages.success(request, "Submitted.")
            return redirect('post_detail', pk)


        else:
            messages.error(request, "Invailed form.")
            print(form.errors, form.errors)
    
    context = {
        'form' : form,
        'post' : post,
    }
    return render(request, 'baseapp/post_update_form.html', context)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Post
    success_url = reverse_lazy('post_list')

@login_required(login_url='login')
def PostDraftListView(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(published = False).order_by('-created_date')
    context = {
        'posts' : posts,
    }
    return render(request, 'baseapp/drafts.html', context)

class PostCategoryView(ListView):
    model = Category
    template_name= 'baseapp/post_category.html'
    context_object_name = 'cat_list'

    def get_queryset(self):
        content={
            'cat': self.kwargs['category'],
            'post': Post.objects.filter(category__name=self.kwargs['category']) 
        }
        return content


   

class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'posts/post_category.html'


############################

def draft_count(request):
    draft = Post.objects.filter(published_date__isnull = True).count

    context={
        'draft':draft
    }
    return render(request, 'baseapp/post_list', context)

@login_required(login_url='login')
def post_publish(request, pk):
    post = Post.objects.get(user = request.user, pk=pk)

    post.published = True
    post.published_date = timezone.now()
    post.save()
    return redirect('post_detail', pk=pk)


@login_required(login_url='login')
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added.")

            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm
    context={
        'form' : form
    }
    return render(request, 'baseapp/comment_form.html', context)

@login_required(login_url='login')
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.comment_approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required(login_url='login')
def comment_edit(request, pk, comment_pk):
    comment = Comment.objects.get(post_id = pk, user = request.user ,pk=comment_pk)
    print(comment)
    form = CommentForm(instance=comment)
    if request.method == 'POST':
        form = CommentForm( request.POST,instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment edited.")

            return redirect('post_detail', pk=comment.post.pk)

        else:
            messages.error(request, "Invailed form.")
            print(form.errors, form.errors)
            return redirect('post_detail', pk=comment.post.pk)
    else:
        context = {
            'form' : form,
        }
        return render(request,'baseapp/comment_form.html', context)



    
@login_required(login_url='login')
def comment_remove(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, user= request.user)
    post_pk = comment.post.pk
    comment.delete()
    
    messages.success(request, "Comment removed.")

    return redirect('post_detail', pk=post_pk)

def category_list(request):
    category_list = Category.objects.exclude(name='uncategorized')

    context={
        'category_list': category_list
    }
    return context

def search_post(request):
    form = PostSearchForm
    q= ''
    c= ''
    results =[]
    query = Q()

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &=Q(category = c)
            if q is not None:
                query &= Q(title__icontains=q)
            results = Post.objects.filter(query)


    context = {
        'form' : form,
        'results' : results,
        'q' : q
    }
    return render(request, 'baseapp/search.html', context)














