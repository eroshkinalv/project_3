from django.forms import ModelForm, BooleanField
from django.core.exceptions import ValidationError
from mailout.models import Clients, Message, Mailout


class ClientsForm(ModelForm):
    class Meta:
        model = Clients
        exclude = ('owner', )

    def __init__(self, *args, **kwargs):

        super(ClientsForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите Email',
        })

        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите ФИО',
        })

        self.fields['notes'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Комментарий',
        })


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ('created_at', 'owner')

    def __init__(self, *args, **kwargs):

        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Тема',
        })

        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Сообщение',
        })


class MailoutForm(ModelForm):
    class Meta:
        model = Mailout
        fields = ('clients', 'message', 'status')

    def __init__(self, *args, **kwargs):

        super(MailoutForm, self).__init__(*args, **kwargs)

        self.fields['clients'].widget.attrs.update({
            'class': 'form-select',
            'multiple aria - label': "multiple select example",
            'placeholder': 'Получатели',
        })
        self.fields['clients'].label = 'Получатели рассылки'

        self.fields['message'].widget.attrs.update({
            'class': 'form-select',
            'placeholder': 'Сообщение',
        })
        self.fields['message'].label = 'Сообщение'

        self.fields['status'].widget.attrs.update({
            'class': 'form-select',
            'placeholder': 'Статус рассылки',
        })




class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-label'
            field.widget.attrs['class'] = 'form-control'
