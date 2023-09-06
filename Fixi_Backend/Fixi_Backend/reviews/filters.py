from django.db.models import QuerySet, Q
from django_filters import rest_framework as filters
from .models import Review


class ReviewFilter(filters.FilterSet):
    category = filters.CharFilter(method="filter_by_category", label='Category')

    def filter_by_category(self, queryset: QuerySet[Review], name, value):
        categories = value.split(',')
        category_filters = Q()
        for category in categories:
            category_filters |= Q(category__value=category.strip())
        queryset = queryset.filter(category_filters)
        return queryset

    class Meta:
        model = Review
        fields = ['category']