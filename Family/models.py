from django.db import models
from django.utils import timezone


class FamilyNode(models.Model):
    title = models.CharField(max_length=90)
    type = models.CharField(max_length=10)
    stDate = models.DateField(default=timezone.now, null=True, blank=True)
    enDate = models.DateField(default=timezone.now, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'People'
    def __str__(self):
        return "{} {} {}".format(self.title, self.type, self.id)

class Relation(models.Model):
    person1 = models.ForeignKey(FamilyNode, on_delete=models.CASCADE, related_name='personHigher')
    person2 = models.ForeignKey(FamilyNode, on_delete=models.CASCADE, related_name='personLower')
    type = models.CharField(max_length=25)
    def __str__(self):
        return "{} ({}) {}".format(self.person1, self.type, self.person2)

class InformationAbstract(models.Model):
    person = models.ForeignKey(FamilyNode, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=50)

    class Meta:
        abstract = True

class InformationText(InformationAbstract):
    data = models.TextField()