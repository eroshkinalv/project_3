from django.urls import path
from mailout.apps import MailoutConfig
from mailout.views import ClientsCreateView, ClientsUpdateView, MessageCreateView, ClientsListView, \
    MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, ClientsDeleteView, ClientsDetailView, \
    MailoutListView, MailoutCreateView, MailoutDetailView, MailoutUpdateView, MailoutDeleteView, AttemptListView, \
    AttemptCreateView, AttemptDetailView, AttemptUpdateView, AttemptDeleteView, HomeCreateView, HomeTemplateView, \
    StatisticsTemplateView

app_name = MailoutConfig.name

urlpatterns = [
    path('home/', HomeTemplateView.as_view(), name='home'),
    path('home/create/', HomeCreateView.as_view(), name='home_create'),

    path('clients/', ClientsListView.as_view(), name='clients'),
    path('client/create/', ClientsCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/detail/', ClientsDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/update/', ClientsUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientsDeleteView.as_view(), name='client_delete'),

    path('message/', MessageListView.as_view(), name='message'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/detail/', MessageDetailView.as_view(), name='message_detail'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailout/', MailoutListView.as_view(), name='mailout'),
    path('mailout/create/', MailoutCreateView.as_view(), name='mailout_create'),
    path('mailout/<int:pk>/detail/', MailoutDetailView.as_view(), name='mailout_detail'),
    path('mailout/<int:pk>/update/', MailoutUpdateView.as_view(), name='mailout_update'),
    path('mailout/<int:pk>/delete/', MailoutDeleteView.as_view(), name='mailout_delete'),

    path('attempt/', AttemptListView.as_view(), name='attempt'),
    path('attempt/create/', AttemptCreateView.as_view(), name='attempt_create'),
    path('attempt/<int:pk>/detail/', AttemptDetailView.as_view(), name='attempt_detail'),
    path('attempt/<int:pk>/update/', AttemptUpdateView.as_view(), name='attempt_update'),
    path('attempt/<int:pk>/delete/', AttemptDeleteView.as_view(), name='attempt_delete'),

    path('statistics/', StatisticsTemplateView.as_view(), name='statistics'),

]
