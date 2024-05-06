from rest_framework.views import APIView
from rest_framework.response import Response

# from payment_app.payment import paymob_client

# class PaymentView(APIView):
    # def post(self, request):
        
        # payment_process_info = {
            # "amount": request.data.get('amount'),
            # "currency" : request.data.get('currency'),
            # "order_id" : request.data.get('order_id'),
            # "order_description": request.data.get('order_description'),
            # "customer": request.data.get('customer'),
            # "billing_data": request.data.get('billing_data'),
            # "shipping_data": request.data.get('shipping_data'),
            # "items": request.data.get('items'),
            # "shipping_method": request.data.get('shipping_method'),
            # "payment_method": request.data.get('payment_method'),
            # "payment_integration": request.data.get('payment_integration'),
            # "success_url": request.data.get('success_url'),
            # "failure_url": request.data.get('failure_url'),
            # "pending_url": request.data.get('pending_url'),
            # "error_url": request.data.get('error_url'),
            # "notification_url": request.data.get('notification_url'),
            # "merchant": request.data.get('merchant'),
        # }


        # Create a payment object
        # payment = paymob_client.Payment.create(
            # payment_process_info
        # )
        # Return the payment response
        # return Response(payment.to_dict())