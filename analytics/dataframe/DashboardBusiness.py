import pandas as pd
from django.db.models import Sum
from analytics.models import DashboardBusiness


class MakeDataFrameBusiness:

    def __init__(self, query):
        self.df = pd.DataFrame(list(query))

    def frame_internal_external(self):
        df2 = self.df[['categoria_id', 'nom_categoria', 'estibas']]
        df2.columns = ['categoria_id', 'name', 'count']
        df3 = df2.groupby(['categoria_id', 'name']).sum()
        df3['y'] = df3['count'] / df3['count'].sum()
        df3.round({'y': 2})
        return {'records': df3.to_dict(orient='records'), 'total': df3['count'].sum()}

    def frame_total_external(self):
        df4 = self.df[self.df.nom_categoria.isin(['Externo Regular', 'Externo Devoluciones'])]
        total_estibas_externas = df4[['estibas']].sum()
        total_estibas_externas = (int(round(total_estibas_externas)))
        porc_externo = ((total_estibas_externas * 100) / self.df['estibas'].sum())
        print('Total Estibas Almacenamiento Externo: ' + str(total_estibas_externas) + '  ' + str(porc_externo))
        return {'total': total_estibas_externas, 'percent': round(porc_externo, 2)}

    def frame_total_internal(self):
        df3 = self.df[self.df.nom_categoria.isin(['Interno Regular', 'Interno Devoluciones'])]
        total_estibas_internas = df3[['estibas']].sum()
        total_estibas_internas = (int(round(total_estibas_internas)))
        porc_interno = ((total_estibas_internas * 100) / self.df['estibas'].sum())
        print('Total Estibas Almacenamiento Interno: ' + str(total_estibas_internas) + ' ' + str(porc_interno))
        return {'total': total_estibas_internas, 'percent': round(porc_interno, 2)}

    def frame_storage_cedi(self):
        print('\nAlmacenamiento x Bodega')
        df2 = self.df[["cod_bodega", "nom_bodega", "nom_categoria", 'estibas']]
        df2.columns = ['bodega_id', 'name', 'type', 'count']
        print(df2)
        df3 = df2.groupby(['bodega_id', 'name', 'type']).sum()
        total_estibas = df3['count'].sum()
        df3['y'] = df3['count'] / total_estibas
        df3.round({'y': 2})
        return {'records': df3.to_dict(orient='records'), 'total': total_estibas}

    def frame_total_status(self):
        print('\nAlmacenamiento x Estado Mcia')
        df2 = self.df[['nom_bodega', 'sku_transito', 'sku_no_apta']]
        print(df2)
        total_estibas_transito = df2["sku_transito"].sum()
        print('Estibas en Transito : ' + str(total_estibas_transito))
        # ---
        total_estibas_no_apta = df2["sku_no_apta"].sum()
        print('Estibas Mci No_APTA : ' + str(total_estibas_no_apta))
        # ---
        df3 = self.df[self.df.nom_categoria.isin(['Interno Devoluciones'])]
        total_estibas_dev_int = df3[['estibas']].sum()
        total_estibas_dev_int = (int(round(total_estibas_dev_int)))
        # ---
        df4 = self.df[self.df.nom_categoria.isin(['Externo Devoluciones'])]
        total_estibas_dev_ext = df4[['estibas']].sum()
        total_estibas_dev_ext = (int(round(total_estibas_dev_ext)))
        total_estibas_dev = total_estibas_dev_int + total_estibas_dev_ext
        # ----
        print('Estibas Mci Devuelta : ' + str(total_estibas_dev))
        titles = ['Almc. Interno (Devolución)', 'Almc. Externo (Devolución)', 'En tránstio', 'No Apta']
        values = [total_estibas_dev_int, total_estibas_dev, total_estibas_transito, total_estibas_no_apta]
        return {'titles': titles, 'values': values}
