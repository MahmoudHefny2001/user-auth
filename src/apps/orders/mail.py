from django.conf import settings

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


from celery import shared_task

from .models import OrderItem


@shared_task()
def send_merchant_order_email(order):

    order_items = OrderItem.objects.filter(order=order)

    # get all different merchants in the order
    merchants = set([order_item.product.merchant for order_item in order_items])

    total_price = None

    subject = 'New Order'

    if len(merchants) == 1 or len(merchants) == 0:
        merchant = merchants.pop()
        merchant_email = merchant.email
        
        total_price = order.total_price
        
        html_content = f"""
        <html>
            <body>
                <h1>New Order</h1>
                Dear Merchant,<br>
                You have a new order with the following details: <br>
                Order ID: <strong>{order.id}</strong><br>
                Total Price: <strong>{total_price}</strong>
                Shipping Address: <strong>{order.shipping_address}</strong>
                Thank you for using our platform!
                <p>
                Best, <strong> Mahmoud Hefny </strong> <br>
                </p>
                
            </body>
        </html>
        """

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email":f"{merchant_email}","name":f"{merchant}"}],
            html_content=html_content,
            sender={"name":"Hefny","email": settings.DEFAULT_FROM_EMAIL},
            subject=subject
        )

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

        return 
    

    # send email to each merchant
    for merchant in merchants:

        merchant_email = merchant.email

        total_price = sum([order_item.sub_total_price for order_item in OrderItem.objects.filter(order=order, product__merchant=merchant)])
        
        html_content = f"""
        <html>
            <body>
                <h1>New Order</h1>
                Dear Merchant,<br>
                You have a new order with the following details: <br>
                Order ID: <strong>{order.id}</strong><br>
                Total Price: <strong>{total_price}</strong><br>
                Shipping Address: <strong>{order.shipping_address}</strong>
                Thank you for using our platform!
                <p>
                Best, <strong> Mahmoud Hefny </strong> <br>
                </p>
            </body>
        </html>
        """

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email":f"{merchant_email}","name":f"{merchant}"}],
            html_content=html_content,
            sender={"name":"Hefny","email": settings.DEFAULT_FROM_EMAIL},
            subject=subject
        )

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


    


@shared_task()
def send_customer_order_email(order):
    subject = 'Order Confirmation'
    
    customer = order.customer

    
    total_price = order.total_price

    html_content = f"""
    <html>
        <body>
            <h1>Order Confirmation</h1>
            Dear Customer, {customer.full_name}<br>
            Your order has been confirmed with the following details: <br>
            Order ID: <strong>{customer.id}</strong><br>
            Total Price: <strong>{total_price}</strong>

            Shipping Address: <strong>{order.shipping_address}</strong>
            
            <h5>Thank you for shopping with us!</h5>
            <p>
                Best, <strong> Mahmoud Hefny </strong> <br>
            </p>
        </body>

    </html>
    """

    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email":f"{customer.email}","name":f"{customer.full_name}"}],
        html_content=html_content,
        sender={"name":"Hefny","email": settings.DEFAULT_FROM_EMAIL},
        subject=subject
    )


    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
