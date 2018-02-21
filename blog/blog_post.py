from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from .forms import PostForm
from .models import Post, Comment


class PostListView(ListView):

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        topic = kwargs.get('topic', None)
        if topic:
            self.object_list = self.get_queryset().filter(topic=topic)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        return Post.objects.all()


class PostDetailView(DetailView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_queryset(self):
        return Post.objects.all()


class PostCreateNew(CreateView):

    form_class = PostForm

    def get(self, request, *args, **kwargs):
        context = {'form': PostForm()}
        self.object = None
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        form = PostForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            new_post = Post()
            title = form.cleaned_data.get('title', None)
            topic = form.cleaned_data.get('topic', None)
            new_post = Post.objects.filter(topic=topic, title=title)
            if not new_post:
                new_post = Post()
                new_post.topic = topic
                new_post.post_img = form.cleaned_data.get('post_img', None)
                new_post.title = title
                new_post.text = form.cleaned_data.get('text', None)
                new_post.link = form.cleaned_data.get('link', None)
                new_post.author = self.request.user
                new_post.save()
                self.object = new_post
            else:
                self.object = new_post[0]
            coments = Comment.objects.filter(comment_to=self.object)
            self.extra_context = {"comets": coments}
            return HttpResponseRedirect(reverse('blog:post_detail', kwargs={'pk': self.object.pk}))
        else:
            return self.form_invalid(form)
