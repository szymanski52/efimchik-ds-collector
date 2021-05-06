from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, DataSetUploadForm
from .models import DataSet


def render_main(request):
    return render(request, 'ds_manager/main.html')


def render_datasets(request):
    context = {}
    context['upload_form'] = DataSetUploadForm()
    datasets = DataSet.objects.filter(user_id=request.user.id)
    context['datasets'] = datasets
    return render(request, 'ds_manager/datasets.html', context)


def render_explore(request):
    return render(request, 'ds_manager/explore.html')


def render_auth(request):
    context = {}
    context['user_form'] = UserRegistrationForm()
    context['form'] = AuthenticationForm()
    return render(request, 'ds_manager/auth.html', context)


def render_dataset(request, ds_id):
    return render(request, 'ds_manager/dataset.html')


def render_profile(request):
    return render(request, 'ds_manager/profile.html')


def upload_dataset(request):
    context = {}
    if request.method == 'POST':
        upload_form = DataSetUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            new_ds = upload_form.save(commit=False)
            new_ds.user_id = request.user.id
            new_ds.save()
        else:
            print('ERRORS:', upload_form.errors)
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
