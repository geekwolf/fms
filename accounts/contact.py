# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from accounts.forms import ContactForm
from accounts.models import Contact,User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.conf import settings
from django.contrib.auth.decorators import permission_required,login_required


@login_required
@permission_required('accounts.get_contact',raise_exception=True)
def contact_list(request):

    error = ''
    data = {}
    current_page = request.GET.get("page", 1)
    page_number = 15
    Contacts = Contact.objects.select_related().all()
    pages = Paginator(Contacts, page_number)
    try:
        Contacts = pages.page(current_page)
    except EmptyPage:
        Contacts = pages.page(current_page)
    data["content"] = Contacts
    data["form"] = []
    for  i in Contacts:
        data["form"].append({"id":i.id,"name":i.name,"email":i.email})
    data["pages"] = pages
    data["request"] = request
    request.breadcrumbs((('首页', '/'),('邮件列表',reverse('contact_list'))))

    return render_to_response('accounts/contact.html', data)


@login_required
@permission_required('accounts.add_contact',raise_exception=True)
def contact_add(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()

    return HttpResponseRedirect(reverse('contact_list'))


@login_required
@permission_required('accounts.edit_contact',raise_exception=True)
def contact_edit(request):

    if request.method == "POST":
        id = request.POST.get('id')
        contact = Contact.objects.get(id=id)
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm(instance=contact)

    return HttpResponseRedirect(reverse('contact_list'))


@login_required
@permission_required('accounts.del_contact',raise_exception=True)
def contact_del(request,id):

    if id:
        Contact.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('contact_list'))

