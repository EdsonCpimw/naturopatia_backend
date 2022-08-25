# Generated by Django 4.0.4 on 2022-04-11 18:28

from django.db import migrations, models
import users.managers
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('nome', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('sobrenome', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('sobre', models.TextField(blank=True, null=True, verbose_name='sobre')),
                ('is_active', models.BooleanField(db_column='Ativo', default=True, verbose_name='active')),
                ('tipo_usuario', models.IntegerField(choices=[(1, 'Administrador'), (2, 'Usuario'), (3, 'ANONIMO')], default=2)),
                ('last_login', models.DateTimeField(auto_now_add=True, db_column='ultimo_login', verbose_name='last login')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to=users.models.upload_image_user)),
                ('is_admin', models.BooleanField(db_column='Admin_Administracao', default=False, help_text='Permite que o usuario possa fazer login na pagina de Administração.', verbose_name='admin status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'permissions': [('GetAllUsers', 'Visualizar todos Usuarios'), ('GetById', 'Visualizar usuario por id')],
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
    ]
