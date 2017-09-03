#-*- coding: utf-8 -*-
import time
from django.contrib.auth.decorators import login_required
from content.models import Content, Type, User, Images
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render
from content.forms import ContentForm,TypeForm,ImagesUploadForm
from django.core.exceptions import ObjectDoesNotExist
from commons.paginator import paginator
# from accounts.permission import permission_verify
import json
from accounts.models import Contact
import collections
# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.decorators import permission_required,login_required

@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        role = '超级管理员'
    elif user.is_anonymous():
        role = '匿名用户'
    else:
        role = '普通用户'
    request.role = role
    return render_to_response('base/index.html', {'request': request})

@login_required
def userprofile(request):
    username = request.user
    user = User.objects.filter(username=username).values_list(
        'username', 'email', 'last_login','fullname')
    return render_to_response('profile.html', {'profile': user})



def time_count(content,start_time,end_time):

        start_time = time.strptime(str(start_time).split('+')[0], "%Y-%m-%d %H:%M:%S")
        end_time = time.strptime(
            str(end_time).split('+')[0], "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(end_time)) - int(time.mktime(start_time))

        setattr(content, 'time', str(timestamp // 3600) + '小时' + str(timestamp % 3600 // 60) + '分')


@login_required
@permission_required('content.get_content',raise_exception=True)
def fms_list(request):

    data = {}
    content = Content.objects.select_related().all().order_by('-ctime')
    for i in content:
        time_count(i,i.start_time,i.end_time)
    data = paginator(request, content)
    request.breadcrumbs((('首页', '/'),('故障管理',reverse('fms_list'))))

    return render_to_response('fms/fms.html',data)


@login_required
@permission_required('content.add_content',raise_exception=True)
def fms_add(request):
    error = ""
    if request.method == "POST":
        title = Content.objects.filter(title=request.POST.get('title'))
        form = ContentForm(request.POST)
        if title:
            error = "简述标题冲突!"
        else:
            if form.is_valid():
                tmp = form.save(commit=False)
                tmp.author = request.user

                tmp.save()
                return HttpResponseRedirect(reverse('fms_list'))
    else:
        form = ContentForm()
    return render(request, 'fms/fms_add.html', {'request': request, 'form': form, 'error': error})


@login_required
@permission_required('content.detail_content',raise_exception=True)
def fms_detail(request, id):
    
    data = {}
    try:
        content = Content.objects.select_related().get(id=id)
        time_count(content,content.start_time,content.end_time)
        data['content'] = content
        data['request'] = request
    except ObjectDoesNotExist:
        data['error'] = '该报告不存在!'
    return render_to_response('fms/fms_detail.html',data)

@login_required
@permission_required('content.edit_content',raise_exception=True)
def fms_edit(request):

    error = ""
    id = request.GET.get("id")
    if id:
        try:
            user = User.objects.get(username=str(request.user.username))
            content = Content.objects.get(id=id)
            if not user.is_superuser and content.author.username != request.user.username:
                error = "没有权限!"
                form = ""
            else:
                form = ContentForm(instance=content)
                id = id
        except:
            error = "该报告不存在"
            form = ""

    if request.method == "POST":
        content = Content.objects.get(id=id)
        form = ContentForm(request.POST,instance=content)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.save()
            return HttpResponseRedirect(reverse('fms_list'))
    return render(request, 'fms/fms_edit.html', {'request': request, 'form': form, 'error': error,'id':id})




@login_required
@permission_required('content.update_type',raise_exception=True)
def type_add(request):

    error = ""
    if request.method == "POST":
        type_name=request.POST.get('type_name')
        name = Type.objects.filter(name=type_name)
        if name:
            error = "类型名称冲突!"
        else:
            Type.objects.create(name=type_name)
            return HttpResponseRedirect(reverse('type_add'))
    else:
        form = Type.objects.all()
    request.breadcrumbs((('首页', '/'),('故障类型',reverse('type_add'))))

    return render(request, 'fms/type.html', {'request': request, 'form': form, 'error': error})



@login_required
@permission_required('content.del_type',raise_exception=True)
def type_del(request,id):

    if id:
        Content.objects.filter(type_id=id).update(type_id=None)
        Type.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('type_add'))



@login_required
def upload_images(request):
    if request.method == 'POST':

        form = ImagesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.url = request.FILES['editormd-image-file']
            tmp.save()
            url = '/uploads/' + str(tmp.url)
            return HttpResponse(json.dumps({"success":1,"message":"ok","url":url}))

    return HttpResponse('allowed only via POST')


def get_email(request):

    data = []
    contact = Contact.objects.all()
    for i in contact:
        data.append({"id":i.id,"name":i.name})
    return HttpResponse(json.dumps(data))


def exec_send(content_id,email_list):

    data = collections.defaultdict(dict)

    from_email = settings.DEFAULT_FROM_EMAIL
    text_content = '这是一封重要的邮件.'

    content = Content.objects.select_related().get(id=content_id)
    data['content'] = content
    subject = '【故障报告】' + str(content.title)

    time_count(content,content.start_time,content.end_time)

    msg_html = render_to_string('mail/detail_template.html', data)
    # send_mail('Subject here', 'Here is the message.', settings.DEFAULT_FROM_EMAIL,email_list, fail_silently=False)
    msg = EmailMultiAlternatives(subject, text_content, from_email, email_list)
    msg.attach_alternative(msg_html, "text/html")
    msg.send()

@login_required
def send_mails(request):
    
    if request.method == "POST":
        content_id = request.POST.get('content_id')
        email_group = json.loads(request.POST.get('email_group'))
        if email_group:
            contact = Contact.objects.filter(name__in=email_group).values('email')

        email_list = (',').join([i['email'] for i in contact]).split(',')
        exec_send(content_id,email_list)
    return HttpResponse('ok')
