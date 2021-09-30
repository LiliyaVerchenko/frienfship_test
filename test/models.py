from django.db import models
from django.utils.translation import gettext_lazy as _



class Users(models.Model):
    salary = models.IntegerField()
    name = models.CharField(max_length=255)
    date = models.DateTimeField()

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
        db_table = 'users'

    def __str__(self):
        return str(self.name)


class Houses(models.Model):
    user = models.ForeignKey('Users', verbose_name=_('Покупатель'), on_delete=models.CASCADE, related_name='house')
    adress = models.CharField(max_length=255)
    cost = models.IntegerField()

    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"
        db_table = 'houses'

    def __str__(self):
        return str(self.pk)