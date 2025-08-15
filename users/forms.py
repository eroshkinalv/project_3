from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField

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
        self.fields['password1'].help_text = ('Пароль должен состоять не менее, чем из 8 символов. '
                                              'Пароль не должен включать в себя легко вычисляемые сочетания символов.')

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


class UserUpdateForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('image', 'phone', 'country')
        exclude = ('password',)

    def __init__(self, *args, **kwargs):

        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['image'].widget.attrs.update({
            'placeholder': '',
        })

        self.fields['image'].help_text = ''
        self.fields['image'].label = 'Your name'
        self.fields['image'].localized_field = 'Your name'
        self.fields['image'].fieldset = 'Your name'
        self.fields['image'].initial = "Your name"

        self.fields['phone'].widget.attrs.update({
            'placeholder': 'Укажите телефон',
        })

        self.fields['country'].widget.attrs.update({
            'placeholder': 'Укажите страну',
        })

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_image(self):

        image = self.cleaned_data.get('image')
        image_size = image.size
        image_name = image.name
        max_size = 5 * 1024 * 1024

        if image_size > max_size:
            raise ValidationError('Размер файла не должен превышать 5МБ')

        elif not (image_name.endswith('png') or image_name.endswith('jpg')):
            raise ValidationError('Формат файла должен быть PNG или JPEG')

        return image


class ManagerForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('image', 'phone', 'country', 'is_blocked',)
        exclude = ('password', 'image', 'phone', 'country')

    def __init__(self, *args, **kwargs):

        super(ManagerForm, self).__init__(*args, **kwargs)

        self.fields['is_blocked'].widget.attrs.update({
            'class': 'form-label',
            'placeholder': 'Заблокировать/разблокировать',
        })


class PasswordUpdateForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):

        super(PasswordUpdateForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите адрес электронной почты',
        })


class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-label'
            field.widget.attrs['class'] = 'form-control'
