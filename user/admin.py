from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import CustomUser

# Register your models here.

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)

	class Meta:
		model = CustomUser
		fields = ('email', 'business_name')

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password1")
		if password1 and password2 and password1 != password2:
			raise ValidationError("Passwords do not match")
		return password2

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField

	class Meta:
		model = CustomUser
		fields = (
			'email',
			'username',
			'business_name',
			'first_name',
			'last_name',
			'is_active',
			'is_admin',
		)

	def clean_password(self):
		return self.initial["password"]

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = [ 'email', 'username', 'business_name', 'is_admin' ]
	list_filter = [ 'is_admin' ]

	fieldsets = (
		(None, { 'fields': ('email', 'password')} ),
			('Personal Info', { 'fields': ('username', 'business_name',)} ),
			('Permissions', { 'fields': ('is_admin',)} ),
		)

	add_fieldsets = (
		(None, { 
			'classes': ('wide',),
			'fields': ('email', 'username', 'password1', 'password2'),
			}),
		)

	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()



admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)