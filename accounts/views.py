#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from django.shortcuts import render,render_to_response,reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from accounts.forms import LoginForm,UserForm
from django.conf import settings
from accounts.models import User
from commons.paginator import paginator
from django.contrib.auth.models import Group,Permission
import json,collections
from django.contrib.auth.decorators import permission_required,login_required,user_passes_test

def login(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        next = request.path
        if next == settings.LOGIN_URL:
            next = '/'
        return render_to_response('accounts/login.html',{'next':next})

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST['next'])
        else:
            error = form.errors
    else:
        form = LoginForm(request)
    data = {'request': request,'form':  form, 'error': error}
    return render_to_response('accounts/login.html', data)

def logout(request):
    
    auth.logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


@login_required
def get_groups(request):

    group = Group.objects.values_list('id','name')
    groups = json.dumps([(i[0],i[1]) for i in group])

    return groups


@login_required
@permission_required('accounts.get_user',raise_exception=True)
def accounts_user(request):

    data = {}
    user = User.objects.all()
    data = paginator(request, user)
    request.breadcrumbs((('首页', '/'),('用户管理',reverse('accounts_user'))))

    return render_to_response('accounts/user/user.html',data)


@login_required
@permission_required('accounts.add_user',raise_exception=True)
def accounts_add(request):

    error = ""
    if request.method == "POST":
        groups = request.POST.getlist('groups')
        new_username = request.POST.get('username')
        username = User.objects.filter(username=new_username)

        form = UserForm(request.POST)
        if username:
            error = u'该账号已存在!'
        else:
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                user.groups.clear()
                user.groups.add(*groups)
                return HttpResponseRedirect(reverse('accounts_user'))
    else:
        form = UserForm()

    groups = get_groups(request)
    print(groups)
    request.breadcrumbs((('首页', '/'),('用户列表',reverse('accounts_user')),('添加用户',reverse('accounts_add'))))

    return render(request, 'accounts/user/user_add.html', {'request': request, 'form': form, 'error': error, 'groups': groups})


@login_required
@permission_required('accounts.edit_user',raise_exception=True)
def accounts_edit(request):

    error = ""
    id = request.GET.get('id')
    if id:
        try:
            user = User.objects.get(id=id)
            user.password=""
            form = UserForm(instance=user)
            form.groups = (',').join([u.name for u in user.groups.all()]) if user.groups.all() else ''
        except:
            error = u"不存在"
            form = ""
    if request.method == "POST":
        groups = request.POST.getlist('groups')
        user = User.objects.get(id=id)
        old_password = user.password
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if user.password:
               user.set_password(form.cleaned_data['password'])
            else:
               user.password = old_password
            user.save()
            user.groups.clear()
            user.groups.add(*groups)
            return HttpResponseRedirect(reverse('accounts_user'))
    groups = get_groups(request)
    request.breadcrumbs((('首页', '/'),('用户管理',reverse('accounts_user')),('编辑用户',reverse('accounts_edit'))))
    return render(request, 'accounts/user/user_edit.html', {'request': request, 'form': form, 'id': id,'error': error, 'groups': groups})

@login_required
@permission_required('accounts.del_user',raise_exception=True)
def accounts_del(request):
    id = request.GET.get('id')
    if id:
        User.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('accounts_user'))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def accounts_group(request):

    data = {}
    group = Group.objects.all()
    users = User.objects.values_list('id','username','fullname')
    data = paginator(request, group)
    request.breadcrumbs((('首页', '/'),('用户管理',reverse('accounts_group'))))
    data['users'] = json.dumps([(i[0],i[1],"%s(%s)"%(i[1],i[2])) for i in users])

    return render_to_response('accounts/user/group.html',data)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def accounts_group_update(request):

    if request.method == "POST":
        group_name = request.POST.get('group_name')
        action = request.POST.get('action')
        ids = json.loads(request.POST.get('users')) if request.POST.get('users') else []
        try:
            group,created = Group.objects.get_or_create(name=group_name)
            group.user_set.clear()
            if ids:
                users = User.objects.filter(id__in = ids)
                group.user_set.add(*users)

        except Exception as e:
            print(e)

    return HttpResponseRedirect(reverse('accounts_group'))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def accounts_group_del(request):

    id = request.GET.get('id')
    if id:
        Group.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('accounts_group'))

