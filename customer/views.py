from django.shortcuts import redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import  logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import RegistrationForm

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


# class UserLoginView(LoginView):
#     template_name = 'login.html'
#     def get_success_url(self):
#         return reverse_lazy('home')

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