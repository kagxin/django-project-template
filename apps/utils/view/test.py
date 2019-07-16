from __future__ import absolute_import, unicode_literals
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from apps.utils.view.viewsets import ModelViewSet
from apps.utils.view import generics
from rest_framework import serializers
from django.http import Http404


class TestModel:

    def __init__(self, id=None, name=None, age=None):
        self.id = id
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.id}, {self.name}, {self.age}"

    def __repr__(self):
        return self.__str__()

    def save(self):
        return self

    def create(self, *args, **kwargs):
        return self

    def update(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.age = kwargs['age']
        return

    def delete(self):
        return


test_data = [
    TestModel(**{
        "name":"kangxin",
        "id":1,
        "age":30
    }),
    TestModel(**{
        "name": "kangxin2",
        "id": 2,
        "age":31
    })
]
print(test_data)



class TestSerializer(serializers.Serializer):

    name = serializers.CharField()
    id = serializers.IntegerField()
    age = serializers.IntegerField()

    def create(self, validated_data):
        instance = TestModel(**validated_data)
        test_data.append(instance)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        return instance


    class Meta:
        fields = ("name", "id", "age")


print(TestSerializer(test_data, many=True).data)


class TestViewSet(ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    serializer_class = TestSerializer

    def get_queryset(self):
        queryset = test_data
        return queryset

    def get_object(self):

        try:
            return [d for d in test_data if d.id==int(self.kwargs['pk'])][0]
        except IndexError:
            raise Http404('not find.')


class TestViewSet2(generics.ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    serializer_class = TestSerializer

    def get_queryset(self):
        queryset = test_data
        return queryset

    def get_object(self):

        try:
            return [d for d in test_data if d.id==int(self.kwargs['pk'])][0]
        except IndexError:
            raise Http404('not find.')


class TestViewSet3(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    serializer_class = TestSerializer

    def get_queryset(self):
        queryset = test_data
        return queryset

    def get_object(self):

        try:
            return [d for d in test_data if d.id==int(self.kwargs['pk'])][0]
        except IndexError:
            raise Http404('not find.')




router = DefaultRouter()
#
router.register(r"test", viewset=TestViewSet, base_name="test")

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'test2/', TestViewSet2.as_view()),
    url(r'test3/(?P<pk>[0-9]+)/', TestViewSet3.as_view()),
]
"""
GET LIST /test/test/
request param
无
response data
{
    "meta": {
        "code": 0,
        "message": "ok."
    },
    "data": [
        {
            "name": "kangxin",
            "id": 1,
            "age": 30
        },
        {
            "name": "kangxin2",
            "id": 2,
            "age": 31
        }
    ]
}

POST create /test/test/
request param
{
    "name": "kangxin",
    "id": 15,
    "age": 12
}
response data
{
    "meta": {
        "code": 0,
        "message": "Created."
    },
    "data": {
        "name": "kangxin",
        "id": 15,
        "age": 12
    }
}

GET /test/test/1/
request param
无

response data
{
    "meta": {
        "code": 0,
        "message": "ok."
    },
    "data": {
        "name": "kangxin",
        "id": 1,
        "age": 30
    }
}


PUT partial_update /test/test/1/
request param
{
    "age": 80
}
response data
{
    "meta": {
        "code": 0,
        "message": "updated."
    },
    "data": {
        "name": "kangxin",
        "id": 1,
        "age": 80
    }
}

DELETE delete /test/test/1/
response data
{
    "meta": {
        "code": 0,
        "message": "deleted."
    },
    "data": {}
}
"""