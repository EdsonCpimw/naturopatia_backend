"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import djoser
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)


from posts.api.viewsets import *
from users.api.viewsets import UserViewSet, ObtainTokenViewSet, ObtainTokenRefreshViewSet, UserCadastroViewSet

router = routers.DefaultRouter()

router.register(r'post', PostsViewSet)
router.register(r'categoria', CategoriaViewSet)
router.register(r'postRecent', PostRecentViewSet)
router.register(r'alimentacao', PostAlimentacao)
router.register(r'terapia', PostTerapia)
router.register(r'banner', BannerViewSet)
router.register(r'users', UserViewSet)
# Admin
router.register(r'user', UserCadastroViewSet)
router.register(r'categoriaAdm', CategoriaAdminViewSet)
router.register(r'bannerAdm', BannerAdminViewSet)
router.register(r'postsAdm', PostsAdminViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('naturopatiaadm/', admin.site.urls),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/token/', ObtainTokenViewSet.as_view()),
    path('auth/refresh/', ObtainTokenRefreshViewSet.as_view()),
    # path('auth/token/', TokenObtainPairView.as_view()),
    # path('auth/refresh/', TokenRefreshView.as_view()),
    # path('auth/verify/', TokenVerifyView.as_view()),
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

urlpatterns += [
    path('api/', include('djoser.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

# altera nome tela de login
admin.site.site_header = 'Nutri-Natural'
# altera o titulo do site
admin.site.index_title = 'Administração do Sistema'
# itera ao nome na aba administração
admin.site.site_title = 'Seja bem vindo ao Nutri-Natural'
