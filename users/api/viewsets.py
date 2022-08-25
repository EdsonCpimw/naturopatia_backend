from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from config.mixins import ActionBaseSerializerMixin
from users.models import User
from users.permissions import AdministradorPermissions, UsuarioPermissions, EditPermissions
from users.api.serializers import CadastroUserSerializer, ObtainTokenSerializer, ObtainTokenRefreshSerializer, \
    UserPostSerializer, CadastroPartialUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.db.models.functions import Concat


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPostSerializer
    permission_classe = IsAuthenticated


class UserCadastroViewSet(ActionBaseSerializerMixin, ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
        EditPermissions,
    )
    # http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options',]

    serializer_classes = {
        'create': CadastroUserSerializer,
        'default': CadastroPartialUserSerializer,
        # 'list': CadastroPartialUserSerializer,
        # 'retrieve': CadastroPartialUserSerializer,
        # 'update': CadastroPartialUserSerializer,
    }

        # return super().list(request, *args, **kwargs)
    # Override a mensagem de ao deletar usuário, foi necessario alterar o status
    # pois status 204 não possui retorno.
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(data='Usuário deletado com sucesso.', status=status.HTTP_200_OK)
    #
    # def perform_destroy(self, instance):
    #     instance.delete()


class ObtainTokenViewSet(TokenObtainPairView):
    serializer_class = ObtainTokenSerializer


class ObtainTokenRefreshViewSet(TokenRefreshView):
    serializer_class = ObtainTokenRefreshSerializer
