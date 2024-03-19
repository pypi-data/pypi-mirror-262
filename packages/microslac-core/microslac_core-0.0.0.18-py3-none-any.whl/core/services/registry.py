from django.conf import settings
from core.services import ProxyService


class AuthService(ProxyService):
    _host = settings.MICROSERVICE.AUTH_HOST
    _port = settings.MICROSERVICE.AUTH_PORT


class TeamService(ProxyService):
    _host = settings.MICROSERVICE.TEAMS_HOST
    _port = settings.MICROSERVICE.TEAMS_PORT


class UserService(ProxyService):
    _host = settings.MICROSERVICE.USERS_HOST
    _port = settings.MICROSERVICE.USERS_PORT


class ConversationService(ProxyService):
    _host = settings.MICROSERVICE.CONVERSATIONS_HOST
    _port = settings.MICROSERVICE.CONVERSATIONS_PORT
