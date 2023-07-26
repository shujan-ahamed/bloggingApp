from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings 
from django.contrib import admin

from .views import *

admin.autodiscover()

urlpatterns = [
    path('about/', AboutView, name='about'),
    path('register/', RegistraionView.as_view(), name='register'),
    path('', PostListView, name='post_list'),
    path('post/<str:pk>/', PostDetailView, name='post_detail'),
    path('post/', PostCreateView, name='create_post'),
    path('post/edit/<str:pk>/', PostUpdateView, name='post_edit'),
    path('post/<str:pk>/remove/', PostDeleteView.as_view(), name='post_remove'),
    path('draft/', PostDraftListView, name='post_draft'),
    path('category/<category>', PostCategoryView.as_view(), name='post_category'),
    path('post/publish/<str:pk>/', post_publish, name='post_publish'),
    path('post/<str:pk>/comment/', add_comment_to_post, name='add_comment_to_post'),
    path('comment/<str:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/edit/<str:pk>/<str:comment_pk>/', comment_edit, name='comment_edit'),
    path('comment/remove/<str:pk>/<str:comment_pk>/', comment_remove, name='comment_remove'),  
    path('comment/publilsh/<str:pk>/', comment_approve, name='comment_publish'),        
    path('search/', search_post, name='search_post'),  
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)