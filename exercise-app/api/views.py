from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from collections import Counter
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from blog.models import Post,Category
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q


def home(request):
    context = {
        'Posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(exercisename__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'Posts':result }
    return render(request,template,context)
   


def getfile(request):
   return serve(request, 'File')




def post_list(request):
    queryset = Post.objects.all().order_by('-date_Posted')
    # get count of all posts in the month 
    month = queryset.filter( date_Posted__month__gte= timezone.now().month)
    # don't repeat day in the month
    day = []
    for i in month:
        if i.date_Posted.day not in day:
            day.append(i.date_Posted.day)

    print(day)
    # get count of all posts in the year
    year = queryset.filter( date_Posted__year__gte= timezone.now().year) 
    yearDay = []
    for i in year: 
        if i.date_Posted.month not in yearDay:
            yearDay.append(i.date_Posted.month)
             

    
    YMD = []
    for d in Post.objects.filter( date_Posted__year__gte= timezone.now().year):
        YMD.append(d.date_Posted.strftime("%Y-%m-%d")) 
        
     
    YMD = list(set(YMD))
    YM = []
    for d in YMD:
        YM.append(d.split('-')[1])
    
    YM = dict(Counter(YM))
    YM = sorted(YM.items(), key=operator.itemgetter(1), reverse=True)

    # pagistion page for the list of posts
    user_list = Post.objects.all().order_by('-date_Posted')
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    
    
    usr = User.objects.all()
    context = {
        'usr': list(usr.values('id','username','profile','post')),
        'Posts': list(queryset.values('id','exercisename','author','hour','min','date_Posted'))
        # 'year': list(posts) 
    }
    return JsonResponse(context)

def post_all(request, pk):
    YMD = []
    for d in Post.objects.all():
        YMD.append(d.date_Posted.strftime("%Y-%m-%d"))
        
    YMD = list(set(YMD))
            
    # return render(request, 'blog/post_all.html', {'days': day})
    return JsonResponse(YMD , safe=False)

def userpost(request, username):
    queryset = Post.objects.filter( author=username  ).order_by('-date_Posted')
    # get count of all posts in the month 
    month = queryset.filter( author=username, date_Posted__month__gte= timezone.now().month)
    # don't repeat day in the month
    day = []
    for i in month:
        if i.date_Posted.day not in day:
            day.append(i.date_Posted.day)

    print(day)
    # get count of all posts in the year
    year = queryset.filter( author=username, date_Posted__year__gte= timezone.now().year) 
    yearDay = []
    for i in year: 
        if i.date_Posted.month not in yearDay:
            yearDay.append(i.date_Posted.month)
             

    
    YMD = []
    for d in Post.objects.filter( author=username, date_Posted__year__gte= timezone.now().year):
        YMD.append(d.date_Posted.strftime("%Y-%m-%d")) 
        
     
    YMD = list(set(YMD))
    YM = []
    for d in YMD:
        YM.append(d.split('-')[1])
    
    YM = dict(Counter(YM))
    YM = sorted(YM.items(), key=operator.itemgetter(1), reverse=True)
    
    usr = User.objects.get(id=username)
    context = {
        'usr': usr,
        'Posts': queryset,
        'Category': Category.objects.filter(post__author__id=username).distinct(),
        'days': day,
        'years': yearDay,
        'YMD': YMD,
        'YM': YM,
        'month': month,
        'year': year
    }
    return render(request, 'blog/user_Posts.html', context) 
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_Posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'Posts'
    paginate_by = 211

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_Posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/Post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/Post_form.html'
    fields = ['exercisename', 'hour','min']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/Post_form.html'
    fields = ['exercisename', 'hour','min']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        Post = self.get_object()
        if self.request.user == Post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/Post_confirm_delete.html'

    def test_func(self):
        Post = self.get_object()
        if self.request.user == Post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'exercisename': 'About'})
