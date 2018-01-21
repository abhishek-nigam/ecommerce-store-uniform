from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..models import Category
from ..forms import CategoryForm


@permission_required('store.can_maintain_categories')
def manage_category_list(request):
    category_queryset = Category.objects.all()
    data = {}

    if request.GET.get('query', False):
        category_queryset = category_queryset.filter(name__icontains=request.GET['query'])
        data['query'] = request.GET.get('query', False)
    
    data['categories'] = category_queryset

    return render(request, 'store/manage/manage_category_list.html', data)


@permission_required('store.can_maintain_categories')
def manage_category_add(request):
    if request.method == 'POST':

        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('manage-category-list'))
    
    else:
        form = CategoryForm()
    
    return render(request, 'store/manage/manage_category_form.html', {
        'title_message': 'Add new category',
        'submit_message': 'Add',
        'form': form
    })


@permission_required('store.can_maintain_categories')
def manage_category_update(request,pk):
    
    category_object = get_object_or_404(Category, category_id=pk)

    if request.method == 'POST':

        form = CategoryForm(request.POST, instance=category_object)
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('manage-category-list'))
    
    else:
        form = CategoryForm(instance=category_object)
    
    return render(request, 'store/manage/manage_category_form.html', {
        'title_message': 'Update category',
        'submit_message': 'Update',
        'form': form
    })


@permission_required('store.can_delete_categories')
def manage_category_delete(request,pk):

    category_object = get_object_or_404(Category, category_id=pk)
    category_object.delete()

    return HttpResponseRedirect(reverse('manage-category-list'))