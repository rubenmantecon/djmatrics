from django.db import models
from enum import Enum
import django.utils.timezone as timezone
from django.core.files.storage import FileSystemStorage


class Term(models.Model):
    class Meta:
        verbose_name = "Curs"
        verbose_name_plural = "Cursos"
    name = models.CharField("nom", max_length=200)
    desc = models.TextField(
        "descripció", max_length=300, blank=True, null=True)
    start = models.DateField("data inici", null=False)
    end = models.DateField("data finalització", null=True, default=None)
    active = models.BooleanField("és actiu", null=False, default=False)

    def __str__(self):
        return self.name


class Career(models.Model):
    class Meta:
        verbose_name = "Cicle"
        verbose_name_plural = "Cicles"
    name = models.CharField("nom", max_length=200)
    code = models.CharField("codi", max_length=20)
    desc = models.TextField(
        "descripció", max_length=300, blank=True, null=True)
    hours = models.IntegerField("duracio", null=False, default=0)
    start = models.DateField("data inici", null=False, default=timezone.now)
    end = models.DateField("data finalització", null=True, default=None)
    active = models.BooleanField("és actiu", null=False, default=None)
    term_id = models.ForeignKey(Term, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class ValidationState(Enum):
    P = "Pending"
    V = "Validated"
    U = "Unregistered"


class Enrolment(models.Model):
    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matricules"

    dni = models.CharField("dni", max_length=9)
    state = models.CharField(max_length=20, choices=[(
        val_state, val_state.value) for val_state in ValidationState], default=None)
    birthplace = models.CharField(
        "lloc de naixement", max_length=50, null=True, default=None)
    birthday = models.DateField("data de naixement", null=True, default=None)
    address = models.CharField("adreça", max_length=255)
    city = models.CharField("ciutat", max_length=150)
    postal_code = models.CharField("codi postal", max_length=5)
    phone_number = models.CharField("número de telèfon", max_length=14)
    emergency_number = models.CharField("número d'emergència", max_length=14)
    tutor_1 = models.CharField(
        "nom del pare/mare o tutor/a legal", max_length=50, null=True, default=None)
    tutor_2 = models.CharField(
        "nom del pare/mare o tutor/a legal (2)", max_length=50, null=True, default=None)
    tutor_1_dni = models.CharField(
        "dni del pare/mare o tutor/a legal", max_length=9, null=True, default=None)
    tutor_2_dni = models.CharField(
        "dni del pare/mare o tutor/a legal (2)", max_length=9, null=True, default=None)
    # user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    term_id = models.ForeignKey(Term, on_delete=models.RESTRICT)
    career_id = models.ForeignKey(Career, on_delete=models.RESTRICT)


class MP(models.Model):
    class Meta:
        verbose_name_plural = "MPs"
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    desc = models.TextField(blank=True, null=True)
    career_id = models.ForeignKey(Career, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UF(models.Model):
    class Meta:
        verbose_name_plural = "UFs"
    name = models.CharField("nom", max_length=255)
    code = models.CharField("codi", max_length=20)
    desc = models.CharField(
        "descripcio", max_length=300, blank=True, null=True)
    mp_id = models.ForeignKey(MP, on_delete=models.RESTRICT)
    active = models.BooleanField("és actiu", default=True)

    def __str__(self):
        return self.name


class EnrolmentUF(models.Model):
    uf_id = models.ForeignKey(UF, on_delete=models.RESTRICT)
    enrolment_id = models.ForeignKey(Enrolment, on_delete=models.RESTRICT)


class ProfileRequirement(models.Model):
    class Meta:
        verbose_name = "Perfil de requeriments"
        verbose_name_plural = "Perfils de requeriment"
    name = models.CharField("nom", max_length=50)
    description = models.TextField("descripció", null=True)


class Record(models.Model):
    # user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    uf_id = models.ForeignKey(UF, on_delete=models.RESTRICT)


class Req_EnrolState(Enum):
    P = "Pending"
    V = "Validated"
    R = "Rejected"
    E = "Empty"


class Requirement(models.Model):
    verbose_name = "Requeriment"
    verbose_name_plural = "Requeriments"
    class Meta:
        verbose_name = "Requeriment"
    profile_id = models.ForeignKey(
        ProfileRequirement, on_delete=models.RESTRICT)
    name = models.CharField("nom", max_length=255)

    def __str__(self):
        return self.name


class Req_enrol(models.Model):
    class Meta:
        verbose_name = "Requeriments matricula"
        verbose_name_plural = "Requeriments matricula"
    requirement_id = models.ForeignKey(Requirement, on_delete=models.RESTRICT)
    enrolment_id = models.ForeignKey(Enrolment, on_delete=models.RESTRICT)
    state = models.CharField(max_length=20, choices=[(
        val_state, val_state.value) for val_state in Req_EnrolState], default=None)


fs = FileSystemStorage(location='')


class Upload(models.Model):
    class Meta:
        verbose_name = "Pujades"
        verbose_name_plural = "Pujades"
    data = models.FileField(storage=fs, null=True)
    req_enrol_id = models.ForeignKey(Req_enrol, on_delete=models.RESTRICT)
