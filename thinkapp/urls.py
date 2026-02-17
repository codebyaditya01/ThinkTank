from thinkapp import views
from django.urls import path

urlpatterns = [
    path('', views.homelistpage, name='list'),

    # Question URLs
    path('addques/', views.addquestion, name='addques'),
    path('question/<int:id>/updateques/', views.updateques, name='updateques'),
    path('question/<int:id>/deleteques/', views.deleteques, name='deleteques'),

    # Answer URLs
    path('answer/<int:id>/updateans/', views.updateans, name='updateans'),
    path('answer/<int:id>/deleteans/', views.deleteans, name='deleteans'),

    # Question Details (also handles adding answer)
    path('details/<int:id>/', views.details, name='details'),  

    # Comments
    path('comments/<int:quesid>/<int:ansid>/', views.comments, name='comments'),
    path('comments/<int:quesid>/<int:ansid>/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    # Profile
    path('profile/', views.profile_view, name='profileview'),  
]

