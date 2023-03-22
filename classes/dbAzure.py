import pyodbc
import pandas as pd
from datetime import datetime


class DBAzure:
    def __init__(self, estadoProduccion):
        self.server     = 'gestionprocesostiendas.database.windows.net'
        self.database   = 'GestionProcesosTienda'
        self.username   = 'htejedai'
        self.password   = 'Donaciones2022'
        if estadoProduccion:
            self.driver = '{ODBC Driver 18 for SQL Server}'
            
        else:
            self.driver = '{ODBC Driver 17 for SQL Server}' 
        self.query      = ""
        self.connection = ''
        self.dataConnection  = f'DRIVER={self.driver};SERVER=tcp:{self.server};PORT=1433;DATABASE={self.database};UID={self.username};PWD={self.password}'
        self.setConeccionDB()


    def setConeccionDB(self):
        print('==================')
        print('CONEXION CON EL SERVIDOR')
        print('==================')
        dataConnection  = f'DRIVER={self.driver};SERVER=tcp:{self.server};PORT=1433;DATABASE={self.database};UID={self.username};PWD={self.password}'
        self.connection = pyodbc.connect(dataConnection)
        

    def executeReadQuery(self):
        rows = None
        with self.connection.cursor() as cursor:
            cursor.execute(self.query)
            rows = cursor.fetchone()
            print(rows)
        return rows


    def executeEditQuery(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.query)
            resultado = cursor.fetchall()
            resultado = resultado[0][0]
            self.connection.commit()
            print(cursor.rowcount, "record(s) affected")
            return resultado
        except TypeError as e:
            print(f"The error '{e}' occurred")

    def editQuery(self):
            cursor = self.connection.cursor()
            cursor.execute(self.query)
            self.connection.commit()
            print(cursor.rowcount, "record(s) affected")

    def getQuerySolpeds(self):
        self.query = f"""
            SELECT *
            FROM equipos_frio_DS
            WHERE ESTADO_CORREO = 'POR_ENVIAR'
            order by id desc
        """
        return pd.read_sql(self.query, self.connection)


    def createSolped(self, solped):
        self.query = f"""
            SET NOCOUNT ON
            INSERT INTO equipos_frio_DS (
                nombreMaquina,
                NUMERO_SERIE,
                TIPO_DE_EQUIPO,
                ZONA,
                temperaturaMinima,
                temperaturaMaxima,
                ESTADO,
                nombreLocal,
                ESTADO_CORREO,
                created_at,
                updated_at,
                OTRO,
                OBSERVACION,
                MODELO,
                Creado,
                DESCRIPCION,
                ORDEN_COMPRA,
                Modificado,
                Observaciones
            )
            VALUES(
                '{solped["nombreMaquina"]}',
                '{solped["NUMERO_SERIE"]}',
                '{solped["TIPO_DE_EQUIPO"]}',
                '{solped["ZONA"]}',
                '{solped["temperaturaMinima"]}',
                '{solped["temperaturaMaxima"]}',
                '{solped["ESTADO"]}',
                '{solped["nombreLocal"]}',
                '{solped["ESTADO_CORREO"]}',
                '{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}',
                '{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                ''
            )
            SELECT @@IDENTITY;
        """
        resultado = self.executeEditQuery()
        print(resultado)
        return resultado


    def createHistory(self, solped, solpedDB, estado = 'nueva'):
        print(estado)
        if estado == 'nueva':
            self.query = f"""
            SET NOCOUNT ON
            INSERT INTO historial_capex (
                    solped,
                    id_solped_capex,
                    ocs,
                    estado,
                    motivo,
                    accion,
                    fecha,
                    estado_trabajo,
                    monto
                )
                VALUES(
                    '{int(solped["Solped"])}',
                    '{int(solpedDB)}',
                    '0',
                    'CREADA',
                    'CREACIÓN SOLPED',
                    'CREADA',
                    '{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}',
                    '{solped["estado_trabajo"]}',
                    '{solped["Total ML"]}
                )
                SELECT @@IDENTITY;
            """
        elif estado == "cambio_estado":
            self.query = f"""
            SET NOCOUNT ON
            INSERT INTO historial_capex (
                    solped,
                    id_solped_capex,
                    ocs,
                    estado,
                    motivo,
                    accion,
                    fecha,
                    estado_trabajo,
                    monto
                )
                VALUES(
                    '{int(solpedDB["solped"])}',
                    '{int(solpedDB['id'])}',
                    '{int(solpedDB['ocs'])}',
                    '{solpedDB['estado']}',
                    'ACTUALIZACIÓN SOLPED',
                    'ACTUALIZACION ESTADO TRABAJO',
                    '{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}',
                    '{solpedDB["estado_trabajo"]}',
                    '{solpedDB["monto"]}'
                )
                SELECT @@IDENTITY;
            """
        elif estado == "cambio_monto":
            self.query = f"""
            SET NOCOUNT ON
            INSERT INTO historial_capex (
                    solped,
                    id_solped_capex,
                    ocs,
                    estado,
                    motivo,
                    accion,
                    fecha,
                    estado_trabajo,
                    monto
                )
                VALUES(
                    '{int(solpedDB["solped"])}',
                    '{int(solpedDB['id'])}',
                    '{int(solpedDB['ocs'])}',
                    '{solpedDB['estado']}',
                    'ACTUALIZACIÓN SOLPED',
                    'ACTUALIZACION MONTO',
                    '{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}',
                    '{solpedDB["estado_trabajo"]}',
                    '{solpedDB["monto"]}'
                )
                SELECT @@IDENTITY;
            """
        self.executeEditQuery()


    def editQuerySolped(self, solped):
        self.query = f"""
            UPDATE solped_capex
            SET contador = {solped}
        """
    
    def UpdateQuerySolped(self, solped, tipo_cambio):
        if tipo_cambio == 'cambio_estado':
            self.query = f"""
                UPDATE solped_capex
                SET estado_trabajo_estandarizado = '{solped['estado_trabajo_estandarizado']}', estado_trabajo = '{solped['estado_trabajo']}'
                WHERE solped = '{solped['solped']}'
            """
        elif tipo_cambio == 'cambio_ocs':
            self.query = f"""
                UPDATE solped_capex
                SET ocs = '{solped['ocs']}'
                WHERE solped = '{solped['solped']}'
            """
        elif tipo_cambio == 'cambio_monto':
            self.query = f"""
                UPDATE solped_capex
                SET monto = '{solped['monto']}'
                WHERE solped = '{solped['solped']}'
            """
        
        else:
            self.query = f"""
                UPDATE solped_capex
                SET estado_trabajo_estandarizado = '{solped['estado_trabajo_estandarizado']}', estado_trabajo = '{solped['estado_trabajo']}', ocs = '{solped['ocs']}'
                WHERE solped = '{solped['solped']}'
            """
        self.editQuery()
    
    def getSolpedById(self, solped):
        self.query = f"""
            SELECT *
            FROM solped_capex
            WHERE solped = '{solped}'
        """
        return pd.read_sql_query(self.query, self.connection)
    
    def changeStatusSolped(self, equipos):
        self.query = f"""
            UPDATE equipos_frio_DS
            SET ESTADO_CORREO = '{equipos['ESTADO_CORREO']}'
            WHERE id = '{equipos['id']}'
        """
        self.editQuery()