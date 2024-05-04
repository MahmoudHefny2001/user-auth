from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import ProductReview
from .serializers import ProductReviewSerializer

from rest_framework.exceptions import PermissionDenied
from django.http import Http404

from apps.users.customJWT import CustomJWTAuthenticationClass


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    authentication_classes = [CustomJWTAuthenticationClass, JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [filters.SearchFilter]

    http_method_names = ["post", "get", "patch", "put", "delete"]

    # search_fields = ["rating", "review", "product__name", "customer__full_name"]


    def get_queryset(self):
        # if the customer trying to get a reivew that it's not his, return 404

        """
        Here we are overriding the get_queryset method to filter the reviews
        to only the ones that belong to the customer making the request
        """

        if self.action == "retrieve":
            review = ProductReview.objects.get(id=self.kwargs.get("pk"))
            if review.customer != self.request.user.customer:
                raise PermissionDenied(detail="You are not allowed to view this review", code=403)
                
            return ProductReview.objects.filter(customer=self.request.user.customer)

        # handle the case where the customer is anonymous
        if not self.request.user.is_authenticated:
            return ProductReview.objects.none()
        
        return ProductReview.objects.filter(customer=self.request.user.customer)



    def list(self, request, *args, **kwargs):
        """
        Here we are overriding the list method to filter the reviews
        to only the ones that belong to the customer making the request
        """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    
    def create(self, request, *args, **kwargs):
        """
        When creating a review, we want to make sure that the customer has not reviewed the product before
        we get the product_id from the request data and the customer from the request user
        the customer is gotten from the request user because we are using JWT authentication
        the review is optional, so we get it from the request data and set it to None if it's not provided
        rating is required, so we get it from the request data
        then we create the review object and return it
        """

        review = request.data.get("review", None)
        rating = request.data.get("rating",)
        product_id = request.data.get("product_id",)
        customer = request.user.customer

        if product_id is None or product_id == '':
            return Response({
                "Product ID is required for the review"
            },
            status = 400
            )

        if ProductReview.objects.filter(product_id=product_id, customer=customer).exists():
            return Response({"message": "You have already reviewed this product"}, status=400)
        
        # Create the review object
        review = ProductReview.objects.create(
            product_id=product_id,
            customer=customer,
            rating=rating,
            review=review,
        )

        return Response(ProductReviewSerializer(review).data, status=201)
    

    def get_object(self):
        """
        Here we are overriding the get_object method to make sure that the customer
        making the request is the owner of the review
        """
        return ProductReview.objects.get(id=self.kwargs.get("pk")) 


    def update(self, request, *args, **kwargs):
        """
        When updating a review, we want to make sure that the customer making the request is the owner of the review
        we get the review object and check if the customer is the owner of the review
        if not, we raise a permission denied exception
        if the customer is the owner of the review, we get the new rating and review from the request data
        then we update the review object and return it
        """

        product_review_object = self.get_object()
        if product_review_object.customer != request.user.customer:
            raise PermissionDenied(detail="You are not allowed to update this review", code=403)
        
        new_rating = request.data.get("rating",)
        new_review = request.data.get("review", None)
        product_review_object = ProductReview.objects.get(id=self.kwargs.get("pk"))
        
        if new_rating is not None:
            product_review_object.rating = new_rating
        
        if new_review is not None:
            product_review_object.review = new_review

        product_review_object.save()
        return Response(ProductReviewSerializer(product_review_object).data, status=200)
    


    def partial_update(self, request, *args, **kwargs):

        """
        When updating a review, we want to make sure that the customer making the request is the owner of the review
        we get the review object and check if the customer is the owner of the review
        if not, we raise a permission denied exception
        if the customer is the owner of the review, we get the new rating and review from the request data
        then we update the review object and return it
        """

        product_review_object = self.get_object()
        if product_review_object.customer != request.user.customer:
            raise PermissionDenied(detail="You are not allowed to update this review", code=403)
        
        new_rating = request.data.get("rating",)
        new_review = request.data.get("review", None)
        product_review_object = ProductReview.objects.get(id=self.kwargs.get("pk"))
        
        if new_rating is not None:
            product_review_object.rating = new_rating
        
        if new_review is not None:
            product_review_object.review = new_review
        product_review_object.save()
        return Response(ProductReviewSerializer(product_review_object).data, status=200)



    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=200)
        except ProductReview.DoesNotExist:
            raise Http404("Review not found")

    

    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"message": "Review deleted successfully"},
                status=204
            )
        except ProductReview.DoesNotExist:
            raise Http404("Review not found")

    def perform_destroy(self, instance):
        instance.delete()


    