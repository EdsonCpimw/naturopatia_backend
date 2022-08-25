from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from datetime import timedelta, datetime
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class CadastroUserSerializer(serializers.ModelSerializer):
    #nome_completo = serializers.CharField(source='get_full_name')
    password = serializers.CharField()
    password_confirm = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'email', 'nome', 'sobrenome', 'imagem',
                  'tipo_usuario', 'sobre', 'password', 'password_confirm', 'is_active', ]
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, **kwargs):
        usuario = User(
            email=self.validated_data['email'],
            nome=self.validated_data['nome'],
            sobrenome=self.validated_data['sobrenome'],
            imagem=self.validated_data['imagem'],
            # data_cadastro=self.validated_data['data_cadastro'],
            tipo_usuario=self.validated_data['tipo_usuario'],
            sobre=self.validated_data['sobre'],
            is_active=self.validated_data['is_active'],
        )
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']

        if password != password_confirm:
            raise serializers.ValidationError({'password': 'As senhas não conferem!'})
        usuario.set_password(password)
        usuario.save()
        return usuario



class CadastroPartialUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'nome', 'sobrenome', 'data_cadastro', 'tipo_usuario', 'imagem', 'sobre', 'is_active', ]


class UserPostSerializer(serializers.ModelSerializer):
    nome_completo = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ['id', 'nome_completo', 'imagem', 'email', 'sobre', 'status',]

    def get_nome_completo(self, obj):
        return '{} {}'.format(obj.nome, obj.sobrenome)

    def get_status(self, obj):
        if obj.is_active == True:
            return 'Ativo'
        else:
            return 'Inativo'


class ObtainTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        # data.pop('refresh', None) # Remover Refresh token
        data['access'] = str(refresh.access_token)

        #Campos adicionais
        data['tipo_usuario'] = self.user.tipo_usuario
        data['nome_usuario'] = self.user.nome
        data['id'] = self.user.id
        data['access_token_lifetime'] = str(refresh.access_token.lifetime)
        data['refresh_token_lifetime'] = str(refresh.lifetime)
        data['access_token_expiry'] = str(datetime.now() + refresh.access_token.lifetime)
        data['refresh_token_expiry'] = str(datetime.now() + refresh.lifetime)
        return data


class ObtainTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])

        data['access'] = str(refresh.access_token)
        data['access_token_lifetime'] = str(datetime.now() + refresh.access_token.lifetime)
        data['refresh_token_lifetime'] = str(datetime.now() + refresh.lifetime)

        return data