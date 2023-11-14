from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    return render(request, 'base/index.html')

# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, request=None, *args, **kwargs):
#         super().__init__(request=None, *args, **kwargs)
#         self.fields['username'].label = 'a cool label'
#         self.fields['password'].label = 'another cool label'
