# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from hostels.models import UserProfile


class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student / Traveler'),
        ('owner',   'Hostel Owner'),
    ]

    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)
    email      = forms.EmailField(required=True)
    phone      = forms.CharField(max_length=15, required=False)
    role       = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.HiddenInput())

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'username', 'email',
                  'phone', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Update the profile (auto-created by signal)
            user.profile.role  = self.cleaned_data['role']
            user.profile.phone = self.cleaned_data.get('phone', '')
            user.profile.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name  = forms.CharField(max_length=50)
    email      = forms.EmailField()

    class Meta:
        model  = UserProfile
        fields = ['phone', 'city', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial  = self.instance.user.last_name
            self.fields['email'].initial      = self.instance.user.email
        for field in self.fields.values():
            # Keep original attrs if any, and add form-control
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_class} form-control".strip()