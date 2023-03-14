import os.path
import smtplib
import datetime
from io import open
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def correoEnvioArchivo(asunto, body, correos, archivos):
    fecha       = (str(datetime.datetime.today()).replace(" ", "-").replace(":", "-")).split("-")
    fechaHora   = f'{fecha[2]}-{fecha[1]}-{fecha[0]} {fecha[3]}:{fecha[4]}'
    mensaje     = f"""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Correo Bendi</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        </head>
        <body style="margin: 0; padding: 0;">
        {body}
        </body>
    </html>
    """
    asunto          = f'{asunto} {fechaHora}'
    fromaddr        = "robotrocket1@cencosud.cl"
    to              = correos["to"]
    cc              = correos["cc"]
    bcc             = correos["bcc"]
    toaddr          = to
    toaddrs         = toaddr + cc + bcc
    toaddr          = ",".join(toaddr)
    cc              = ",".join(cc)
    msg             = MIMEMultipart()
    msg['From']     = fromaddr
    msg['cc']       = cc
    msg['To']       = toaddr
    msg['Subject']  = asunto
    body            = mensaje
    msg.attach(MIMEText(body, 'html'))
    for archivo in archivos:
        estado = os.path.isfile(archivo['ruta'])
        if estado == True:
            archivo['estado'] = True
        else:
            archivo['estado'] = False
    # print(archivos)
    id = 0
    for archivo in archivos:
        if archivo['estado'] == True:
            with open(archivo['ruta'], 'rb') as f:
                # set attachment mime and file name, the image type is png
                mime = MIMEBase(archivo['tipo_archivo'], archivo['formato_archivo'], filename=archivo['nombre_archivo'])
                # add required header data:
                mime.add_header('Content-Disposition', 'attachment', filename=archivo['nombre_archivo'])
                mime.add_header('X-Attachment-Id', str(id))
                mime.add_header('Content-ID', '<'+str(id)+'>')
                # read attachment file content into the MIMEBase object
                mime.set_payload(f.read())
                # encode with base64
                encoders.encode_base64(mime)
                # add MIMEBase object to MIMEMultipart object
                msg.attach(mime)
        id = id + 1
    # creates SMTP session
    s = smtplib.SMTP('SMTP.Office365.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(fromaddr, "Q1w2e3r4")
    # Converts the Multipart msg into a string
    text = msg.as_string()
    # sending the mail
    s.sendmail(fromaddr, toaddrs, text)
    # terminating the session
    s.quit()