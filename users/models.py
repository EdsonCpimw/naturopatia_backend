from __future__ import unicode_literals
from distutils.command.upload import upload

from django.contrib.auth.models import AbstractBaseUser, Permission
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions

from .managers import UserManager


def upload_image_user(instance, filename):
    return "users/%s/%s" % (instance.data_cadastro, filename)
    # return f"{instance.id}-{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    ADMINISTRADOR = 1
    USUARIO = 2
    ANONIMO = 3

    TIPOUSUARIO = (
        (ADMINISTRADOR, 'Administrador'),
        (USUARIO, 'Usuario'),
        (ANONIMO,  'ANONIMO')
    )
    email = models.EmailField(_('email address'), unique=True)
    nome = models.CharField(_('first name'), max_length=150, blank=True)
    sobrenome = models.CharField(_('last name'), max_length=150, blank=True)
    password = models.CharField(_("password"), max_length=128)
    data_cadastro = models.DateTimeField(_('date joined'), auto_now_add=True)
    sobre = models.TextField(verbose_name='sobre', null=True, blank=True)
    is_active = models.BooleanField(
        _('active'), default=True, db_column='Ativo')
    tipo_usuario = models.IntegerField(choices=TIPOUSUARIO, default=2)
    is_staff = models.BooleanField(
        default=False, db_column='Acesso_administracao')
    last_login = models.DateTimeField(
        _('last login'), auto_now_add=True, db_column='ultimo_login')
    imagem = models.ImageField(
        upload_to=upload_image_user, null=True, blank=True)

    # Remover este campo
    is_admin = models.BooleanField(
        _('admin status'),
        default=False,
        db_column='Admin_Administracao',
        help_text=_(
            'Permite que o usuario possa fazer login na pagina de Administração.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = [
            ('GetAllUsers', 'Visualizar todos Usuarios'),
            ('GetById', 'Visualizar usuario por id'),
        ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.nome, self.sobrenome)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.nome

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
