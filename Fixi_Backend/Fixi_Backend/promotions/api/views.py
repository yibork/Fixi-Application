from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import UserPromoCode
from .serializers import UserPromoCodeSerializer
# from ..permissions.promocode import *
from django.db.models import Max
from django.utils import timezone
from django.db.models import Q


from rest_framework.generics import ListAPIView


class UserPromoCodeListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPromoCodeSerializer

    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()
        
        # Filter promo codes based on validity and the latest creation date
        last_created_at_date = UserPromoCode.objects.filter(user=user).aggregate(Max('created_at'))['created_at__max']
        queryset = UserPromoCode.objects.filter(
            user=user,
            promo_code__end_date__gte=today,
            created_at=last_created_at_date
        )
        
        # Flag promo codes that are not valid
        invalid_promo_codes = queryset.exclude(
            Q(promo_code__start_date__lte=today) | Q(promo_code__end_date__gte=today)
        )
        queryset = queryset.exclude(
            Q(promo_code__start_date__gt=today) | Q(promo_code__end_date__lt=today)
        )
        print(queryset)
        print(invalid_promo_codes)
        # invalid_promo_codes.update(is_valid=False)
        
        return queryset