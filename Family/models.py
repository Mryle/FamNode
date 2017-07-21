from django.db import models
from django.utils import timezone


class Person(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=30)
    man = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = 'People'
    def __str__(self):
        return "{} {}".format(self.name, self.surname)

class Relation(models.Model):
    person1 = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='personHigher')
    person2 = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='personLower')
    type = models.CharField(max_length=25)
    def __str__(self):
        return "{} ({}) {}".format(self.person1, self.type, self.person2)

class InformationAbstract(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=50)

    class Meta:
        abstract = True

class InformationText(InformationAbstract):
    data = models.TextField()