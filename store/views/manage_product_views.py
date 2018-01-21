from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from ..models import Product
from ..forms import ProductForm

@permission_required('store.can_maintain_products')
def manage_product_list(request):
    product_queryset = Product.objects.all()
    data = {}

    if request.GET.get('query', False):
        query = request.GET.get('query', False)
        product_queryset = product_queryset.filter(
                        Q(title__icontains=query) | 
                        Q(school__name__icontains=query) |
                        Q(category__name__icontains=query)
                        )
        data['query'] = query
    
    data['products'] = product_queryset

    return render(request, 'store/manage/manage_product_list.html', data)


@permission_required('store.can_maintain_products')
def manage_product_add(request):
    if request.method == 'POST':

        form = ProductForm(request.POST)
        if form.is_valid():
            school = form.save()
            return HttpResponseRedirect(reverse('manage-product-list'))
    
    else:
        form = ProductForm()
    
    return render(request, 'store/manage/manage_product_form.html', {
        'title_message': 'Add new product',
        'submit_message': 'Add',
        'form': form
    })


@permission_required('store.can_maintain_products')
def manage_product_update(request,pk):
    
    product_object = get_object_or_404(Product, product_id=pk)

    if request.method == 'POST':

        form = ProductForm(request.POST, instance=product_object)
        if form.is_valid():
            product = form.save()
            return HttpResponseRedirect(reverse('manage-product-list'))
    
    else:
        form = ProductForm(instance=product_object)
    
    return render(request, 'store/manage/manage_product_form.html', {
        'title_message': 'Update product',
        'submit_message': 'Update',
        'form': form
    })


@permission_required('store.can_delete_products')
def manage_product_delete(request,pk):

    product_object = get_object_or_404(Product, product_id=pk)
    product_object.delete()

    return HttpResponseRedirect(reverse('manage-product-list'))