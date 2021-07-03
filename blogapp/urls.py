from django.urls import path
from blogapp import views

app_name = 'blogapp'

urlpatterns = [

    path('create/',views.createpost.as_view(),name='createpost'),
    path('list/',views.post_list.as_view(),name='post_list'),
    path('draft_list/',views.draft_list.as_view(),name='draft_list'),
    path('detail/<int:pk>',views.PostDetail.as_view(),name='post_detail'),
    path('draftpost/<int:pid>',views.draftpost,name='draft_post'),
    path('draftdetail/<int:pk>',views.DraftDetail.as_view(),name='draft_detail'),
    path('edit/<int:pk>',views.UpdatePost.as_view(),name='editpost'),
    path('delete/<int:pk>',views.PostDelete.as_view(),name='deletepost'),
    path('comment/<int:cid>',views.CreateComment,name='comment'),
    path('editcomment/<int:cid>',views.editcomment,name='edit_comment'),
    path('deletecomment/<int:cid>',views.delete_comment,name='delete_comment'),
]
