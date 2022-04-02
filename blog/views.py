from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# def home(request):
#     context = {'posts' : Post.objects.all()}
#     return render(request, 'blog/blog-home.html', context)

def about(request):
    return render(request, 'blog/blog-about.html', {'title' : 'About'})  

#class baseview list view
class PostListView(ListView):
    model = Post
    template_name = 'blog/blog-home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5    
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get ('username'))
        return Post.objects.filter(auther=user).order_by('-date_posted')

#class baseview detailview(hiển thị chi tiết bài post)
class PostDetailView(DetailView):
    model = Post

#class baseview form tạo ra bài post mới
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.auther = self.request.user
        return super().form_valid(form)

#class baseview update post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.auther = self.request.user
        return super().form_valid(form)
    # kiểm tra bài post có phải của user này tạo ra hay không
    def test_func(self):
        post = self.get_object()
        if post.auther == self.request.user:
            return True
        return False   

#class baseview delete post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post           
    success_url = '/'

    # kiểm tra bài post có phải của user này tạo ra hay không
    def test_func(self):
        post = self.get_object()
        if post.auther == self.request.user:
            return True
        return False  