from django.conf.urls import url
from django.views.generic import TemplateView

from blog.views import MyLoginView
from .blog_post import PostListView, PostDetailView, PostCreateNew, PostDeleteView, PostUpdateView
from . import views
from django.conf import settings
from django.conf.urls.static import static

edit_patern = r'^post/(?P<pk>[0-9]+)/edit/$'

#додаємо URL шаблон
urlpatterns = [
    url(r'^$', PostListView.as_view(), name='base'),
    url(r'^home/$', PostListView.as_view(), name='post_list'),
    url(r'^(?P<topic>[food|travel|sport]+)/$', PostListView.as_view(template_name='blog/post_list.html'), name='post_by_topic'),
    url(r'^post/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new$', PostCreateNew.as_view(), name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/update$', PostUpdateView.as_view(), name='post_update'),
    url(r'^post/(?P<pk>[0-9]+)/dell/$', PostDeleteView.as_view(), name='post_dell'),
    url(r'^add_sportnews$', views.get_sportnews, name='addsport'),
    url(r'^add_foodnews$', views.get_foodnews, name='addfood'),
    url(r'^add_travelnews$', views.get_travelnews, name='addtravel'),
    url(r'^post/(?P<pk>[0-9]+)/add_coment/$', views.add_coment, name='add_coment'),
    url(r'^search$', views.search, name='search'),
    url(r'^login$', MyLoginView.as_view(template_name='blog/log_in.html'), name='login'),
    url(r'^signup$', views.SignupForm.as_view(), name='signup'),
    url(r'^logout$', views.user_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


