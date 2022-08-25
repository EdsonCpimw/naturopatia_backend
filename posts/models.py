from curses.ascii import NUL
from distutils.command.upload import upload
from pyexpat import model
from statistics import mode
from django.db import models
from users.models import User

# Create your models here.


class Categoria(models.Model):

    TIPOCATEGORIA = (
        ('Alimentação', 'Alimentação'),
        ('Terapia', 'Terapia')
    )
    nome_categoria = models.CharField(max_length=100, choices=TIPOCATEGORIA,)

    def __str__(self):
        return '{}, {}'.format(self.id, self.nome_categoria)

    def __repr__(self) -> str:
        return '{}, {}'.format(self.id, self.nome_categoria)

    class Meta:
        db_table = 'tb_categoria'
        ordering = ('id',)


def upload_image_posts(instance, filename):
    # return "Posts/%s/%s" % (instance.data_cadastro, filename)
    return "Posts/%s" % (filename)
    # return filename


def get_deleted_user_instance(obj):
    return User.objects.get(id=(obj))


user_postagem_novo = 1


class Posts(models.Model):
    titulo = models.CharField(max_length=150)
    imagem = models.ImageField(upload_to=upload_image_posts, blank=True, null=True)
    data_cadastro = models.DateField()
    ativo = models.BooleanField(default=False)
    data_postagem = models.DateField(null=True, blank=True)
    texto = models.TextField(verbose_name='texto')

    user_cadastro = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_cadastro')

    user_postagem = models.ForeignKey(
        User, on_delete=models.SET(user_postagem_novo),  blank=True, null=True, related_name='user_postagem')

    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name='categoria')

    # def save_user_postagem(self, *args, **kwargs):
    #     if not self.user_postagem:
    #         self.user_postagem = self.user_cadastro
    #     super(Posts, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return '{}, {}'.format(self.titulo, self.data_cadastro)

    def __repr__(self) -> str:
        return '{}, {}'.format(self.titulo, self.data_cadastro)

    class Meta:
        db_table = 'tb_post'
        ordering = ('id',)


def upload_image_banners(instance, filename):
    # return "banner/%s/%s" % (instance.data_postagem, filename)
    return "banner/%s" % (filename)
    # return f"{instance.id}-{filename}"


class Banners(models.Model):
    imagem = models.ImageField(upload_to=upload_image_banners, null=True, blank=True)
    ativo = models.BooleanField(default=False)
    data_postagem = models.DateField()
    titulo = models.CharField(max_length=50, null=True, blank=True)
    texto = models.TextField(verbose_name='texto', null=True, blank=True)
    url_post = models.CharField(
        max_length=150, verbose_name='url', null=True, blank=True)

    def __str__(self) -> str:
        return '{}, {}'.format(self.id, self.imagem)

    def __repr__(self) -> str:
        return '{}, {}'.format(self.id, self.imagem)

    class Meta:
        db_table = 'tb_banner'
        ordering = ('id',)
