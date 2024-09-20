from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import  logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')  # Redirect to login on successful registration

    def form_valid(self, form):
        form.save()  # Save the valid form (create the user)
        messages.success(self.request, 'Account created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)



class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')
    
def user_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('home'))


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html')



@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)  # Fetch the user's profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile view after saving
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})
