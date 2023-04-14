
while True:

    import pandas as pd
    from os import remove
    import time

    from classes import dbAzure
    DBAzure = dbAzure.DBAzure

    from helpers import correoEnvioArchivo, validarProduccion, rutas, correosDestino
    estadoProduccion    = validarProduccion.validarProduccion()
    rutaRelativa        = rutas.rutas()

    from helpers import rutas, correoEnvioArchivo, correosDestino, validarProduccion
    correoEnvioArchivo  = correoEnvioArchivo.correoEnvioArchivo


    rutaRelativa = rutaRelativa.replace('\\SRC', '')
    print(rutaRelativa)

    dbAzure = DBAzure(estadoProduccion)

    equipos = dbAzure.getQuerySolpeds()
    equipos = equipos.rename({
    'ORDEN_COMPRA'    :'ORDEN_TRABAJO'
    },axis=1)

    len(equipos != 0)
    if(len(equipos != 0)):
        print("entra a enviar",len(equipos))
        equipos_envio = equipos.drop(
            ['temperaturaMinima','temperaturaMaxima','Creado', 'DESCRIPCION', 'Modificado','created_at', 'updated_at', 'id' ], axis=1)
        rutaRelativa.replace('/PROYECTOS', '/PROYECTOS/ROTACION/DOCS')
        equipos_envio.to_excel("EQUIPOS_NO_OPERATIVOS.xlsx")
        print("crear excel")

        rutaRelativa = rutaRelativa.replace('/PROYECTOS', '/PROYECTOS/ROTACION')

        correos         = correosDestino.correosDestino(estadoProduccion)
        correos['to'].append('jose.garrido@jumbo.cl')


        archivos    = []
        archivos.append({
            'nombre_archivo':   'EQUIPOS_NO_OPERATIVOS.xlsx',
            'tipo_archivo':     'application',
            'formato_archivo': 'vnd.ms-excel',
            'ruta':             f'{rutaRelativa}/EQUIPOS_NO_OPERATIVOS.xlsx'
        })
        correoEnvioArchivo('EQUIPOS NO OPERATIVOS DS', "", correos, archivos)
        print("CORREO ENVIADO")

        equipos['ESTADO_CORREO'] = 'NO ENVIAR'

        for index in equipos.index:
            dbAzure.changeStatusSolped(equipos.iloc[index])

        time.sleep(20)

    else:
        print("no envia",len(equipos))
        time.sleep(20)
        continue
