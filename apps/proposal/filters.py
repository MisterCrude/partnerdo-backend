import datetime
import re
from apps.proposal.models import Proposal
from core.consts import GENDER_CHOICES
from django_filters import rest_framework as filters
from django.db.models import Q


class ProposalFilter(filters.FilterSet):
    gender = filters.ChoiceFilter(
        choices=GENDER_CHOICES, field_name='author__gender')
    categories = filters.CharFilter(method='filter_categories')
    city = filters.CharFilter(field_name='city__id')
    city_area = filters.CharFilter(field_name='city_area__id')
    age = filters.CharFilter(method='filter_age')
    search = filters.CharFilter(method='filter_search')

    def filter_categories(self, queryset, name, value):
        category_ids = value.split(',')
        return queryset.filter(category__id__in=category_ids)

    def filter_age(self, queryset, name, value):
        age_range = value.split(',')
        current_year = datetime.datetime.now().year

        if len(age_range) == 1 and re.match('[0-9]', age_range[0]):
            birth_year = current_year - int(age_range[0])

            return queryset.filter(author__birth_year__lt=birth_year)

        if len(age_range) == 2 and re.match('[0-9]', age_range[1]) and re.match('[0-9]', age_range[0]):
            max_birth_year = current_year - int(age_range[0])
            min_birth_year = current_year - int(age_range[1])

            return queryset.filter(Q(author__birth_year__gte=min_birth_year) & Q(author__birth_year__lte=max_birth_year))

        return queryset

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))

        return queryset

    class Meta:
        model = Proposal
        fields = ['gender', 'categories', 'city', 'age', 'search']
