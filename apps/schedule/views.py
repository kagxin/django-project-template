from apps.utils.view.viewsets import ModelViewSet
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework import serializers


class CrontabScheduleSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        schedule, _ = CrontabSchedule.objects.get_or_create(**validated_data)
        return schedule

    class Meta:
        model = CrontabSchedule
        exclude = ['timezone', ]


class CreateScheduleTask(ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CrontabScheduleSerializer
    queryset = CrontabSchedule.objects.all()

    def perform_create(self, serializer):
        """
        生成一个新的定时任务就是新建一条PeriodicTask记录，
        修改settings timezone 重新执行
        >>> from django_celery_beat.models import PeriodicTasks
        >>> PeriodicTasks.changed()
        参考文档 https://django-celery-beat.readthedocs.io/en/latest/
        :param serializer:
        :return:
        """
        schedule = serializer.save()
        import uuid
        PeriodicTask.objects.create(
            crontab=schedule,
            name=uuid.uuid1().__str__(),
            task='apps.schedule.tasks.add',
        )


"""
post
{
    "minute": "*",
    "hour": 3,
    "day_of_week": "*",
    "day_of_month": "*",
    "month_of_year": "*"
}
"""
