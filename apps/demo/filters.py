import rest_framework_filters as filters
from apps.demo.models import Article


class ProductFilter(filters.FilterSet):
    content = filters.CharFilter(method='content_filter')

    def content_filter(self, qs, name, value):
        return qs.filter(content__contains=value)

    class Meta:
        model = Article
        fields = {
            'headline': ['icontains', ],
            'pub_date': ['lte', 'gte', ],
            # 'reporter__fullname': ['icontains', ]
        }
