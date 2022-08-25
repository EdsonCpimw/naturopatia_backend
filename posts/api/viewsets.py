from cgitb import lookup
from dataclasses import fields
from re import search
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from config.mixins import ActionBaseSerializerMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from posts.models import Posts, Categoria, Banners
from posts.api.serializers import PostSerializer, CategoriaSerializer, PostRecentSerializer, BannerSerializer, \
    BannerAdmSerializer, PotsAdmSerializers, PartialPostsAdminSerializers
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.filters import CharFilter, NumberFilter

from users.permissions import AdministradorPermissions, UsuarioPermissions


class PaginationWithPageSize(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100


class FilterPosts(FilterSet):
    titulo = CharFilter(field_name='titulo', lookup_expr='icontains')
    # categoria = CharFilter(field_name='categoria', lookup_expr='icontains')


class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    http_method_names = ['get', 'head', 'options', ]


class CategoriaAdminViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (
        IsAuthenticated,
        AdministradorPermissions,
    )
    http_method_names = ['get', 'delete', 'post', 'head', 'options', ]


class PostsViewSet(ModelViewSet):
    queryset = Posts.objects.filter(ativo=True).order_by('-data_postagem')
    serializer_class = PostSerializer
    pagination_class = PaginationWithPageSize
    filter_class = FilterPosts
    search_fields = ['titulo']
    http_method_names = ['get', 'head', 'options', ]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PostAlimentacao(ModelViewSet):
    queryset = Posts.objects.filter(
        ativo=True, categoria__nome_categoria='Alimentação')
    serializer_class = PostSerializer
    pagination_class = PaginationWithPageSize
    filter_class = FilterPosts
    search_fields = ['titulo']
    http_method_names = ['get', 'head', 'options', ]


class PostTerapia(ModelViewSet):
    queryset = Posts.objects.filter(
        ativo=True, categoria__nome_categoria='Terapia')
    serializer_class = PostSerializer
    pagination_class = PaginationWithPageSize
    filter_class = FilterPosts
    search_fields = ['titulo']


class PostRecentViewSet(ModelViewSet):
    queryset = Posts.objects.order_by('-data_postagem')[:4]
    serializer_class = PostRecentSerializer
    http_method_names = ['get', 'head', 'options', ]


class BannerViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Banners.objects.filter(ativo=True)
    serializer_class = BannerSerializer


class BannerAdminViewSet(ModelViewSet):
    queryset = Banners.objects.all()
    serializer_class = BannerAdmSerializer
    permission_classes = (
        IsAuthenticated,
        UsuarioPermissions,
    )


class PostsAdminViewSet(ActionBaseSerializerMixin, ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PotsAdmSerializers
    permission_classes = (
        IsAuthenticated,
        UsuarioPermissions,
    )

    serializer_classes = {
        'list': PartialPostsAdminSerializers,
        'default': PotsAdmSerializers,
    }