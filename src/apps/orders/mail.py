from django.core.mail import send_mail

from django.conf import settings

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


def send_merchant_order_email(order, merchant):
    subject = 'New Order'
    
    html_content = f"""
    <html>
        <body>
            <h1>New Order</h1>
            Dear Merchant, {merchant.business_name} <br>
            You have a new order with the following details: <br>
            Order ID: <strong>{order.id}</strong><br>
            Total Price: <strong>{order.total_price}</strong>
        </body>
    </html>
    """

    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email":f"{merchant.email}","name":f"{merchant.business_name}"}],
        html_content=html_content,
        sender={"name":"Hefny","email": settings.DEFAULT_FROM_EMAIL},
        subject=subject
    )


    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)



def send_customer_order_email(order, customer):
    subject = 'Order Confirmation'
    
    html_content = f"""
    <html>
        <body>
            <h1>Order Confirmation</h1>
            Dear Customer, {customer.full_name}<br>
            Your order has been confirmed with the following details: <br>
            Order ID: <strong>{order.id}</strong><br>
            Total Price: <strong>{order.total_price}</strong>
        </body>
    </html>
    """

    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email":f"{customer.email}","name":f"{customer.first_name} {customer.last_name}"}],
        html_content=html_content,
        sender={"name":"Hefny","email": settings.DEFAULT_FROM_EMAIL},
        subject=subject
    )


    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        