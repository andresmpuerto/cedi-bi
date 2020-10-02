import pandas as pd
import numpy as np
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker


class Dimensions:
    def __init__(self, path, separator, db_data):
        self.separator = separator
        self.path = path
        self.data = pd.read_csv(self.path, header=0, sep=self.separator)
        self.engine = sql.create_engine("mysql+mysqldb://{user}:{pw}@{host}/{db}"
                                        .format(user=db_data[0],
                                                pw=db_data[1],
                                                host=db_data[2],
                                                db=db_data[3]))

    # MAESTRA DE BODEGAS
    def dim_bodegas(self):
        print('Creación de Dimension de Bodegas')
        df = pd.DataFrame(self.data[['COD_BODEGA', 'NOM_BODEGA']])
        df = df.drop_duplicates(['COD_BODEGA', 'NOM_BODEGA'])[['COD_BODEGA', 'NOM_BODEGA']]
        # if (df.ID_NEGOCIO.count()) >= 1:
        df.to_sql('core_bodegasdimttemp', con=self.engine, if_exists='append', index=False, index_label=None,
                  chunksize=10000)

        # Session = sessionmaker(bind=self.engine)
        # session = Session()
        # try:
        print('Actualización Categoria Bodegas')
        sql_query = sql.text(
            "UPDATE core_bodegasdimttemp SET categoria_id = 1 WHERE cod_bodega IN ('1','59','71','BF','I7','T8');")
        self.engine.execute(sql_query)
        sql_query = sql.text("COMMIT;")
        self.engine.execute(sql_query)

        sql_query = sql.text(
            "UPDATE core_bodegasdimttemp SET categoria_id = 3 WHERE cod_bodega IN ('8','88','C7','C8','C9');")
        self.engine.execute(sql_query)
        sql_query = sql.text("COMMIT;")
        self.engine.execute(sql_query)

        sql_query = sql.text(
            "UPDATE core_bodegasdimttemp SET categoria_id = 2 WHERE cod_bodega IN ('2','48','81','BA','BC');")
        self.engine.execute(sql_query)
        sql_query = sql.text("COMMIT;")
        self.engine.execute(sql_query)

        sql_query = sql.text("UPDATE core_bodegasdimttemp SET categoria_id = 4 WHERE cod_bodega IN ('43','C5');")
        self.engine.execute(sql_query)
        sql_query = sql.text("COMMIT;")
        self.engine.execute(sql_query)

        sql_query = sql.text("CALL cargar_bodegas_dim;")
        self.engine.execute(sql_query)
        #     session.commit()
        # except:
        #     session.rollback()
        # finally:
        #     session.close()

    # MAESTRA DE NEGOCIOS
    def dim_negocios(self):
        print('Creación de Dimension de Negocios')
        df = pd.DataFrame(self.data[['COD_NEGOCIO', 'NOM_NEGOCIO']])
        df = df.drop_duplicates(['COD_NEGOCIO', 'NOM_NEGOCIO'])[['COD_NEGOCIO', 'NOM_NEGOCIO']]
        # if (df.ID_NEGOCIO.count()) >= 1:
        df.to_sql('core_negociosdimttemp', con=self.engine, if_exists='append', index=False, index_label=None,
                  chunksize=10000)
        sql_query = sql.text("CALL cargar_negocios_dim;")
        self.engine.execute(sql_query)

    # MAESTRA DE LINEAS
    def dim_lineas(self):
        print('Creación de Dimension de Lineas')
        df = pd.DataFrame(self.data[['COD_LINEA', 'NOM_LINEA', 'COD_NEGOCIO', ]])
        df = df.drop_duplicates(['COD_LINEA', 'NOM_LINEA', 'COD_NEGOCIO'])[['COD_LINEA', 'NOM_LINEA', 'COD_NEGOCIO', ]]
        # if (df.ID_LINEA.count()) >= 1:
        df.to_sql('core_lineasdimttemp', con=self.engine, if_exists='append', index=False, index_label=None,
                  chunksize=10000)
        sql_query = sql.text("CALL cargar_lineas_dim;")
        self.engine.execute(sql_query)

    # MAESTRA DE MARCAS
    def dim_marcas(self):
        print('Creación de Dimension de Marcas')
        df = pd.DataFrame(self.data[['COD_MARCA', 'NOM_MARCA', 'COD_LINEA', ]])
        df = df.drop_duplicates(['COD_MARCA', 'NOM_MARCA', 'COD_LINEA', ])[['COD_MARCA', 'NOM_MARCA', 'COD_LINEA' ]]
        # if (df.ID_MARCA.count()) >= 1:
        df.to_sql('core_marcasdimttemp', con=self.engine, if_exists='append', index=False, index_label=None,
                  chunksize=10000)
        sql_query = sql.text("CALL cargar_marcas_dim;")
        self.engine.execute(sql_query)

    # MAESTRA DE ARTICULOS
    def dim_articulos(self):
        print('Creación de Dimension de Articulos')
        df = pd.DataFrame(
            self.data[['COD_ARTICULO', 'NOM_ARTICULO', 'PRESENTACION', 'UNIDAD_VENTA', 'FACTOR_ESTIBA', 'COD_MARCA']])
        df = df.drop_duplicates(['COD_ARTICULO', 'NOM_ARTICULO', 'PRESENTACION', 'UNIDAD_VENTA', 'COD_MARCA'])[
            ['COD_ARTICULO', 'NOM_ARTICULO', 'PRESENTACION', 'UNIDAD_VENTA', 'FACTOR_ESTIBA', 'COD_MARCA', ]]
        # if (df.ID_MARCA.count()) >= 1:
        df.to_sql('core_articulosdimttemp',
                  con=self.engine,
                  if_exists='append',
                  index=False, index_label=None,
                  chunksize=10000)
        sql_query = sql.text("CALL cargar_articulos_dim;")
        self.engine.execute(sql_query)

    def dim_lotes(self):
        print('Creación de Dimension de Lotes')
        df = pd.DataFrame(self.data[['COD_LOTE', 'COD_ARTICULO', 'FECHA_FAB', 'FECHA_VENCIMIENTO']])
        df = df.drop_duplicates(['COD_LOTE', 'COD_ARTICULO', 'FECHA_FAB', 'FECHA_VENCIMIENTO'])[
            ['COD_LOTE', 'COD_ARTICULO', 'FECHA_FAB', 'FECHA_VENCIMIENTO']]
        print(df)
        df.to_sql('core_lotesdimttemp',
                  con=self.engine,
                  if_exists='append',
                  index=False, index_label=None,
                  chunksize=10000)
        sql_query = sql.text("CALL cargar_lotes_dim;")
        self.engine.execute(sql_query)
