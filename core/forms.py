from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserProfile

# Sign-up form
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        if password: 
            cleaned_data["password"] = password.strip()
        else: 
            self.add_error("password", "Password is required.")
            return cleaned_data
        confirm_password = cleaned_data.get("confirm_password")
        
        # Debugging line
        print(f"Password: {password}, Confirm Password: {confirm_password}")
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data


# Login form
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'id': 'login_username'})
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'login_password'})
        )
    
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        # Add validation if needed (e.g., file size or type validation)
        return picture