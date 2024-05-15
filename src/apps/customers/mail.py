from django.core.mail import send_mail

from django.conf import settings

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_reset_password_email(email, token):
    subject = 'Password Reset'
    

    html_content = f"""
    <html>
        <body>
            <h1>Reset Your Password</h1>
            Dear Customer, <br>
            Here is the token to reset your password: <strong>{token}</strong>
        </body>
    </html>
    """

    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email":f"{email}","name":f"{email}"}],
        html_content=html_content,
        sender={"name":"Hefny","email": settings.DEFAULT_FROM_EMAIL},
        subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
