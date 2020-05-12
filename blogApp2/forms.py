from django import forms
from blogApp2.models import blogpost,profile
from django.contrib.auth.models import User
"""class formModel(forms.ModelForm):
    first_name = forms.CharField()
    username = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget =forms.PasswordInput)
    
    
    class Meta:

        model = User
        fields= ('username','FIRST NAME','LAST NAME')"""
class saveblog(forms.ModelForm):
    class Meta:
        model = blogpost
        fields = ('title','content','pic')
class updateblog(forms.ModelForm):
    class Meta:
        model = blogpost
        fields = ('title','content','pic')
        
class profileUpdate(forms.ModelForm):
    class Meta:
        model = profile
        fields = '__all__'
