from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, GuestForm
from  django.utils.http import is_safe_url
from .models import GuestEmail
from django.contrib.auth.models import User
from django.conf import settings
from addresses.models import Address

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() 
            form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are able now to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form' : form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST , instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES , instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
           u_form.save()
           p_form.save()
           messages.success(
               request, f'Your account has been updated!')
           return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'accounts/profile.html', context)


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context ={
        "form": form
    }
    next_           = request.GET.get('next')
    next_post       = request.POST.get('next')
    redirect_path   = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id']= new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return render(request, "accounts/register.html", context)

def address_get(request):
    User = settings.AUTH_USER_MODEL
    instance = request.user.username
    user = User.objects.get(instance)
    adrs = Address.objects.filter(user=user)
    print ("this is the address",adrs)
    
    return render(request, 'accounts/profile.html', {'adrs': adrs})


