import uuid
from django.conf import settings
from django.utils import timezone
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from Fixi_Backend.core.models import AbstractBaseModel
from django.core.exceptions import ValidationError
from ..reviews.models import Review

# from yanvision_ecommerce.courses.models import Course, UserCourseEnrollement

User = get_user_model()


class Order(AbstractBaseModel):
    @staticmethod
    def generate_order_number():
        # UUIDs are universally unique, and we take the hex to get a nice string.
        order_number = uuid.uuid4().hex.upper()
        try:
            Order.objects.get(order_number=order_number)
            return Order.generate_order_number()
        except Order.DoesNotExist:
            return order_number

    class OrderStatusChoices(models.TextChoices):
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        CANCELED = "canceled", _("Canceled")
        REFUNDED = "refunded", _("Refunded")

    class PaymentMethodChoices(models.TextChoices):
        CREDIT_CARD = "CC", _("Credit Card")
        PAYPAL = "PP", _("PayPal")
        BANK_TRANSFER = "BT", _("Bank Transfer")

    order_number = models.CharField(
        _("Order Number"),
        max_length=32,  # UUID is 32 chars
        unique=True,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        related_name="orders",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    promo_code = models.ForeignKey(
        "promotions.PromoCode",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Promo code"),
    )
    payment_method = models.CharField(
        _("Payment method"),
        max_length=2,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.CREDIT_CARD,
    )
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
    )
    total_amount = models.DecimalField(
        _("Total amount"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    billing_address = models.TextField(_("Billing Address"))
    billing_country = CountryField(blank_label=_("(Select country)"))
    paid_at = models.DateTimeField(_("Paid at"), null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_number} - Status: {self.get_status_display()}"

    def get_metadata(self):
        # Required for stripe payment
        return {}

    def get_order_items(self):
        return self.order_items.all()

    # def create_course_enrollment(self, for_company: bool):
    #     # TODO: Implement company enrollment
    #     course_content_type = ContentType.objects.get_for_model(
    #         Course
    #     )

    #     for order_item in self.order_items.all():

    #         if order_item.content_type == course_content_type:
    #             course = order_item.item

    #             UserCourseEnrollement.objects.create(
    #                 user=self.user,
    #                 course=course
    #             )

    # Should be called in admin when he creates order for company manually
    def mark_paid_for_company(self):
        self.status = self.OrderStatusChoices.PAID
        self.paid_at = timezone.now()
        self.save()
        self.create_course_enrollment(for_company=True)

    # called on success url in payment hook
    def mark_paid_for_user(self):
        self.status = self.OrderStatusChoices.PAID
        self.paid_at = timezone.now()
        self.save()
        self.create_course_enrollment(for_company=False)

    def mark_canceled(self):
        self.status = self.OrderStatusChoices.CANCELED
        self.save()

    def mark_refunded(self):
        self.status = self.OrderStatusChoices.REFUNDED
        self.save()

    @staticmethod
    @transaction.atomic  # Ensures the operation is atomic
    def create_order_from_basket(basket):
        # TODO: implement payment method
        order = Order.objects.create(
            order_number=Order.generate_order_number(),
            user=basket.user,
            promo_code=basket.promo_code,
            status=Order.OrderStatusChoices.PENDING,
            total_amount=basket.total_price(),
            # billing_address=basket.user.profile.billing_address, # TODO: Implement billing address; probably on user profile + checkout
            billing_country=basket.country,  # TODO: Implement billing address; probably on user profile + checkout
        )

        for basket_item in basket.items.all():
            OrderItem.objects.create(
                order=order,
                content_type=basket_item.content_type,
                content_id=basket_item.content_id,
                item=basket_item.item,
                quantity=basket_item.quantity,
                price=basket_item.item.get_price(),
            )

        # Clear the basket
        basket.clear_basket()

        return order


class OrderItem(AbstractBaseModel):
    class OrderItemStatusChoices(models.TextChoices):
        PLACED = "placed", _("Placed")
        PROCESSING = "processing", _("Processing")
        SHIPPED = "shipped", _("Shipped")
        DELIVERED = "delivered", _("Delivered")

    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=100, null=True, choices=OrderItemStatusChoices.choices, default=OrderItemStatusChoices.PLACED)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "content_id")
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    date_delivered = models.DateTimeField(_("Date delivered"), null=True, blank=True)
    date_refunded = models.DateTimeField(_("Date refunded"), null=True, blank=True)

    def total_price(self):
        return self.price * self.quantity
    
    def get_review(self):
        """
        check if content_type is product or variant
        """
        if self.content_type.model == "product":
            return Review.objects.filter(product=self.item, user=self.order.user).first()
        else:
            return Review.objects.filter(product=self.item.product, user=self.order.user).first()
        
    # def get_image(self):
    #     """
    #     check if content_type is product or variant
    #     """
    #     if self.content_type.model == "product":
    #         return self.item.get_image()
    #     else:
    #         return self.item.product.get_image()

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            raise ValidationError(_("Invalid quantity."))

        # Validate if the item (product) exists
        if not self.item:
            raise ValidationError(
                _("Product associated with the basket item does not exist.")
            )

        valid_content_types = []

        for product_model in settings.PRODUCT_MODELS:
            app_label, model_name = product_model.split(".")
            content_type = ContentType.objects.get(
                app_label=app_label, model=model_name.lower()
            )
            valid_content_types.append(content_type)

        if self.content_type not in valid_content_types:
            raise ValidationError(_("Invalid product type."))

        super().save(*args, **kwargs)
