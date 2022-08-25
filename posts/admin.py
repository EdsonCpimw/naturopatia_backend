from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import forms
from django.utils.translation import gettext_lazy as _
from .models import Categoria, Posts, Banners
from django.contrib import messages
from django.db import transaction


# Register your models here.

@admin.register(Posts)
class PostesAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'id', 'data_cadastro', 'ativo', 'data_postagem', 'tem_texto')
    # raw_id_fields = ('user_cadastro', 'user_postagem')
    autocomplete_fields = ('user_cadastro', 'user_postagem')
    list_filter = ('titulo',)
    # readonly_fields = ['data_cadastro', 'last_login']
    fieldsets = (
        ('Campos Obrigatórios',
         {'fields': ('titulo', 'imagem', 'categoria', 'data_cadastro', 'user_cadastro', 'texto',)}),
        (_('Campos de Postagem'), {
         'fields': ('ativo', 'user_postagem', 'data_postagem',)}),
    )
    search_fields = ('id', 'titulo',)
    ordering = ('id',)

    def tem_texto(self, obj):
        if obj.texto:
            return 'Sim'
        else:
            return 'Não'

    tem_texto.short_description = 'Possui Texto'

    def save_model(self, request, obj, form, change):
        try:
            if obj.ativo is not False and obj.user_postagem is not None and obj.data_postagem is not None:
                with transaction.atomic():
                    obj.save()
                super().save_model(request, obj, form, change)
            elif obj.ativo is False and obj.user_postagem is None and obj.data_postagem is None:
                with transaction.atomic():
                    obj.save()
                super().save_model(request, obj, form, change)
            else:
                return messages.add_message(
                    request, messages.ERROR,
                    u'Error ao Salvar, só é permitido salvar com todos ou nenhum dos Campos de Postagem preenchido',
                    fail_silently=True)
        except Exception as ex:
            messages.add_message(
                request, messages.ERROR,
                u'Ocorreu um erro ao salvar o Post. Erro: %s' % ex,
                fail_silently=True)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome_categoria', 'id')
    list_filter = ('nome_categoria',)
    fieldsets = (
        ('Campos Obrigatórios', {'fields': ('nome_categoria',)}),
    )
    search_fields = ('id', 'nome_categoria',)
    ordering = ('id',)


@admin.register(Banners)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'imagem', 'ativo', 'data_postagem')
    list_filter = ('imagem',)
    fieldsets = (
        ('Campos Obrigatórios', {'fields': ('imagem', 'data_postagem')}),
        (_('Campos não Obrigatórios'), {
         'fields': ('ativo', 'titulo', 'texto', 'url_post',)}),
    )
    search_fields = ('id', 'imagem',)
    ordering = ('id',)
