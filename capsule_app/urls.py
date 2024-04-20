from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.registerPage, name = 'register_page'),

    path('capsules/<int:pk>', views.CapsuleDetailView.as_view(), name= 'capsule-detail'),
    path('creators/', views.CreatorListView.as_view(), name= 'creators'),
    path('creator/<int:pk>', views.CreatorDetailView.as_view(), name='creator-detail'),
    path('creator/update_creator/<int:creator_id>', views.update_creator, name='update-creator'),
    path('creator/<int:creator_id>/create_capsule', views.create_capsule, name='create-capsule'),
    path('creator/<int:creator_id>/view_capsule/<int:capsule_id>', views.view_capsule, name='view-capsule'),
    path('creator/<int:creator_id>/update_capsule/<int:capsule_id>', views.update_capsule, name='update-capsule'),
    path('creator/<int:creator_id>/delete_capsule/<int:capsule_id>', views.delete_capsule, name='delete-capsule'),
]