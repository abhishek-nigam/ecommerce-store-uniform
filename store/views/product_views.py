from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Product, Category


def demo(request):
    return render(request, 'store/index.html', {})


def product_list(request):
    product_queryset = Product.objects.filter(is_available=True)
    category_queryset = Category.objects.all()
    query = request.GET.get('query',False)
    category = request.GET.get('category',False)

    if query or category:
        if query:
            product_queryset = product_queryset.filter(
                        Q(title__icontains=query) | 
                        Q(school__name__icontains=query) |
                        Q(category__name__icontains=query)
                        )
        if category:
            product_queryset = product_queryset.filter(category__name__exact=category)

    data = {
        'product_list': True,
        'products': product_queryset,
        'categories': category_queryset
    }

    if query:
        data['query'] = query
    if category:
        data['category_query'] = category

    return render(request, 'store/product_list.html', data)


def product_detail(request,product_id):
    product_id = int(product_id)

    product = get_object_or_404(Product,product_id=product_id)
    instance_set = product.productinstance_set.all().filter(is_available=True)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'instances': instance_set
    })
