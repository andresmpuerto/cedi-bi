import pandas as pd
from django.db.models import Sum
from analytics.models import DashboardBusiness


class MakeDataFrameBusiness:

    def __init__(self, query):
        self.df = pd.DataFrame(list(query))
        self.df.columns = ['categoria_id', 'name', 'count']
        self.total_estibas = self.df[['count']].sum()
        self.total_estibas = (int(round(self.total_estibas)))

    def frame_internal_external(self):
        self.df['y'] = ((self.df[['count']] * 100) / self.total_estibas)
        self.df.round({'y': 2})
        return {'records': self.df.to_dict(orient='records'), 'total': self.total_estibas}

    def frame_total_external(self):
        df4 = self.df[self.df.name.isin(['Externo Regular', 'Externo Devoluciones'])]
        total_estibas_externas = df4[['count']].sum()
        total_estibas_externas = (int(round(total_estibas_externas)))
        porc_externo = ((total_estibas_externas * 100) / self.total_estibas)
        print(df4)
        print('Total Estibas Almacenamiento Externo: ' + str(total_estibas_externas) + '  ' + str(porc_externo))
        return {'total': total_estibas_externas, 'percent': round(porc_externo, 2)}

    def frame_total_internal(self):
        df3 = self.df[self.df.name.isin(['Interno Regular', 'Interno Devoluciones'])]
        total_estibas_internas = df3[['count']].sum()
        total_estibas_internas = (int(round(total_estibas_internas)))
        porc_interno = ((total_estibas_internas * 100) / self.total_estibas)
        print(df3)
        print('Total Estibas Almacenamiento Interno: ' + str(total_estibas_internas) + '  ' + str(porc_interno))
        return {'total': total_estibas_internas, 'percent': round(porc_interno, 2)}

    def frame_storage_cedi(self):
        print('\nAlmacenamiento x Bodega')
        values = DashboardBusiness.objects.filter(estibas__gt=0)\
            .values("cod_bodega", "nom_bodega", "nom_categoria")\
            .annotate(Sum('estibas'))
        df2 = pd.DataFrame(list(values))
        df2.columns = ['bodega_id', 'name', 'type', 'count']
        total_estibas = df2[['count']].sum()
        total_estibas = (int(round(total_estibas)))
        df2['y'] = ((df2[['count']] * 100) / total_estibas)
        df2.round({'y': 2})
        return {'records': df2.to_dict(orient='records'), 'total': total_estibas}

    def frame_total_status(self):
        print('\nAlmacenamiento x Estado Mcia')
        values = DashboardBusiness.objects.values('nom_bodega')\
            .annotate(Sum('sku_transito'))\
            .annotate(Sum('sku_no_apta'))
        df2 = pd.DataFrame(list(values))
        print(df2)
        df2.columns = ['bodega', 'transito', 'no_apta']
        total_estibas_transito = df2[['transito']].sum()
        print('Estibas en Transito : ' + str(total_estibas_transito))
        # ----
        total_estibas_no_apta = df2[['no_apta']].sum()
        print('Estibas Mci No_APTA : ' + str(total_estibas_no_apta))
        # ----
        df3 = self.df[self.df.name.isin(['Interno Devoluciones'])]
        total_estibas_dev_int = df3[['count']].sum()
        total_estibas_dev_int = (int(round(total_estibas_dev_int)))
        # ---
        df4 = self.df[self.df.name.isin(['Externo Devoluciones'])]
        total_estibas_dev_ext = df4[['count']].sum()
        total_estibas_dev_ext = (int(round(total_estibas_dev_ext)))
        total_estibas_dev = total_estibas_dev_int + total_estibas_dev_ext
        print('Estibas Mci Devuelta : ' + str(total_estibas_dev))
        titles = ['Almc. Interno (Devolución)', 'Almc. Externo (Devolución)', 'En tránstio', 'No Apta']
        values = [total_estibas_dev_int, total_estibas_dev, total_estibas_transito, total_estibas_no_apta]
        return {'titles': titles, 'values': values}