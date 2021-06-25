import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.encoding import smart_str

from .forms import UserRegistrationForm, DataSetUploadForm, SearchForm
from .models import DataSet, UserFollowing
import os


def render_main(request):
    return render(request, 'ds_manager/main.html')


def render_datasets(request):
    context = {}
    context['upload_form'] = DataSetUploadForm()
    datasets = DataSet.objects.filter(user_id=request.user.id)
    context['datasets'] = datasets
    return render(request, 'ds_manager/datasets.html', context)


def download_dataset(request, ds_id):
    ds = DataSet.objects.get(pk = ds_id)
    path_to_file = ds.csv_file

    response = HttpResponse(content_type='application/force-download')
    print(ds.csv_file)
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(ds.csv_file)
    response['X-Sendfile'] = smart_str(path_to_file)
    return response


def render_explore(request):
    context = {}
    public_datasets = DataSet.objects.filter(access=1)
    for i in public_datasets:
        i.cover = i.cover.url[11:]
    context['public'] = public_datasets
    return render(request, 'ds_manager/explore.html', context)


def render_auth(request):
    context = {}
    context['user_form'] = UserRegistrationForm()
    context['form'] = AuthenticationForm()
    return render(request, 'ds_manager/auth.html', context)


def render_dataset(request, ds_id):
    context = {}
    ds_info = DataSet.objects.get(id=ds_id)
    cover = ds_info.cover.url[11:]
    context['ds_info'] = ds_info
    context['cover'] = cover
    try:
        data = pd.read_csv('.' + ds_info.csv_file.url)
        context['data'] = data.head()
    except pd.errors.ParserError:
        error = 'Unable to process the data'
        context['message'] = error
    return render(request, 'ds_manager/dataset.html', context)


def edit_dataset(request, ds_id):
    context = {}
    ds_info = DataSet.objects.get(id=ds_id)
    cover = ds_info.cover.url[11:]
    context['ds_info'] = ds_info
    context['cover'] = cover
    try:
        data = pd.read_csv('.' + ds_info.csv_file.url)
        context['data'] = data
    except pd.errors.ParserError:
        error = 'Unable to process the data'
        context['message'] = error
    return render(request, 'ds_manager/edit_ds.html', context)


def render_profile(request):
    context = {}

    return render(request, 'ds_manager/profile.html', context)


def search(request):
    context = {}
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        users = User.objects.filter(username=search_form['query'].value())
        context['users'] = users
    return render(request, 'ds_manager/search.html', context)


def upload_dataset(request):
    context = {}
    if request.method == 'POST':
        upload_form = DataSetUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            new_ds = upload_form.save(commit=False)
            new_ds.user_id = request.user.id
            new_ds.save()
    else:
        upload_form = DataSetUploadForm()
    context['upload_form'] = upload_form
    return render(request, 'ds_manager/datasets.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
    else:
        user_form = UserRegistrationForm()
    return render(request, 'ds_manager/main.html')
