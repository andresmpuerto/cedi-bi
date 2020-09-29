from django.shortcuts import render
from django.utils.timezone import now
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from django.db.models import Sum
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from analytics.models import DashboardCedi
from core.models import NegociosDim, LineasDim, MarcasDim, FactAlmacenamiento


def response_data(message, status=200, extra_data=None):
    data = {'coderesponse': 0, 'message': message, 'date': now().strftime("%Y/%m/%d %H:%M:%S")}
    if extra_data:
        data.update(extra_data)
    return Response(status=status, data=data)


class OccupationBoardObject(ListAPIView):
    # serializer_class = BoardSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read']

    def get_queryset(self):
        if self.kwargs['pk'] == 0:
            values = NegociosDim.objects.all()
        else:
            values = NegociosDim.objects.filter(pk=self.kwargs['pk'])
        return values

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        # serialize = BoardSerializer(instance)
        data = {}
        for negocio in list(instance):
            lineas_negocio = LineasDim.objects.filter(cod_negocio=negocio.cod_negocio)
            data['NEGOCIO-' + str(negocio.cod_negocio)] = {}
            for linea in list(lineas_negocio):
                marcas_linea = MarcasDim.objects.filter(cod_linea=linea.cod_linea)
                data['NEGOCIO-' + str(negocio.cod_negocio)]['LINEA-' + str(linea.cod_linea)] = {}
                for marca in list(marcas_linea):
                    data['NEGOCIO-' + str(negocio.cod_negocio)]['LINEA-' + str(linea.cod_linea)][
                        'MARCA-' + marca.nom_marca] = {}
                    articulos_marca = DashboardCedi.objects\
                        .filter(cod_marca=marca.cod_marca) \
                        .values("cod_articulo")\
                        .annotate(Sum("estibas"))
                    for articulo in list(articulos_marca):
                        data['NEGOCIO-' + str(negocio.cod_negocio)]['LINEA-' + str(linea.cod_linea)][
                            'MARCA-' + marca.nom_marca][
                            'ARTICULO-' + str(articulo['cod_articulo'])] = articulo['estibas__sum']

        return response_data(message='Board Ocupacion', extra_data={'graph': data})


class ExpiredBoardObject(ListAPIView):
    # serializer_class = BoardSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read']

    def get_queryset(self):
        values = NegociosDim.objects.all()
        return values

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        # serialize = BoardSerializer(instance)
        data = {}
        for negocio in list(instance):
            lineas_negocio = LineasDim.objects.filter(cod_negocio=negocio.cod_negocio)
            data['NEGOCIO-' + str(negocio.cod_negocio)] = {}
            for linea in list(lineas_negocio):
                marcas_linea = MarcasDim.objects.filter(cod_linea=linea.cod_linea)
                data['NEGOCIO-' + str(negocio.cod_negocio)]['LINEA-' + str(linea.cod_linea)] = {}

        return response_data(message='Board Ocupacion', extra_data={'graph': data})
