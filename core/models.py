from django.db import models


class Career(models.Model):
    
    class Meta:
        verbose_name= "Cicle"
        verbose_name_plural = "Cicles"
    name = models.CharField("Nom",max_length=200)
    code = models.CharField("codi",max_length=20)
    desc = models.TextField("descripció",blank=True,null=True)
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


