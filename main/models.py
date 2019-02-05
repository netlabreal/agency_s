from django.db import models

import os
from sobstvennik.settings import BASE_DIR


class News(models.Model):
    name = models.CharField(max_length=100)
    foto = models.ImageField(null=True, blank=True)
    txt = models.TextField()
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Новости'

    @property
    def get_url(self):
        if self.id:
            return "%s" % (self.id, )


class Types(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Типы'


class Typ(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Типы объектов"
        ordering = ['name']


class Rayon(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Районы"
        ordering = ['name']


class Agent(models.Model):
    name = models.CharField(null=True, max_length=200)
    tel = models.CharField(null=True, max_length=30)
    email = models.CharField(null=True, max_length=100)
    foto = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Агенты"


class Object(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(Types, on_delete=models.SET_NULL, null=True)
    typ = models.ForeignKey(Typ, on_delete=models.SET_NULL, null=True)
    rayon = models.ForeignKey(Rayon, on_delete=models.SET_NULL, null=True)
    adres = models.CharField(null=True, max_length=255)
    komnat = models.IntegerField(null=True)
    floor = models.IntegerField(null=True)
    floors = models.IntegerField(null=True)
    s = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    cost = models.DecimalField(null=True, max_digits=16, decimal_places=2)
    mainimage = models.CharField(max_length=150, blank=True)
    opisanie = models.TextField(blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True)
    shirota = models.DecimalField(null=True, max_digits=13, decimal_places=10, blank=True, default=0)
    dolgota = models.DecimalField(null=True, max_digits=13, decimal_places=10, blank=True, default=0)
    date_n = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    s_number = models.CharField(max_length=100, null=True)
    s_ssilka = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    @property
    def main_img(self):
        if self.mainimage:
            return "/media/foto/%s/%s" % (self.id, self.mainimage)

    @property
    def get_images(self):
        r = []
        #j = "%s\media\foto\%s" % (BASE_DIR, self.id, )
        for file in os.listdir("%s/media/foto/%s" % (BASE_DIR, self.id, )):
            r.append("/media/foto/%s/%s" % (self.id, file))
        return r

    class Meta:
        ordering = ['date_n']
        verbose_name_plural = "Объекты"
