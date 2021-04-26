from django.db import models
from enum import Enum


class Term(models.Model):
    class Meta:
        verbose_name = "Curs"
    name = models.CharField("nom", max_length=200)
    desc = models.TextField(
        "descripció", max_length=300, blank=True, null=True)
    start = models.DateField("data inici", null=False)
    end = models.DateField("data finalització", null=True, default=None)
    active = models.BooleanField("és actiu", null=False)


class Career(models.Model):
    class Meta:
        verbose_name = "Cicle"
        verbose_name_plural = "Cicles"
    name = models.CharField("nom", max_length=200)
    code = models.CharField("codi", max_length=20)
    desc = models.TextField(
        "descripció", max_length=300, blank=True, null=True)
    hours = models.IntegerField("duracio", null=False)
    start = models.DateField("data inici", null=False)
    end = models.DateField("data finalització", null=True, default=None)
    active = models.BooleanField("és actiu", null=False)
    # theres's no on_update method
    mp = models.ForeignKey(Term, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

class MP(models.Model):
    class Meta:
        verbose_name_plural = "MPs"
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    desc = models.TextField(blank=True,null=True)
    career = models.ForeignKey(Career,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class UF(models.Model):
    class Meta:
        verbose_name_plural = "UFs"
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    desc = models.TextField(blank=True,null=True)
    mp = models.ForeignKey(MP,on_delete=models.CASCADE)
    def __str__(self):
        return self.name


