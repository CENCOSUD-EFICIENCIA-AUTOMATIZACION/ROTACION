def correosDestino(estadoProduccion):
    if estadoProduccion:
        servidor = "produccion"
    else:
        servidor = "local"
    correos = {
        "produccion": {
            "to":   [],
            "cc":   [],
            "bcc":  [
                #'hector.tejedaihl@cencosud.cl',
                'camilo.mansilla@cencosud.cl',
            ],
        },
        "local": {
            "to": [],
            "cc": [],
            "bcc": [
                #'hector.tejedaihl@cencosud.cl',
                'camilo.mansilla@cencosud.cl',
            ],
        }
    }
    return correos[servidor]
