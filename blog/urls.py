from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, 
                    PostPopularView, PostListUserView, fileUpload, PostDeleteView, like_post)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('popular/', PostPopularView.as_view(), name='post_list_popular'),
    path('user/<str:blog>/', PostListUserView.as_view(), name='post_user'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('upload', fileUpload, name='fileupload'),
    path('like/<int:pk>', like_post, name='like_post'),
    
]


urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
