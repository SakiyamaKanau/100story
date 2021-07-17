from django.shortcuts import render,resolve_url,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView,CreateView,DetailView,UpdateView,DeleteView,ListView
from .models import Post,Like,Category,SubCategory
from django.urls import reverse_lazy
from .forms import PostForm,LoginForm,SignUpForm,SearchForm #SearchFormを追加
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin 
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.core.paginator import Paginator #paginatorを追加する

class OnlyMyPostMixin(UserPassesTestMixin):
  raise_exception = True
  def test_func(self):
    post = Post.objects.get(id = self.kwargs['pk'])
    return post.author == self.request.user


class index(TemplateView):
  template_name = 'blog_app/index.html'

  def get_context_data(self,*args, **kwargs):
      context = super().get_context_data(**kwargs)
      post_list = Post.objects.all().order_by('-created_at')
      context = {
        'post_list': post_list,
      }
      return context

class PostCreate(LoginRequiredMixin,CreateView):
  model = Post
  form_class = PostForm
  success_url = reverse_lazy('blog_app:index')
  def form_valid(self, form):
    form.instance.author_id = self.request.user.id
    return super(PostCreate,self).form_valid(form)

  def get_success_url(self):
    messages.success(self.request,'100esを登録しました。')
    return resolve_url('blog_app:index')

class PostDetail(DetailView):
  model = Post

  def get_context_data(self, *args,**kwargs):
      detail_data  = Post.objects.get(id=self.kwargs['pk'])
      category_posts = Post.objects.filter(category = detail_data.category).order_by('-created_at')[:5]
      params = {
        'object':detail_data,
        'category_posts':category_posts,
      }
      return params


class PostUpdate(OnlyMyPostMixin,UpdateView):
  model = Post
  form_class = PostForm

  def get_success_url(self):
    messages.info(self.request, '100esを更新しました。')
    return resolve_url('blog_app:post_detail',pk=self.kwargs['pk'])

class PostDelete(OnlyMyPostMixin,DeleteView):
  model = Post
  def get_success_url(self):
    messages.info(self.request, '100esを削除しました')
    return resolve_url('blog_app:index')

class PostList(ListView):
  model = Post
  #5件ごとにページを切り替える
  paginate_by = 5
  def get_queryset(self):
    return Post.objects.all().order_by('-created_at')

class Login(LoginView):
   form_class = LoginForm
   template_name = 'blog_app/login.html'

class Logout(LogoutView):
  template_name = 'blog_app/logout.html'

class SignUp(CreateView):
  form_class = SignUpForm
  template_name = 'blog_app/signup.html'
  success_url = reverse_lazy('blog_app:index')

  def form_valid(self, form):
    user = form.save()
    login(self.request,user)
    self.object = user
    messages.info(self.request,'ユーザー登録をしました。')
    return HttpResponseRedirect(self.get_success_url())

@login_required
def Like_add(request,post_id):
    post = Post.objects.get(id = post_id)
    is_liked = Like.objects.filter(user = request.user,post = post_id).count()
    if is_liked > 0:
      messages.info(request, 'すでにお気に入りに追加済みです。')
      return redirect('blog_app:post_detail', post.id)
    like = Like()
    like.user = request.user
    like.post = post
    like.save()

    messages.success(request, 'お気に入りに追加しました')
    return redirect('blog_app:post_detail', post.id)

class CategoryList(ListView):
  model = Category

class SubCategoryList(ListView):
  model = SubCategory

class CategoryDetail(DetailView):
  model = Category
  slug_field = 'name_en'
  slug_url_kwarg = 'name_en'

  def get_context_data(self,*args, **kwargs):
    detail_data = Category.objects.get(name_en = self.kwargs['name_en'])
    category_posts = Post.objects.filter(category = detail_data.id).order_by('-created_at')

    params = {
      'object':detail_data,
      'category_posts':category_posts,
    }

    return params

#クエスチョンのQ
def Search(request):
  if request.method == 'POST':
    searchform = SearchForm(request.POST)

    if searchform.is_valid():
      freeword = searchform.cleaned_data['freeword']
      search_list = Post.objects.filter(Q(title__icontains = freeword)|Q(content__icontains = freeword))

    params = {
       'search_list':search_list,
     }

    return render (request, 'blog_app/search.html',params) #クエスチョンのQ