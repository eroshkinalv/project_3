from django.contrib.auth.forms import UserCreationForm
from mailout.forms import StyleFormsMixin
from users.models import User


class UserRegisterForm(StyleFormsMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):

        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Придумайте пароль',
        })

        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].help_text = 'Пароль должен состоять не менее, чем из 8 символов. Пароль не должен включать в себя легко вычисляемые сочетания символов.'

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
        })

        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].help_text = ''

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите адрес электронной почты',
        })
