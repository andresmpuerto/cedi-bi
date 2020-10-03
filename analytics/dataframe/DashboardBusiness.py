import pandas as pd
from django.db.models import Sum
from analytics.models import DashboardBusiness


class MakeDataFrameBusiness:

    def __init__(self, query):
        self.df = pd.DataFrame(list(query))

    def frame_internal_external(self):
        df = self.df[['cod_negocio', 'nom_negocio']]
        negocios = df.drop_duplicates()
        titles = list()
        cvalues = [{}, {}, {}, {}]
        cod = 0
        c1 = []
        c2 = []
        c3 = []
        c4 = []
        df5 = self.df[['categoria_id', 'nom_categoria', 'cod_negocio', 'estibas']]
        for negocio in negocios.to_dict(orient='records'):
            titles.append(negocio['nom_negocio'])
            cats = df5[df5['cod_negocio'] == negocio['cod_negocio']]
            df3 = cats.groupby(['categoria_id', 'nom_categoria', 'cod_negocio'], as_index=False).sum()
            print(df3)
            for cat in df3.to_dict(orient='records'):
                if cat['categoria_id'] is 1:
                    c1.append(cat['estibas'])
                    if cvalues[0] is {}:
                        cvalues[0] = {'name': cat['nom_categoria'], 'data': c1}
                    else:
                        cvalues[0]['data'] = c1
                elif cat['categoria_id'] is 2:
                    c2.append(cat['estibas'])
                    if cvalues[1] is {}:
                        cvalues[1] = {'name': cat['nom_categoria'], 'data': c2}
                    else:
                        cvalues[1]['data'] = c2
                elif cat['categoria_id'] is 3:
                    c3.append(cat['estibas'])
                    if cvalues[2] is {}:
                        cvalues[2] = {'name': cat['nom_categoria'], 'data': c3}
                    else:
                        cvalues[2]['data'] = c3
                else:
                    c4.append(cat['estibas'])
                    if cvalues[3] is {}:
                        cvalues[3] = {'name': cat['nom_categoria'], 'data': c4}
                    else:
                        cvalues[3]['data'] = c4
        return {'categories': titles, 'records': cvalues}

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
        print('\nAlmacenamiento x Negocio')
        df2 = self.df[["nom_negocio", 'estibas']]
        df2.columns = ['name', 'count']
        print(df2)
        df3 = df2.groupby(['name'], as_index=False).sum()
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
