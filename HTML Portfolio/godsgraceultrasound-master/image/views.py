from django.shortcuts import render,  get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from.forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from.models import Profile 
from .forms import User_form,  Edit_Profile_form 
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.db import transaction




# Create your views here.

class SignUpView(generic.CreateView):
    
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def myProfile(request, u_id):  
    my_detail = Profile.objects.all().filter(user_id=u_id)
    return render(request=request, template_name='userapp/user_profile.html', context={"myDetails":my_detail})


@login_required
@transaction.atomic
def editProfile(request, u_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=u_id)

        user_form = User_form(request.POST, instance=user)
        profile_form = Edit_Profile_form(request.POST or None, request.FILES or None, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            if profile_form.cleaned_data['staff']:
                
                user.is_staff = True
                user.save()
            else:
               
                user.is_staff = False
                user.save()
            messages.success(request, ('Your profile has been successfully updated!'))
            return myProfile(request, u_id)
        
        else:
            messages.error(request, ('Please correct the error below.'))
            return HttpResponsePermanentRedirect(reverse('edit_profile', args=(u_id,)))
        
    else:
        user = get_object_or_404(User, id=u_id)
        user_form = User_form(instance=user)
        profile_form = Edit_Profile_form(instance=user.profile)
        return render(request, 'userApp/edit_profile_form.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })
    

@login_required
def deactivate_account(request, _id):
    pass