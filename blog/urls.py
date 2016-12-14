from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


edit_patern = r'^post/(?P<pk>[0-9]+)/edit/$'

#додаємо URL шаблон
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^home$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^new$', views.post_new, name='post_new'),
    url(edit_patern, views.post_edit, name='post_edit'),
    url(r'^log_in$', views.log_in, name='log_in'),
    url(r'^travel$', views.post_list_travel, name='travel'),
    url(r'^food$', views.post_list_food, name='food'),
    url(r'^sport$', views.post_list_sport, name='sport'),
    url(r'^sing_up$', views.sing_up, name='sing_up'),
    url(r'^post/(?P<pk>[0-9]+)/dell/$', views.post_dell, name='post_dell'),
    url(r'^registr$', views.registration, name='registration'),
    url(r'^user_login$', views.user_login, name='login'),
    url(r'^log_out$', views.user_logout, name='logout'),
    url(r'^add_sportnews', views.get_sportnews, name='addsport'),
    url(r'^add_foodnews', views.get_foodnews, name='addfood'),
    url(r'^add_travelnews', views.get_travelnews, name='addtravel'),
    url(r'^post/(?P<pk>[0-9]+)/add_coment$', views.add_coment, name='add_coment'),
    url(r'^search', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


