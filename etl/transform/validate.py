import csv
import pandas as pd
import numpy as np


class ValidateCsv:

    def __init__(self, path, separator, min, max):
        self.separator = separator
        self.path = path
        self.data = pd.read_csv(self.path, header=0, sep=self.separator)
        self.min = min
        self.max = max

    # https://docs.python.org/3/library/csv.html
    def is_separator(self):
        v_separator_file = open(self.path, 'r')
        v_find = csv.Sniffer().sniff(v_separator_file.read())
        v_separator_file.close()
        print('VALIDACIÓN SEPARADOR DE ARCHIVO')
        if self.separator == v_find.delimiter:
            print('Separador de archivo...Correcto\n')
            return True
        else:
            print('Separador de archivo...Incorrecto')
            return False

    def has_correct_size(self):
        print('VALIDACIÓN CANTIDAD DE REGISTROS')
        print('cargando Archivo...\nResumen de datos: \n')
        res = self.data.describe()
        print(str(res))
        # validación de Número de Filas (0>filas<10.000) len()=numero de filas  count()=numer de registros por cada
        # columna
        registers = len(self.data)
        if registers < self.min:
            print(
                "Se requeiren mas de 10 filas para cargar el archivo\n Por favor revise el archivo\n ARCHIVO NO CARGADO")
            return False
        elif registers >= self.max:
            print("El maximo de registros permitidos es de: " + str(
                self.max) + "\nPor favor revise el archivo\nARCHIVO NO CARGADO")
            return False
        else:
            print("cantidad de registros valida\nARCHIVO CARGADO\n")
            return True

    def has_template(self, path):
        print('VALIDACIÓN CANTIDAD, ORDEN Y NOMBRES DE COLUMNAS')
        path_template = path
        template = pd.read_csv(path_template, header=0, sep=';')
        template_columns = template.columns
        source_columns = self.data.columns
        if len(template_columns) != len(source_columns):
            print('  Cantidad de columnas: NO ES CORRECTA')
            return False
        print('	Cantidad de Columnas: CORRECTA')
        order = np.array_equal(template_columns, source_columns)
        if order is not True:
            print('  Orden y Nombre de Columnas: NO ES CORRECTA')
            return False
        else:
            print('  Orden y Nombre de Columnas: CORRECTA\n')
            return True

    def is_null(self):
        print('VALIDACION DATOS NULOS')
        df = self.data[['FECHA_REGISTRO', 'COD_BODEGA', 'COD_NEGOCIO', 'COD_LINEA', 'COD_MARCA', 'COD_ARTICULO']]
        search_null = df.isna().sum()
        search_null = search_null[search_null >= 1]
        na = search_null.sum()

        if na >= 1:
            print('Existe ID = Null  en las siguientes columnas\n')
            print(search_null)
            print('Total registros en Null:' + str(na) + '\n')
            # Ubica posicion del NaN (indice)
            buscar_na = df.isna()
            x = (buscar_na[buscar_na['FECHA_REGISTRO'] is True][[]].index.values.astype(int)) + 2
            print('Existen registros sin ID en la columna FECHA_REGISTRO fila:' + str(x))
            x = (buscar_na[buscar_na['COD_BODEGA'] is True][[]].index.values.astype(int)) + 2
            print('Existen registros sin ID en la columna ID_BODEGA fila:' + str(x))
            x = (buscar_na[buscar_na['COD_NEGOCIO'] is True][[]].index.values.astype(int)) + 2
            print('Existen registros sin ID en la columna ID_NEGOCIO fila:' + str(x))
            x = (buscar_na[buscar_na['COD_LINEA'] is True][[]].index.values.astype(int)) + 2
            print('Existen registros sin ID en la la columna ID_LINEA fila:' + str(x))
            x = (buscar_na[buscar_na['COD_MARCA'] is True][[]].index.values.astype(int)) + 2
            print('Existen registros sin ID en la columna ID_MARCA fila:' + str(x))
            x = (buscar_na[buscar_na['COD_ARTICULO'] is True][[]].index.values.astype(int)) + 2
            print('Existen registros sin ID en la collumna ID_ARTICULO fila:' + str(x))
            return False
        else:
            print('CORRECTA\n')
            return True

    # crear destructor
