from django import forms
from cars.models import Brand, Car

# class CarForm(forms.Form):
#     model = forms.CharField(max_length=200)
#     brand = forms.ModelChoiceField(Brand.objects.all())
#     factory_year = forms.IntegerField()
#     model_year = forms.IntegerField()
#     plate = forms.CharField(max_length=10)
#     value = forms.FloatField()
#     photo = forms.ImageField()

#     def save(self):
#         car = Car(
#             model=self.cleaned_data['model'],
#             brand=self.cleaned_data['brand'],
#             factory_year=self.cleaned_data['factory_year'],
#             model_Year=self.cleaned_data['model_year'],
#             plate=self.cleaned_data['plate'],
#             Value=self.cleaned_data['value'],
#             photo=self.cleaned_data['photo']
#         )

#         car.save()
#         return car
    
class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'brand', 'factory_year', 'model_year', 'plate', 'value', 'photo', 'bio']

    def clean_value(self):
        value = self.cleaned_data.get('value')

        # Só valida se não for None
        if value is not None and value < 20000:
            self.add_error('value', 'O valor mínimo do carro deve ser de R$ 20.000,00')

        # Retorna sempre o valor (mesmo que None)
        return value

    def clean_factory_year(self):
        factory_year = self.cleaned_data.get('factory_year')

        # Só valida se não for None
        if factory_year is not None and factory_year < 1975:
            self.add_error('factory_year', 'Não é possível cadastrar carros fabricados antes de 1975')

        return factory_year

    def clean_model_year(self):
        model_year = self.cleaned_data.get('model_year')
        return model_year

    