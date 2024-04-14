# IMPORTACIONES PARA ENVIAR EMAIL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from config import settings

"""
    >> Desarrollador: Johan Esteban Sabogal <canoas430@gmail.com>
    >> Derechos: Todos los derechos reservados. EMCALI 2023.
"""

class GenericFunctions:
    """
        Funcion generica de envio de correo electronico
    """
    def send_email(self, content_json):
        data = {}
        try:
            # URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER,
                            settings.EMAIL_HOST_PASSWORD)
            # ============> NORMALMENTE ES EL CAMPO EMAIL QUIEN HACE ESTA PARTE, PERO EN ESTE CASO EL USERNAME ES EL EMAIL
            email_to = content_json["username"]
            mensaje = MIMEMultipart()
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = content_json["subject"]
            content = render_to_string(content_json["html"], content_json)
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
            data["type"] = "success"
            data["msg"] = "Se envio el correo"
        except Exception as e:
            data["msg"] = str(e)
            data["type"] ="error"
        return data
