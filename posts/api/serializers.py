import json
from dataclasses import fields
from operator import contains
from pyexpat import model
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from posts.models import Posts, Categoria, Banners
from users.api.serializers import UserPostSerializer
from users.models import User


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = ['id', 'nome_categoria']


class CategoriaPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = ['nome_categoria']


class PostSerializer(serializers.ModelSerializer):
    user_postagem = UserPostSerializer()
    categoria = CategoriaPostSerializer()
    user_cadastro = UserPostSerializer()

    class Meta:
        model = Posts
        fields = ['id', 'titulo', 'imagem', 'user_postagem',
                  'data_postagem', 'texto', 'categoria', 'user_cadastro']



class PostRecentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ['id', 'titulo', 'imagem', 'data_postagem']


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banners
        fields = ['id', 'imagem', 'data_postagem', 'titulo', 'texto', 'url_post']


class BannerAdmSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Banners
        fields = ['id', 'imagem', 'data_postagem', 'titulo', 'ativo', 'status', 'texto', 'url_post', ]


    def get_status(self, obj):
        if obj.ativo == True:
            return 'Ativo'
        else:
            return 'Inativo'

class PartialPostsAdminSerializers(serializers.ModelSerializer):
     status = serializers.SerializerMethodField()
     categoria = CategoriaSerializer()

     class Meta:
         model = Posts
         fields = ['id', 'titulo', 'status', 'data_cadastro',
                  'data_postagem', 'categoria']

     def get_status(self, obj):
         if obj.ativo == True:
             return 'Ativo'
         else:
             return 'Inativo'

class PotsAdmSerializers(WritableNestedModelSerializer):
    status = serializers.SerializerMethodField()
    user_postagem = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    user_cadastro = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Posts
        # exclude = ('titulo',)
        fields = ['id', 'titulo', 'ativo', 'status', 'data_cadastro', 'imagem',
                  'data_postagem', 'texto', 'categoria', 'user_cadastro', 'user_postagem']
        depth = 1

    def get_status(self, obj):
        if obj.ativo == True:
            return 'Ativo'
        else:
            return 'Inativo'