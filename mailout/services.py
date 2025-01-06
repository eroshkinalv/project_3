from mailout.models import Clients, Mailout


def get_clients_for_mailout(mailout_id):
    clients_id = Mailout.clients.filter(mailout_id=mailout_id)
    clients = {}
    clients['emails'] = Clients.email.filter(id=clients_id)
    return clients

