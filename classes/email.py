import json
import msal
import base64
import requests
from time import sleep


class Email():
    def __init__(self, toUserEmail, asuntos, ruta, robot, nombreArchivo=None):
        self.CLIENT_ID   = 'eab16f14-dd68-45a2-a309-b7e08cc14cd4'
        self.TENTANT_ID  = 'a50762c4-c5ad-413a-a05e-9ffe15752882'
        self.SECRET      = 'cBQ8Q~hr4uNJpUxy2Wek-gyZgJT7AxPCQXg2LctY'
        self.USERS_ID    = {
            'robotrocket1':     '46b7d39d-9f15-4dbf-b48f-d1ddbebc46e7',
            'robotrocket2':     '8da285fe-23c6-49f1-92b0-bc20f6b3a369',
            'robotrocket3':     '10e1f5cc-3cc0-4aff-9d8e-430ed3bea586',
            'hector.tejeda':    'afac103f-a2ef-42e2-b378-3a2d588b2381',
        }
        self.result     = ''
        self.emails     = []
        self.userId     = self.USERS_ID[robot]
        self.message    = ''

        self.toUserEmail    = toUserEmail
        self.asuntos         = asuntos
        self.ruta           = ruta
        self.nombreArchivo  = nombreArchivo


    def getToken(self):
        app = msal.ConfidentialClientApplication(
            client_id           = self.CLIENT_ID,
            client_credential   = self.SECRET,
            authority           = f"https://login.microsoftonline.com/{self.TENTANT_ID}",
        )

        scopes = ["https://graph.microsoft.com/.default"]
        result = None
        result = app.acquire_token_silent(scopes, account=None)

        if not result:
            result = app.acquire_token_for_client(scopes=scopes)
        self.result = result


    def sendEmail(self):
        if "access_token" in self.result:
            endpoint    = f'https://graph.microsoft.com/v1.0/users/{self.userId}/sendMail'
            email_msg   = {
                'Message': {
                    'Subject': "Test Sending Email from Python",
                    'Body': {
                        'ContentType': 'Text', 
                        'Content': "This is a test email."
                    },
                    'ToRecipients': [
                        {
                            'EmailAddress': {
                                'Address': self.toUserEmail
                            }
                        }
                    ]
                },
                'SaveToSentItems': 'true'
            }
            r = requests.post(
                endpoint,
                headers = {
                    'Authorization': 'Bearer ' + self.result['access_token']}, 
                    json = email_msg,
            )
            if r.ok:
                print('Sent email successfully')
            else:
                print('Error al enviar correo: ', r.json())
        else:
            print('error', self.result.get("error"))
            print('error_description', self.result.get("error_description"))
            print('correlation_id', self.result.get("correlation_id"))


    def getEmails(self):
        for asunto in self.asuntos:
            url     = f"https://graph.microsoft.com/v1.0/users/{self.userId}/messages?$filter= contains(subject, '{asunto}') and isRead eq false and hasAttachments eq true"
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.result['access_token'], 
            }
            response    = requests.request("GET", url, headers=headers, data=payload)
            response    = response.json()
            self.emails += response['value']


    def downloadAttachments(self, *args):
        url     = f"https://graph.microsoft.com/v1.0/users/{self.userId}/messages/{self.message}/attachments"
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + self.result['access_token'],
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        for attachment in response['value']:
            self.nombreArchivo = ""
            print(attachment['name'])
            if attachment['@odata.mediaContentType'] == 'image/png':
                continue
            contentBytes    = attachment['contentBytes']
            if self.nombreArchivo:
                name = self.nombreArchivo
            else:
                name                = attachment['name']
                self.nombreArchivo  = name
            
            print('Descargando archivos 💡')
            # DECODIFICAR DATA DEL ARCHIVO
            decoded = base64.b64decode(contentBytes)
            # CREAR ARCHIVO
            fileXlsx = open(f'{self.ruta}/{name}', 'wb')
            fileXlsx.write(decoded)
            fileXlsx.close()
            print(f'Achivo {name} descargado✅')
            sleep(5)


    def readEmail(self):
        url     = f"https://graph.microsoft.com/v1.0/users/{self.userId}/messages/{self.message}"
        payload = json.dumps({
            "isRead": True
        })
        headers = {
            'Authorization': 'Bearer ' + self.result['access_token'],
            'Content-Type': 'application/json'
        }
        response = requests.request("PATCH", url, headers=headers, data=payload)
        print(response)


    def downloadReadEmails(self, *args):
        contador = 1
        while True:
            print('CONTADOR: ', contador)
            # OBTENER TOKEN
            self.getToken()
            # BUSCAR CORREOS POR EL ASUNTO
            self.emails = []
            self.getEmails()
            if len(self.emails) == 0:
                break
            # DESCARGAR ARCHIVOS DEL CORREO
            for email in self.emails:
                self.message = email['id']
                self.downloadAttachments(args)
                self.readEmail()
            contador += 1