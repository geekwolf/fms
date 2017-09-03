#-*- coding: utf-8 -*-
'''
	Author: Geekwolf
	Blog: http://www.simlinux.com
'''
from django.shortcuts import render,render_to_response,reverse
from django.http import HttpResponse,HttpResponseRedirect
from commons.paginator import paginator
from accounts.models import User
from django.db.models import Q

def user_search(request):

    data = {}
    search = request.GET.get("search")
    user = User.objects.filter(Q(group__name__icontains=search) | Q(username__icontains=search) | Q(email__icontains=search) | Q(fullname__icontains=search) | Q(mobile__icontains=search))
    data = paginator(request, user)
    return render_to_response('accounts/user/user_table.html',data)