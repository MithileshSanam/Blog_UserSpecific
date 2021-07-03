from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from blogapp.models import Post,Comment
from django.urls import reverse_lazy,reverse
from blogapp.forms import PostForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


def home(request):
    if request.user.is_authenticated:
        post_list = Post.objects.filter(published_date__isnull = False).filter(author=request.user).order_by('-id')
        return render(request,'blogapp/home.html',context={'post_list':post_list})
    else:
        return render(request,'blogapp/home.html')

def registration(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')
        if pwd1 == pwd2:
            user_check = User.objects.get_or_create(username=name)
            if user_check[1] == False:
                return render(request,'registration/registration.html')
            else:
                user_obj = user_check[0]
                user_obj.set_password(pwd1)
                user_obj.is_superuser = True
                user_obj.save()
                return HttpResponseRedirect(reverse('login'))
    return render(request,'registration/registration.html')

class createpost(CreateView,LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blogapp/post_detail.html'
    model = Post
    template_name = 'blogapp/createpost.html'
    form_class = PostForm

    def post(self,request):
        postform = PostForm(self.request.POST)
        if postform.is_valid():
            post_obj = postform.save(commit=False)
            post_obj.author = request.user
            if 'submit_post' in self.request.POST:
                post_obj.publish()
            else:
                post_obj.save()
        return HttpResponseRedirect(reverse('blogapp:post_list'))

class draft_list(ListView,LoginRequiredMixin):
    redirect_field_name = 'blogapp/home.html'
    model = Post
    context_object_name = 'post_list'
    template_name='blogapp/draft_list.html'
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).filter(author=self.request.user).order_by('-id')

class post_list(ListView,LoginRequiredMixin):
    redirect_field_name = 'blogapp/post_list.html'
    model = Post
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-id')

class PostDetail(DetailView,LoginRequiredMixin):
    redirect_field_name = 'blogapp/post_detail.html'
    model = Post

class DraftDetail(DetailView,LoginRequiredMixin):
    redirect_field_name = 'blogapp/home.html'
    model = Post
    template_name='blogapp/draft_detail.html'

class UpdatePost(UpdateView,LoginRequiredMixin):
    redirect_field_name = 'blogapp/post_detail.html'
    model = Post
    template_name = 'blogapp/editpost.html'
    form_class = PostForm

    def get(self,request,pk):
        if Post.objects.get(id=pk).author != self.request.user:
            return HttpResponseRedirect(reverse('blogapp:post_list'))
        return super().get(request,pk)


class PostDelete(DeleteView,LoginRequiredMixin):
    redirect_field_name = 'blogapp/deleteconfirm.html'
    model = Post
    success_url = reverse_lazy('blogapp:post_list')
    template_name = 'blogapp/deleteconfirm.html'
    def get(self,request,pk):
        if Post.objects.get(id=pk).author != self.request.user:
            return HttpResponseRedirect(reverse('blogapp:post_list'))
        return super().get(request,pk)

@login_required
def editcomment(request,cid):
    txt = request.POST.get('comment_text')
    com_obj = Comment.objects.get(id=cid)
    pid = com_obj.post.id
    com_obj.text = txt
    com_obj.save()
    return HttpResponseRedirect(reverse('blogapp:post_detail',kwargs={'pk':pid}))

@login_required
def delete_comment(request,cid):
    com_obj = Comment.objects.get(id=cid)
    pid = com_obj.post.id
    com_obj.delete()
    return HttpResponseRedirect(reverse('blogapp:post_detail',kwargs={'pk':pid}))

@login_required
def draftpost(request, pid):
    if request.method == 'POST':
        post = Post.objects.get(id=pid)
        if 'draft_delete' in request.POST:
            post.delete()
            return HttpResponseRedirect(reverse('blogapp:post_list'))
        else:
            d_title = request.POST.get('draft_title')
            d_text = request.POST.get('draft_text')
            post.text = d_text
            post.title = d_title
            post.publish()
        return HttpResponseRedirect(reverse('blogapp:post_detail',kwargs={'pk':pid}))

@login_required
def CreateComment(request, cid):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('blogapp:post_detail',kwargs={'pk':cid}))
    if request.method == 'POST':
        comment_author = request.user
        comment_text = request.POST.get('comment')
        comment_post = Post.objects.get(id=cid)
        com_obj = Comment.objects.get_or_create(post=comment_post,text=comment_text,author=comment_author)
        if com_obj[1] == True:
            com_obj[0].save()
        return HttpResponseRedirect(reverse('blogapp:post_detail',kwargs={'pk':cid}))
