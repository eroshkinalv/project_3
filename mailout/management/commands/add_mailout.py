from django.core.management.base import BaseCommand
from mailout.models import Mailout, Message, Clients


class Command(BaseCommand):
    help = 'Добавьте новую рассылку'

    def handle(self, *args, **kwargs):

        Mailout.objects.all()
        Message.objects.all()
        Clients.objects.all()

        try:

            clients = Clients.objects.filter(email='person_1@example.com')

            mailout = Mailout.objects.create(message_id=2, status='Запущена')

            mailout.clients.set(clients)

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Mailing failed: {e}'))

        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully mailed: {mailout.message}'))
