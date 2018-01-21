from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..models import ProductInstance
from ..forms import ProductInstanceForm


@permission_required('store.can_maintain_product_instances')
def manage_product_instance_list(request):
    product_instance_queryset = ProductInstance.objects.all()
    data = {}

    if request.GET.get('query', False):
        query = request.GET.get('query', False)

        product_instance_queryset = product_instance_queryset.filter(product__title__icontains=query)
        data['query'] = query
    
    data['product_instances'] = product_instance_queryset

    return render(request, 'store/manage/manage_product_instance_list.html', data)


@permission_required('store.can_maintain_product_instances')
def manage_product_instance_add(request):
    if request.method == 'POST':

        form = ProductInstanceForm(request.POST)
        if form.is_valid():
            product_instance = form.save()
            return HttpResponseRedirect(reverse('manage-product-instance-list'))
    
    else:
        form = ProductInstanceForm()
    
    return render(request, 'store/manage/manage_product_instance_form.html', {
        'title_message': 'Add new product instance',
        'submit_message': 'Add',
        'form': form
    })


@permission_required('store.can_maintain_product_instances')
def manage_product_instance_update(request,pk):
    
    product_instance_object = get_object_or_404(ProductInstance, instance_id=pk)

    if request.method == 'POST':

        form = ProductInstanceForm(request.POST, instance=product_instance_object)
        if form.is_valid():
            product_instance = form.save()
            return HttpResponseRedirect(reverse('manage-product-instance-list'))
    
    else:
        form = ProductInstanceForm(instance=product_instance_object)
    
    return render(request, 'store/manage/manage_product_instance_form.html', {
        'title_message': 'Update product instance',
        'submit_message': 'Update',
        'form': form
    })


@permission_required('store.can_delete_product_instances')
def manage_product_instance_delete(request,pk):

    product_instance_object = get_object_or_404(ProductInstance, instance_id=pk)
    product_instance_object.delete()

    return HttpResponseRedirect(reverse('manage-product-instance-list'))
