from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from analytics.views import BoardListCreate, BoardObject, CommentListCreate, MainBoardMix
from core.views import OccupationBoardObject
from account.views import login, logout, UserList

from oauth2_provider.models import AccessToken, Application, Grant, RefreshToken

API_TITLE = 'Documentación API CeDiBI'
API_DESCRIPTION = 'API para el Análisis de Datos de empresas con Centros de Distribución'
schema_view = get_swagger_view(title=API_TITLE)

admin.site.site_title = 'CeDi BI'
admin.site.site_header = 'Administración del CeDi BI'
# admin.site.unregister(AccessToken)
# admin.site.unregister(Grant)
# admin.site.unregister(RefreshToken)
# admin.site.unregister(Application)

urlpatterns = [
    url('', admin.site.urls),
    url(r'^api/v1/login', login, name='login'),
    # logout
    url(r'^api/v1/logout', logout, name='logout'),
    path('api/v1/users/<int:pk>', UserList.as_view(), name='user-detail'),
    path('api/v1/roles/<int:pk>/boards', BoardListCreate.as_view(), name='boards'),
    path('api/v1/boards/<int:pk>', BoardObject.as_view(), name='board'),
    path('api/v1/boards/<int:pk>/comments', CommentListCreate.as_view()),
    # #####
    path('api/v1/roles/<int:pk>/dashboard', MainBoardMix.as_view()),
    path('api/v1/boards/occupation/<int:pk>', OccupationBoardObject.as_view()),
    # ######
    path('api/v1', include('rest_framework.urls', namespace='rest_framework')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, public=False)),
    url(r'^docs/', schema_view),
]