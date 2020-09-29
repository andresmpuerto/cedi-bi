import pandas as pd

from analytics.models import DashboardCedi


class BoardExpiration:

    def frame_expired(self, query):
        df = pd.DataFrame(list(query))
        df2 = df[['estibas', 'dias_vencimiento']]
        filter = df2[df2['dias_vencimiento'] <= 0]
        total_estibas_ven = filter[['estibas']].sum()
        total_estibas_ven = (int(round(total_estibas_ven)))
        print('Total estibas Mcia Vencida : ' + str(total_estibas_ven))
        no_filter = df2[df2['dias_vencimiento'] > 0]
        total_estibas_nven = no_filter[['estibas']].sum()
        total_estibas_nven = (int(round(total_estibas_nven)))
        print('Total estibas Mcia NO Vencida : ' + str(total_estibas_nven))
        total_estibas = total_estibas_ven + total_estibas_nven
        total_estibas_ven_porc = ((total_estibas_ven * 100) / total_estibas)
        total_estibas_nven_porc = ((total_estibas_nven * 100) / total_estibas)
        print('Porc. estiba Mcia Vencida : ' + str(total_estibas_ven_porc))
        print('Porc. estiba Mcia NO Vencida : ' + str(total_estibas_nven_porc))
        print('Porc. total estibas : ' + str(total_estibas) + '\n')

        return {
            'expired': {'total': total_estibas_ven, 'porc': total_estibas_ven_porc},
            'no_expired': {'total': total_estibas_nven, 'porc': total_estibas_nven_porc},
            'total_estibas': total_estibas
        }

    def frame_expired_storage(self, query):
        df = pd.DataFrame(list(query))
        df2 = df[['nom_bodega', 'nom_categoria', 'estibas']]
        df2.columns = ['name', 'nom_categoria', 'count']
        df3 = df2.groupby(['name', 'nom_categoria'], as_index=False).sum()
        total_estibas = df3[['count']].sum()
        total_estibas = (int(round(total_estibas)))
        df3['y'] = ((df3[['count']] * 100) / total_estibas)
        df3.round({'y': 2})
        print('Total estibas Mcia Vencida x Bodega : ' + str(total_estibas))
        return {
            'records': df3.to_dict(orient='records'),
            'total': total_estibas
        }

    def frame_expired_business(self, query):
        df = pd.DataFrame(list(query))
        df2 = df[['nom_negocio', 'estibas']]
        df2.columns = ['name', 'count']
        df3 = df2.groupby(['name'], as_index=False).sum()
        df3['drilldown'] = df3['name']
        df3['y'] = df3['count'] / df3['count'].sum()
        return {'records': df3.to_dict(orient='records')}

    def frame_expired_line(self, query):
        df = pd.DataFrame(list(query))
        df2 = df[["nom_negocio", "nom_linea", "estibas"]]
        df2.columns = ['id', 'name', 'count']
        df3 = df2.groupby(['id', 'name'], as_index=False).sum()
        df3['drilldown'] = df3['name']
        df3['y'] = df3['count'] / df3['count'].sum()
        records = df3.to_dict(orient='records')
        drill = list()
        for record in records:
            if len(drill) is 0:
                drill.append({
                    'name': record['id'],
                    'colorByPoint': True,
                    'id': record['id'],
                    'data': []
                })

            if drill[-1]['name'] is record['id']:
                drill[-1]['data'].append({'name': record['name'], 'y': record['y'], 'drilldown': record['name']})
            else:
                drill.append({
                    'name': record['id'],
                    'colorByPoint': True,
                    'id': record['id'],
                    'data': [{'name': record['name'], 'y': record['y'], 'drilldown': record['name']}]
                })

        return drill

    def frame_expired_marca(self, query):
        df = pd.DataFrame(list(query))
        df2 = df[["nom_linea", "nom_marca", "estibas"]]
        df2.columns = ['id', 'name', 'count']
        df3 = df2.groupby(['id', 'name'], as_index=False).sum()
        df3['drilldown'] = df3['name']
        df3['y'] = df3['count'] / df3['count'].sum()
        records = df3.to_dict(orient='records')
        drill = list()
        for record in records:
            if len(drill) is 0:
                drill.append({
                    'name': record['id'],
                    'colorByPoint': True,
                    'id': record['id'],
                    'data': []
                })

            if drill[-1]['name'] is record['id']:
                drill[-1]['data'].append({'name': record['name'], 'y': record['y'], 'drilldown': record['name']})
            else:
                drill.append({
                    'name': record['id'],
                    'colorByPoint': True,
                    'id': record['id'],
                    'data': [{'name': record['name'], 'y': record['y'], 'drilldown': record['name']}]
                })

        return drill

    def frame_expired_product(self, query):
        df = pd.DataFrame(list(query))
        df2 = df[["nom_marca", "nom_articulo", "estibas"]]
        df2.columns = ['id', 'name', 'count']
        df3 = df2.groupby(['id', 'name'], as_index=False).sum()
        df3['y'] = df3['count'] / df3['count'].sum()
        records = df3.to_dict(orient='records')
        drill = list()

        for record in records:
            if len(drill) is 0:
                drill.append({
                    'name': record['id'],
                    'colorByPoint': True,
                    'id': record['id'],
                    'data': []
                })

            if drill[-1]['name'] is record['id']:
                drill[-1]['data'].append([record['name'], record['y']])
            else:
                drill.append({
                    'name': record['id'],
                    'colorByPoint': True,
                    'id': record['id'],
                    'data': [[record['name'], record['y']]]
                })

        return drill
