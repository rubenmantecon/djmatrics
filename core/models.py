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


class ValidationState(Enum):
    P = "Pending"
    V = "Validated"
    U = "Unregistered"


class Enrolment(models.Model):
    class Meta:
        verbose_name = "Matrícula"
    dni = models.CharField("dni", max_length=9)
    state = models.CharField(max_length=20, choices=[(
        val_state, val_state.value) for val_state in ValidationState], default=None)
    birthplace = models.CharField(
        "lloc de naixement", max_length=50, null=True, default=None)
    birthday = models.DateField("data de naixement", null=True, default=None)
    address = models.CharField("adreça")
    city = models.CharField("ciutat")
    postal_code = models.CharField("codi postal")
    phone_number = models.CharField("número de telèfon", max_length=14)
    emergency_number = models.CharField("número d'emergència", max_length=14)
    tutor_1 = models.CharField(
        "nom del pare/mare o tutor/a legal", null=True, default=None)
    tutor_2 = models.CharField(
        "nom del pare/mare o tutor/a legal (2)", null=True, default=None)
    tutor_1_dni = models.CharField(
        "dni del pare/mare o tutor/a legal", max_length=9, null=True, default=None)
    tutor_2_dni = models.CharField(
        "dni del pare/mare o tutor/a legal (2)", max_length=9, null=True, default=None)
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    term_id = models.ForeignKey(Term, on_delete=models.RESTRICT)
    career_id = models.ForeignKey(Career, on_delete=models.RESTRICT)


class MP(models.Model):
    class Meta:
        verbose_name_plural = "MPs"
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    desc = models.TextField(blank=True, null=True)
    career = models.ForeignKey(Career, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UF(models.Model):
    class Meta:
        verbose_name_plural = "UFs"
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    desc = models.TextField(blank=True, null=True)
    mp = models.ForeignKey(MP, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
