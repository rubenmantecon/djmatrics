from django.db import models
import django.utils.timezone as timezone
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User


class Term(models.Model):
    class Meta:
        verbose_name = "Curs"
        verbose_name_plural = "Cursos"
    name = models.CharField("nom", max_length=200)
    desc = models.TextField(
        "descripció", max_length=255, blank=True, null=True)
    start = models.DateField("data inici", null=False)
    end = models.DateField("data finalització", null=True, default=None)
    active = models.BooleanField("és actiu", default=False)

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
    active = models.BooleanField("és actiu", default=False)
    term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


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
    CHOICES = (
        ('1', '1r'),
        ('2', '2n'),
    )
    name = models.CharField("nom", max_length=255)
    code = models.CharField("codi", max_length=20)
    course = models.CharField(
        "primer o segon", max_length=20, choices=CHOICES, default=None, null=True)
    desc = models.CharField(
        "descripcio", max_length=300, blank=True, null=True)
    price = models.IntegerField("preu", default=25)
    mp = models.ForeignKey(MP, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField("és actiu", default=True)

    def __str__(self):
        return "{} - {}".format(self.mp.name[:4],self.name)


class ProfileRequirement(models.Model):
    class Meta:
        verbose_name = "Perfil de requeriments"
        verbose_name_plural = "Perfils de requeriment"
    CHOICES = (
        ('EX', 'Exempció'),
        ('BO', 'Bonificació'),
        ('MA', 'Obligatori')
    )

    name = models.CharField("nom", max_length=255)
    description = models.TextField("descripció", null=True)
    profile_type = models.CharField(
        'tipus', max_length=20, choices=CHOICES, default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class Enrolment(models.Model):
    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matricules"

    CHOICES = (
        ('P', 'Pendent'),
        ('V', 'Validat'),
        ('R', 'Rebutjat'),
    )
    ID_TYPES = (
        ('DNI','DNI'),
        ('NIE','NIE'),
        ('PASS','Passaport'),
    )
    user = models.ForeignKey( User, on_delete=models.SET_NULL,
                                null=True, blank=True)
    # dades importades
    request_num = models.CharField("Número de sol·licitud", max_length=100,unique=True)
    ralc_num = models.CharField("Identificador RALC", max_length=100,
                                            null=True,blank=True,unique=True)
    first_name = models.CharField( "nom", max_length=100 )
    last_name_1 = models.CharField( "cognom 1", max_length=100 )
    last_name_2 = models.CharField( "cognom 2", max_length=100, null=True, blank=True )
    ID_num = models.CharField( "ID num", max_length=30,
                        help_text="Número del DNI, NIE o Passaport")
    ID_type = models.CharField( "tipus de doc ID", max_length=30, choices=ID_TYPES)
    tis = models.CharField( "Targeta Sanitària", max_length=20,
                            null=True, blank=True, default=None )
    birthplace = models.CharField( "lloc de naixement", 
                            max_length=50, null=True, default=None)
    birthday = models.DateField("data de naixement", null=True, default=None)
    address = models.CharField("adreça", max_length=255, null=True)
    city = models.CharField("ciutat", max_length=150, null=True)
    postal_code = models.CharField("codi postal", null=True, max_length=5)
    phone_number = models.CharField( "número de telèfon",
                            null=True, max_length=14)
    email = models.EmailField("correu", max_length=254, null=True)
    emergency_number = models.CharField( "número d'emergència",
                    null=True, blank=True, max_length=14)
    tutor_1_dni = models.CharField( "dni del pare/mare o tutor/a legal (1)",
                    max_length=30, null=True, blank=True, default=None)
    tutor_1_name = models.CharField( "nom del pare/mare o tutor/a legal (1)",
                    max_length=50, null=True, blank=True, default=None)
    tutor_1_lastname1 = models.CharField( "cognoms del pare/mare o tutor/a legal (1)",
                    max_length=50, null=True, blank=True, default=None)
    tutor_1_lastname2 = models.CharField( "cognoms del pare/mare o tutor/a legal (1)",
                    max_length=50, null=True, blank=True, default=None)
    tutor_2_dni = models.CharField( "dni del pare/mare o tutor/a legal (2)",
                    max_length=9, null=True, blank=True, default=None)
    tutor_2_name = models.CharField( "cognoms del pare/mare o tutor/a legal (2)",
                    max_length=50, null=True, blank=True, default=None)
    tutor_2_lastname1 = models.CharField( "cognoms del pare/mare o tutor/a legal (2)",
                    max_length=50, null=True, blank=True, default=None)
    tutor_2_lastname2 = models.CharField( "cognoms del pare/mare o tutor/a legal (2)",
                    max_length=50, null=True, blank=True, default=None)
    # dades creades per l'usuari
    image_rights = models.BooleanField("Drets d'imatge", null=True, blank=True)
    excursions = models.BooleanField("Salides d'excursio", null=True, blank=True)
    extracurricular = models.BooleanField("Salides extraescolars", null=True, blank=True)
    profile_req = models.ForeignKey(
        ProfileRequirement, on_delete=models.SET_NULL, null=True, blank=True)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True)
    ufs = models.ManyToManyField(UF,blank=True)
    state = models.CharField("estat de matrícula",
                                 max_length=20, choices=CHOICES, default="P")
    def llest_per_a_revisio(self):
        #return False
        req_enrols = self.req_enrol_set.all()
        pending_docs = 0    
        for req in req_enrols:
            if req.state == "R":
                # mentre hi hagi un doc invàlid (rebutjat) no es pot finalitzar
                # la matrícula. Per tant, no està per revisar encara
                return False
            elif req.state == "P":
                if req.upload_set.count() == 0:
                    # si queda algun doc sense cap càrrega encara no està llest
                    return False
                # si està pendent i amb uploads podem seguir avaluant
                pending_docs += 1
        # si hem arribat aquí és pq cap doc està rebutjat ni pendent de càrrega
        if pending_docs:
            return True
        return False
    llest_per_a_revisio.boolean = True
    def carregues(self):
        total = 0
        for req in self.req_enrol_set.all():
            total += req.upload_set.count()
        return total
    def docs_valids(self):
        if not self.profile_req or self.req_enrol_set.count()==0:
            return False
        for req in self.req_enrol_set.all():
            if req.state != "V":
                return False
        return True
    docs_valids.boolean = True        
    def docs_a_revisar(self):
        for req in self.req_enrol_set.all():
            if req.state == "P" and req.upload_set.count() > 0:
                return True
        return False
    docs_a_revisar.boolean = True
    def __str__(self):
        lastname2 = self.last_name_2 or ""
        return "{} {}, {}".format(self.last_name_1, lastname2, self.first_name)


class Record(models.Model):
    class Meta:
        verbose_name = "UF_superada"
        verbose_name_plural = "UFs_superades"

    uf = models.ForeignKey(UF, on_delete=models.SET_NULL, null=True)
    uf_name = models.CharField( max_length=80,
                                verbose_name="nom de la unitat formativa" )
    uf_code = models.CharField( max_length=12,
                                verbose_name="codi de la unitat formativa" )
    student_id = models.CharField( max_length=30,
                                verbose_name="DNI de l'estudiant")
    term = models.CharField(verbose_name="any escolar", max_length=50)
    career_code = models.CharField(
        verbose_name="codi del cicle formatiu", max_length=12)


class Requirement(models.Model):
    class Meta:
        verbose_name = "Requeriment"
    name = models.CharField("nom", max_length=255)
    description = models.TextField("descripció", null=True)
    profile = models.ForeignKey( ProfileRequirement,
                            on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name


class Req_enrol(models.Model):
    class Meta:
        verbose_name = "Requeriment matricula"
    CHOICES = (
        ('P', 'Pendent'),
        ('V', 'Validat'),
        ('R', 'Rebutjat'),
    )
    requirement = models.ForeignKey( Requirement,
                            on_delete=models.SET_NULL, null=True)
    enrolment = models.ForeignKey( Enrolment,
                            on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=20, choices=CHOICES, default=None)
    comments = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.requirement.name


class Upload(models.Model):
    class Meta:
        verbose_name = "Pujades"
        verbose_name_plural = "Pujades"
    data = models.FileField(upload_to="uploads/", null=True, blank=True)
    req_enrol = models.ForeignKey( Req_enrol,
                            on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.data.name
