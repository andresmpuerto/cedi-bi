"""cedibi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

from account import views as login_view
from analytics import views as bi_view
from account.views import login, logout

API_TITLE = 'Documentación API CeDiBI'
API_DESCRIPTION = 'API para el Análisis de Datos de empresas con Centros de Distribución'
schema_view = get_swagger_view(title=API_TITLE)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/', include('rest_framework.urls', namespace='rest_framework')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, public=False)),
    ###
    # login
    url(r'^api/v1/login', login, name='login'),
    # logout
    url(r'^api/v1/logout', logout, name='logout'),

    url('^api/v1/users', login_view.UserViewSet),
    url(r'^docs/', schema_view),
    # --------------------
    # get user
    # get boards
    # create board
    # url('api/v1/roles/<int:pk>/boards', bi_view.BoardListCreate.as_view()),
    # get board
    # url('api/v1/boards/<int:pk>', bi_view.BoardObject.as_view()),
    # get comments and
    # create comments
    # url('api/v1/boards/<int:pk>/comments', bi_view.CommentListCreate.as_view()),

]
