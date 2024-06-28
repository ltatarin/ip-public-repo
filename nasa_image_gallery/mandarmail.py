from email.message import EmailMessage
import ssl
import smtplib
def MandarMail(emailrecibido):
    password = "kzph fpqi uixv xgal"
    email_sender = "maildepruebaip653@gmail.com"
    email_reciver = emailrecibido
    subject = "Verificación de cuenta"
    body = "Usted ha creado una cuenta para la galería de la nasa"
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_reciver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
        smtp.login(email_sender,password)
        smtp.sendmail(email_sender,email_reciver,em.as_string())