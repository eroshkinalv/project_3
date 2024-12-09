from django.core.management.base import BaseCommand
from mailout.models import Clients


class Command(BaseCommand):
    help = 'Добавьте нового получателя'

    def handle(self, *args, **kwargs):
        Clients.objects.all().delete()

        mailout, _ = Clients.objects.get_or_create(name='Email', description='ФИО')

        clients = [
            {'email': 'person@example.com', 'full_name': 'Фамилия Имя Отчество', 'notes': 'Песональная рассылка',},
        ]

        for client_data in clients:
            mailout, created = Clients.objects.get_or_create(**client_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added product: {clients.name}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Client already exists: {clients.name}'))
