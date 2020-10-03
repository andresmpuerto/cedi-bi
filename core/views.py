from django.shortcuts import render
from django.utils.timezone import now
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from django.db.models import Sum
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from analytics.models import DashboardCedi, Board, DashboardBusiness
from analytics.serializers import BoardSerializer
from core.models import NegociosDim, LineasDim, MarcasDim, FactAlmacenamiento


def response_data(message, status=200, extra_data=None):
    data = {'coderesponse': 0, 'message': message, 'date': now().strftime("%Y/%m/%d %H:%M:%S")}
    if extra_data:
        data.update(extra_data)
    return Response(status=status, data=data)


class OccupationBoardObject(RetrieveAPIView):
    serializer_class = BoardSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read']

    def get_queryset(self):
        values = Board.objects.filter(pk=self.kwargs["pk"])
        return get_object_or_404(values)

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset()
        negocios = DashboardBusiness.objects.filter(cod_bodega=self.kwargs['id']).values("cod_negocio", "nom_negocio") \
            .distinct()

        serialize = BoardSerializer(instance)
        data = {}
        for negocio in list(negocios):
            lineas_negocio = DashboardBusiness.objects.filter(cod_negocio=negocio['cod_negocio'],
                                                              cod_bodega=self.kwargs['id']).values("cod_linea",
                                                                                                   "nom_linea")
            cod = str(negocio['cod_negocio'])
            data['NEGOCIO-' + cod] = {}
            for linea in list(lineas_negocio):
                marcas_linea = DashboardBusiness.objects.filter(cod_linea=linea['cod_linea'],
                                                                cod_negocio=cod,
                                                                cod_bodega=self.kwargs['id']).values("cod_marca",
                                                                                                     "nom_marca")
                data['NEGOCIO-' + cod]['LINEA-' + str(linea['cod_linea'])] = {}
                for marca in list(marcas_linea):
                    data['NEGOCIO-' + cod]['LINEA-' + str(linea['cod_linea'])][
                        'MARCA-' + marca['nom_marca']] = {}
                    articulos_marca = DashboardBusiness.objects.filter(cod_linea=linea['cod_linea'],
                                                                       cod_negocio=cod,
                                                                       cod_marca=marca['cod_marca'],
                                                                       cod_bodega=self.kwargs['id']).values(
                        "cod_articulo").annotate(Sum("sku_cantidad_total"))
                    for articulo in list(articulos_marca):
                        data['NEGOCIO-' + cod]['LINEA-' + str(linea['cod_linea'])]['MARCA-' + marca['nom_marca']][
                            'ARTICULO-' + str(articulo['cod_articulo'])] = articulo['sku_cantidad_total__sum']

        return response_data(message='Board Ocupacion', extra_data={'graph': data, 'board': serialize.data})


class OccupationCediBoardObject(RetrieveAPIView):
    serializer_class = BoardSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read']

    def get_queryset(self):
        values = Board.objects.filter(pk=self.kwargs["pk"])
        return get_object_or_404(values)

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset()
        negocios = DashboardCedi.objects.filter(cod_bodega=self.kwargs['id']).values("cod_negocio", "nom_negocio") \
            .distinct()
        serialize = BoardSerializer(instance)
        data = {}
        for negocio in list(negocios):
            lineas_negocio = DashboardCedi.objects.filter(cod_negocio=negocio['cod_negocio'],
                                                          cod_bodega=self.kwargs['id']).values("cod_linea",
                                                                                               "nom_linea")
            cod = str(negocio['cod_negocio'])
            data['NEGOCIO-' + cod] = {}
            for linea in list(lineas_negocio):
                marcas_linea = DashboardCedi.objects.filter(cod_linea=linea['cod_linea'],
                                                            cod_negocio=cod,
                                                            cod_bodega=self.kwargs['id']).values("cod_marca",
                                                                                                 "nom_marca")
                data['NEGOCIO-' + cod]['LINEA-' + str(linea['cod_linea'])] = {}
                for marca in list(marcas_linea):
                    data['NEGOCIO-' + cod]['LINEA-' + str(linea['cod_linea'])][
                        'MARCA-' + marca['nom_marca']] = {}
                    articulos_marca = DashboardCedi.objects.filter(cod_linea=linea['cod_linea'],
                                                                   cod_negocio=cod,
                                                                   cod_marca=marca['cod_marca'],
                                                                   cod_bodega=self.kwargs['id']).values(
                        "cod_articulo").annotate(Sum("estibas"))
                    for articulo in list(articulos_marca):
                        data['NEGOCIO-' + cod]['LINEA-' + str(linea['cod_linea'])]['MARCA-' + marca['nom_marca']][
                            'ARTICULO-' + str(articulo['cod_articulo'])] = articulo['estibas__sum']

        return response_data(message='Board Ocupacion', extra_data={'graph': data, 'board': serialize.data})
