import pandas as pd


class BoardExpiration:

    def frame_expired(self, query):
        df2 = pd.DataFrame(list(query))
        df2.columns = ['estibas', 'dias_vencimiento']
        filter = df2[df2['dias_vencimiento'] <= 0]
        print(filter)
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
        total_estibas_porc = total_estibas_ven_porc + total_estibas_nven_porc
        print('Porc. estiba Mcia Vencida : ' + str(total_estibas_ven_porc))
        print('Porc. estiba Mcia NO Vencida : ' + str(total_estibas_nven_porc))
        print('Porc. total estibas : ' + str(total_estibas_porc) + '\n')

        return {
            'expired': {'total': total_estibas_ven, 'porc': total_estibas_ven_porc},
            'no_expired': {'total': total_estibas_nven, 'porc': total_estibas_nven_porc},
            'total_estibas': total_estibas_porc
        }

    def frame_expired_storage(self, query):
        df2 = pd.DataFrame(list(query))
        df2.columns = ['name', 'nom_categoria', 'count']
        total_estibas = df2[['count']].sum()
        total_estibas = (int(round(total_estibas)))
        df2['y'] = ((df2[['count']] * 100) / total_estibas)
        df2.round({'y': 2})
        print('Total estibas Mcia Vencida x Bodega : ' + str(total_estibas))
        return {
            'records': df2.to_dict(orient='records'),
            'total': total_estibas
        }

    def frame_expired_business(self, query):
        df2 = pd.DataFrame(list(query))
        df2.columns = ['nom_negocio', 'count']
        total_estibas = df2[['count']].sum()
        total_estibas = (int(round(total_estibas)))
        df2['porc'] = ((df2[['count']] * 100) / total_estibas)
        df2.round({'porc': 2})
        print('Total estibas Mcia Vencida x Negocio : ' + str(total_estibas))
        return {
            'records': df2.to_dict(orient='records'),
            'total': total_estibas
        }

    def frame_expired_line(self, query):
        df2 = pd.DataFrame(list(query))
        df2.columns = ['nom_negocio', 'nom_linea', 'count']
        total_estibas = df2[['count']].sum()
        total_estibas = (int(round(total_estibas)))
        df2['porc'] = ((df2[['count']] * 100) / total_estibas)
        df2.round({'porc': 2})
        print('Total estibas Mcia Vencida x Linea : ' + str(total_estibas))
        return {
            'records': df2.to_dict(orient='records'),
            'total': total_estibas
        }

    def frame_expired_product(self, query):
        df2 = pd.DataFrame(list(query))
        df2.columns = ['nom_negocio', 'nom_linea', 'nom_articulo', 'count']
        total_estibas = df2[['count']].sum()
        total_estibas = (int(round(total_estibas)))
        df2['porc'] = ((df2[['count']] * 100) / total_estibas)
        df2.round({'porc': 2})
        print('Total estibas Mcia Vencida x articulo : ' + str(total_estibas))
        return {
            'records': df2.to_dict(orient='records'),
            'total': total_estibas
        }
