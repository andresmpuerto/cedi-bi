from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from django.db.models import Sum
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from account.models import Rol
from analytics.dataframe.BoardExpirations import BoardExpiration
from analytics.dataframe.DashboardCedi import MakeDataFrameCedi
from analytics.dataframe.DashboardBusiness import MakeDataFrameBusiness
from analytics.models import Board, Comment, DashboardCedi, DashboardBusiness
from analytics.serializers import BoardSerializer, CommentSerializer, PostCommentSerializer, BoardMixSerializer


class BoardListCreate(ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read']

    def get_queryset(self):
        values = Board.objects.filter(rol=self.kwargs["pk"])
        return get_object_or_404(values)


class BoardObject(RetrieveAPIView):
    serializer_class = BoardSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read']

    def get_queryset(self):
        values = Board.objects.filter(pk=self.kwargs["pk"])
        return get_object_or_404(values)

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serialize = BoardSerializer(instance)
        graphs = {}
        if self.kwargs['pk'] is 2:  # vencimientos
            graphs = Boards().expired_products()

        return response_data(message='Board Vencimiento', extra_data={'graphs': graphs, 'board': serialize.data})


class CommentListCreate(ListCreateAPIView):
    parser_classes = [JSONParser]
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read', 'write']

    def get_queryset(self):
        values = Comment.objects.filter(board=self.kwargs["pk"]).order_by('-created_at')
        return values

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = CommentSerializer(instance, many=True)
        data = serializer.data
        return response_data(message='success comments', extra_data={'comments': data})

    def post(self, request, format=None, **kwargs):
        posts = PostCommentSerializer(data=request.data, context={'request': request})
        if posts.is_valid():
            posts.save()
            return response_data("success", extra_data=None)
        else:
            return response_data("fail", status=400, extra_data=None)


def response_data(message, status=200, extra_data=None):
    data = {'coderesponse': 0, 'message': message, 'date': now().strftime("%Y/%m/%d %H:%M:%S")}
    if extra_data:
        data.update(extra_data)
    return Response(status=status, data=data)


class OcupationBoard(ListAPIView):
    parser_classes = [JSONParser]
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read']

    def get_queryset(self):
        values = DashboardCedi.objects.values("categoria_id", "nom_categoria").annotate(Sum('estibas'))
        return values

    def list(self, request, *args, **kwargs):
        pass


class MainBoardMix(ListAPIView):
    parser_classes = [JSONParser]
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read']

    def get_queryset(self):
        if self.kwargs['pk'] == 20:
            values = DashboardCedi.objects \
                .filter(estibas__gt=0) \
                .values("categoria_id", "nom_categoria", "estibas", "cod_bodega", "nom_bodega")
        else:
            values = DashboardBusiness.objects \
                .filter(estibas__gt=0) \
                .values("categoria_id", "nom_categoria", "estibas", "cod_bodega", "nom_bodega", "sku_transito",
                        "sku_no_apta")

        return values

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = BoardMixSerializer(instance, many=True, )
        cod = self.kwargs['pk']
        # roles = Rol.objects.all()
        if cod == 20:
            records = MakeDataFrameCedi(list(instance))
        else:
            records = MakeDataFrameBusiness(list(instance))

        data = dict(
            storage=records.frame_storage_cedi(),
            mix=records.frame_internal_external(),
            internal=records.frame_total_internal(),
            external=records.frame_total_external(),
            status=records.frame_total_status()
        )

        return response_data(message='success board mix', extra_data={'data': data})


class Boards:

    def get_queryset(self):
        return DashboardCedi.objects \
            .filter(estibas__gt=0) \
            .values('nom_bodega',
                    'nom_categoria',
                    "nom_negocio",
                    'nom_linea',
                    'nom_marca',
                    'nom_articulo',
                    'estibas',
                    'dias_vencimiento')

    def expired_products(self):
        instance = self.get_queryset()
        cedi = BoardExpiration()
        q = list(instance)

        q2 = DashboardCedi.objects \
            .filter(estibas__gt=0, dias_vencimiento__lte=0) \
            .values('nom_bodega',
                    'nom_categoria',
                    "nom_negocio",
                    'nom_linea',
                    'nom_marca',
                    'nom_articulo',
                    'estibas',
                    'dias_vencimiento')

        data = cedi.frame_expired_line(q2) + \
               cedi.frame_expired_marca(q2) + \
               cedi.frame_expired_product(q2)

        return {'expired': cedi.frame_expired(q),
                'storage': cedi.frame_expired_storage(q2),
                'series': cedi.frame_expired_business(q2),
                'drills': data
                }
