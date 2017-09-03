#-*- coding: utf-8 -*-
from django import forms
from content.models import Content,Type,Images
from django.contrib.auth.models import Group
class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ('name',)

class ContentForm(forms.ModelForm):

    class Meta:
        model = Content
        exclude = ('author',)
        description = '请按如下文本格式编写:\n1.整理知识，学习笔记\n2.发布日记，杂文，所见所想\n3.撰写发布技术文稿（代码支持)\n4.撰写发布学术论文（LaTeX 公式支持'

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'level' : forms.Select(attrs={'class':'form-control'}),
            'type' : forms.Select(attrs={'class':'form-control'}),
            'project' : forms.Select(attrs={'class':'form-control'}),
            'effect' : forms.Textarea(attrs={'class':'form-control','rows': '7','placeholder':description}),
            'reasons' : forms.Textarea(attrs={'class':'form-control','rows': '7','placeholder': description}),
            'solution' : forms.Textarea(attrs={'class':'form-control','rows': '10','placeholder': description}),
            'improve' : forms.Select(attrs={'class':'form-control'}),
            'status' : forms.Select(attrs={'class':'form-control'}),
            'content' : forms.Textarea(),
        }


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
        }



class ImagesUploadForm(forms.ModelForm):
    
    class  Meta:
        model = Images
        fields = '__all__'

