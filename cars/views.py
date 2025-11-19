from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarModelForm
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required # login
from django.utils.decorators import method_decorator # decorador
from django.contrib import messages

# baseada em função
# def cars_view(request):
#     cars = Car.objects.all().order_by('model')
#     search = request.GET.get('search')

#     if search:
#         cars = cars.filter(model__icontains=search)
#     return render(request, 'cars.html', {'cars': cars})

#  baseada em classes
# class CarsView(View):

#     def get(self, request):
#         cars = Car.objects.all().order_by('model')
#         search = request.GET.get('search')
#         if search:
#             cars = cars.filter(model__icontains=search)
#         return render(request, 'cars.html', {'cars': cars})  

# baseada em classes
class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        cars = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')
        if search:
            cars = cars.filter(model__icontains=search)
        return cars    

     
        
      

# baseada em função
# def new_car_view(request):
#     if request.method == 'POST':
#         new_car_form = CarModelForm(request.POST, request.FILES)
#         if new_car_form.is_valid():
#             new_car_form.save()
#             return redirect('cars_list')
#     else:
#         new_car_form = CarModelForm()
#         return render(request, 'new_car.html', {'new_car_form': new_car_form})

#  baseada em class
# class NewCarView(View):

#     def get(self, request):
#         new_car_form = CarModelForm()
#         return render(request, 'new_car.html', {'new_car_form': new_car_form})
    
#     def post(self, request):
#         new_car_form = CarModelForm(request.POST, request.FILES)
#         if new_car_form.is_valid():
#             new_car_form.save()
#             return redirect('cars_list')
#         return render(request, 'new_car.html', {'new_car_form': new_car_form})

# baseada em class
@method_decorator(login_required(login_url='login'), name='dispatch') #decorator, login 
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = reverse_lazy('cars_list')

    def form_valid(self, form):
        # Salva o dono corretamente
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        # Se NÃO for superusuário e NÃO for o dono → bloquear
        if not request.user.is_superuser and obj.owner != request.user:
            messages.error(request, "❌ Você não tem permissão para editar este carro.")
            return redirect('cars_list')

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
    # Garante que o proprietário nunca é alterado
        form.instance.owner = self.get_object().owner
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

    


@method_decorator(login_required(login_url='login'), name='dispatch') #decorator, login 
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = reverse_lazy('cars_list')

    # 🚨 Lógica de Autorização Adicionada
    # def get_queryset(self):
    #     # Chama a queryset base (todos os carros)
    #     queryset = super().get_queryset()

    #     # Permite que o superusuário veja todos os carros
    #     if self.request.user.is_superuser:
    #         return queryset
        
    #     # Para usuários normais, filtra para mostrar SÓ os carros que eles criaram (se o campo for 'owner')
    #     return queryset.filter(owner=self.request.user)
    
    # 🚨 Bloqueia usuários que tentam excluir carro que não é deles
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if (not request.user.is_superuser) and (obj.owner != request.user):
            messages.error(request, "❌ Você não tem permissão para excluir este carro.")
            return redirect('cars_list')

        return super().dispatch(request, *args, **kwargs)