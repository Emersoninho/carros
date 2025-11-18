from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField('Modelo', max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='car_brand', verbose_name='Marca')
    factory_year = models.IntegerField('Ano de Fabricação', blank=True, null=True)
    model_year = models.IntegerField('Ano do Modelo', blank=True, null=True)
    plate = models.CharField('Placa', max_length=10, blank=True, null=True)
    value = models.FloatField('Valor (R$)', blank=True, null=True)
    photo = models.ImageField('Foto do Carro', upload_to='cars/', blank=True, null=True)
    bio = models.TextField('Descrição', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Proprietário', null=True, blank=True)

    def __str__(self):
        return self.model
    
class CarInventory(models.Model):
    cars_count = models.IntegerField('Quantidade do Estoque')
    cars_value = models.FloatField('Valor do Estoque')
    created_at = models.DateTimeField('Data e Horário da Criação', auto_now_add=True)    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.cars_count} - {self.cars_value}'    