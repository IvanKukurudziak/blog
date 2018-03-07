from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from blog.views import get_foodnews, get_sportnews, get_travelnews, MyLoginView, SignupFormView, add_coment, search, user_logout
from blog.blog_post import PostListView, PostDetailView, PostCreateNew, PostDeleteView, PostUpdateView

edit_patern = r'^post/(?P<pk>[0-9]+)/edit/$'

#додаємо URL шаблон
urlpatterns = [
    url(r'^$', PostListView.as_view(), name='base'),
    url(r'^home/$', PostListView.as_view(), name='post_list'),
    url(r'^(?P<topic>[food|travel|sport]+)/$', PostListView.as_view(), name='post_by_topic'),
    url(r'^post/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new$', PostCreateNew.as_view(), name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/update$', PostUpdateView.as_view(), name='post_update'),
    url(r'^post/(?P<pk>[0-9]+)/dell/$', PostDeleteView.as_view(), name='post_dell'),
    url(r'^add_sportnews$', get_sportnews, name='addsport'),
    url(r'^add_foodnews$', get_foodnews, name='addfood'),
    url(r'^add_travelnews$', get_travelnews, name='addtravel'),
    url(r'^post/(?P<pk>[0-9]+)/add_coment/$', add_coment, name='add_coment'),
    url(r'^search/$', search, name='search'),
    url(r'^login/$', MyLoginView.as_view(), name='login'),
    url(r'^signup/$', SignupFormView.as_view(), name='signup'),
    url(r'^logout/$', user_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


