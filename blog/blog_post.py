from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .forms import PostForm
from .models import Post, Comment


class PostListView(ListView):
    paginate_by = 5
    model = Post
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['pages'] = context['paginator'].page_range
        if context['page_obj'].has_next():
            context['next_page'] = context['page_obj'].next_page_number()
        if context['page_obj'].has_previous():
            context['prev_page'] = context['page_obj'].previous_page_number()
        return context

    def get_queryset(self):
        topic = self.kwargs.get('topic')
        if topic:
            return Post.objects.filter(topic=topic)
        return Post.objects.all()


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'blog/post_detail.html'


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/home'
    template_name = 'blog/post_list.html'


class PostCreateNew(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_edit.html'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_post = Post.objects.create(author=self.request.user, **form.cleaned_data)
            self.object = new_post
            coments = Comment.objects.filter(comment_to=self.object)
            self.extra_context = {"comets": coments}
            return  redirect(self.get_success_url())
        return self.form_invalid(form)


class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_update.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_object(self):
        return Post.objects.get(pk=self.kwargs.get('pk'))


