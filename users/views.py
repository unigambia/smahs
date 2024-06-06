from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from apps.corecode.forms import RegistrationForm, UserUpdateForm, UserForm
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

# @user_passes_test(lambda u: u.is_superuser or u.is_staff)
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "corecode/user_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserForm()
        
        return context


class UserCreateView(UserPassesTestMixin, SuccessMessageMixin ,LoginRequiredMixin, CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("users")
    success_message = "New User successfully added"

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        # Ensure that the password and confirm_password fields match
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        if password != confirm_password:
            messages.error(self.request, "Passwords do not match.")
            return self.form_invalid(form)
        
        obj = form.save(commit=False)
        obj.set_password(password)
        obj.is_superuser = True
        obj.save()
        return super().form_valid(form)



class UserUpdateView(UserPassesTestMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm 
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("users")
    success_message = "User successfully updated."

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserUpdateForm(instance=self.object)
        return context

    def form_valid(self, form):
        password = form.cleaned_data.get('password', None)
        confirm_password = form.cleaned_data.get('confirm_password', None)

        if password and confirm_password:
            if password != confirm_password:
                messages.error(self.request, "Passwords do not match.")
                return self.form_invalid(form)

        obj = form.save(commit=False)
        obj.set_password(password)
        obj.save()

        return super().form_valid(form)


class UserDeleteView(UserPassesTestMixin, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "User  has been deleted with all its attached content"

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj)
        messages.success(self.request, self.success_message.format(obj.username))
        return super(UserDeleteView, self).delete(request, *args, **kwargs)
 

 