from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    sid = models.CharField(max_length=8, verbose_name='学号', primary_key=True, default="18301030")
    # iid = models.CharField(max_length=18, verbose_name='身份证号', default='000000000000000000')

    def __str__(self):
        return self.name
