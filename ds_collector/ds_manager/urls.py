from django.urls import path

from . import views

urlpatterns = [
    path('', views.render_main, name='main'),
    path('datasets', views.render_datasets, name='datasets'),
    path('dataset/<ds_id>', views.render_dataset, name='dataset'),
    path('profile', views.render_profile, name='profile'),
    path('explore', views.render_explore, name='explore'),
    path('register', views.register, name='register'),
    path('auth', views.render_auth, name='auth'),
    path('upload', views.upload_dataset, name='upload'),
]
