from rest_framework.permissions import BasePermission, SAFE_METHODS
from ..models import OrderItem, Review


class HasPurchasedTheProductAndNotReviewed(BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            user = request.user
            product_id = request.query_params.get('product')

            number_of_purchase = OrderItem.objects.filter(order__user=user, product_id=product_id).count()
            number_of_prev_reviews = Review.objects.filter(user=user, product_id=product_id).count()

            has_purchased = OrderItem.objects.filter(order__user=user, product_id=product_id).exists()

            if number_of_purchase <= number_of_prev_reviews or not has_purchased:
                self.message = 'You must have purchased the product and not reviewed it before.'
                return False

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        is_original_creator = request.user == obj.user
        return is_original_creator