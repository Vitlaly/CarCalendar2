from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import timedelta, datetime
from .models import *
from .forms import ComponentForm, CreateUserForm, OwnerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group, User
from django.forms import inlineformset_factory


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    context = {'form': form}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='owners_car')
            user.groups.add(group)
            Owner.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )
            messages.success(request,  "Account was created for" + user.username)
            return redirect('login')

    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['admins'])
def home(request):
    components = Component.objects.all()
    owners = Owner.objects.all()
    context = {'components': components, 'owners': owners}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def my_components(request):
    now = datetime.datetime.now()
    now3 = timedelta(20)
    owner = Owner.objects.get(name=request.user)
    components = owner.component_set.all()
    components_count = components.count()
    context = {'components': components,
               'owner': owner,
               'components_count': components_count,
               'now': now}
    return render(request, 'accounts/my_components.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def owner(request, pk):
    car_owner = Owner.objects.get(id=pk)
    components = car_owner.component_set.all()
    # component is a child object owner`s model
    components_count = components.count()

    context = {'car_owner': car_owner, 'components': components, 'components_count': components_count}

    return render(request, 'accounts/owner.html', context)


@login_required(login_url='login')
def createComponent(request, pk_test):
    componentSet = inlineformset_factory(Owner, Component,
                                         fields=('name',
                                                 'resource',
                                                 'unit',
                                                 'mileage_installation',
                                                 'date_installation',
                                                 'description',
                                                 'status'),
                                         extra=1, can_delete=False,
                                         )
    user = Owner.objects.get(id=pk_test)
    formset = componentSet(queryset=Component.objects.none(), instance=user)
    context = {'formset': formset}
    if request.method == "POST":
        # form = ComponentForm(request.POST,)
        formset = componentSet(request.POST, instance=user)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    return render(request, 'accounts/component_form.html', context)


@login_required(login_url='login')
def updateComponent(request, pk):
    component = Component.objects.get(id=pk)
    form = ComponentForm(instance=component)
    context = {'form': form, 'component': component}

    if request.method == 'POST':
        form = ComponentForm(request.POST, instance=component)
        if form.is_valid():
            form.save()
            return redirect('my_components')
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def ownerUpdate(request):
    owner = Owner.objects.get(name=request.user)
    form = OwnerForm(instance=owner)
    context = {'form': form, 'owner': owner}
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'accounts/owner_form.html', context)


@login_required(login_url='login')
def deleteComponent(request, pk):
    component = Component.objects.get(id=pk)
    context = {'component': component}
    if request.method == "POST":
        component.delete()
        return redirect('my_components')
    return render(request, 'accounts/delete_component.html', context)







