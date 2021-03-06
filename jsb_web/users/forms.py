from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms as django_forms

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

class SignUpForm(django_forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','name','username','password','bu_name','level_name']

        labels = {
            'email':'이멩일 주소',
            'name':'성명',
            'username':'사용자 이름',
            'password':'비밀번호',
            'bu_name':'부서명',
            'level_name':'직책',
        }

        widgets = {
            'email':django_forms.TextInput(attrs={'placeholder':'이메일 주소'}),
            'name':django_forms.TextInput(attrs={'placeholder':'성명'}),
            'username':django_forms.TextInput(attrs={'placeholder':'비밀번호'}),
            'password':django_forms.PasswordInput(),
            'bu_name':django_forms.TextInput(attrs={'placeholder':'부서명'}),
            'level_name':django_forms.TextInput(attrs={'placeholder':'직책'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

