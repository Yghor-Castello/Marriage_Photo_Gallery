from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomUserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'user_type',
            'password1',
            'password2',
        ]
        labels = {'email': 'E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = [
            'name',
            'email',
        ]
        labels = {'email': 'E-mail'}
