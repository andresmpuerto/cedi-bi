import pandas as pd
import numpy as np
import sqlalchemy as sql


class Fact:
    def __init__(self, path, separator, db_data):
        self.separator = separator
        self.path = path
        self.data = pd.read_csv(self.path, header=0, sep=self.separator)
        self.engine = sql.create_engine("mysql+mysqldb://{user}:{pw}@{host}/{db}"
                                        .format(user=db_data[0],
                                                pw=db_data[1],
                                                host=db_data[2],
                                                db=db_data[3]))

    # TABLA DE HECHOS
    def cedibi_fact(self):
        print('Creación de Tabla de Hechos')
        df = pd.DataFrame(self.data[['CANTIDAD_INICIAL', 'CANTIDAD_ENTRADAS', 'CANTIDAD_SALIDAS',
                                     'CANTIDAD_VENTAS', 'CANTIDAD_DEVOLUCION', 'CANTIDAD_EXISTENCIAS',
                                     'CANTIDAD_SEPARACION', 'CANTIDAD_RESERVA', 'CANTIDAD_TRANSITO',
                                     'CANTIDAD_NO_APTA', 'FECHA_REGISTRO', 'COD_BODEGA', 'COD_NEGOCIO',
                                     'COD_LINEA', 'COD_MARCA',  'COD_ARTICULO'
                                     ]])
        # if (df.ID_NEGOCIO.count()) >= 1:
        df.to_sql('core_factalmacenamiento',
                  con=self.engine,
                  if_exists='append',
                  index=False,
                  index_label=None,
                  chunksize=10000)
    # print(df.ID_NEGOCIO.count())
    # print('Dimensión de negocios Cargada\n')


