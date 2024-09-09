from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stories/', views.get_stories, name='get-stories'),
    path('create/', views.create, name='create'),
    path('<int:story_id>/', views.detail, name='detail'),
    path('<int:story_id>/delete/', views.delete, name='delete'),
    path('filter/<slug:slug>', views.filter_, name='list-by'),
    path('<int:story_id>/like/', views.like, name='like'),
    path('<int:obj_id>/comment/', views.comment, name='comment'),
    path('validate-title/', views.validate_title, name='validate-title'),
    path('validate-content/', views.validate_content, name='validate-content'),
    path('validate-tag/', views.validate_tag, name='validate-tag'),
]
