from typing import Any

from django.core.paginator import Paginator
from django.db.models.manager import BaseManager
from django.http import HttpResponse, Http404
from django.shortcuts import render

from goods.models import Products
from goods.utils import q_search


def catalog(request, category_slug: str = None) -> HttpResponse:
    page = request.GET.get('page', 1)

    on_sale = request.GET.get('on_sale', None)

    order_by = request.GET.get('order_by', None)

    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods: BaseManager[Products] = Products.objects.all()

    elif query:
        goods: BaseManager[Products] | None = q_search(query=query)

    else:
        goods: list[Products] = Products.objects.filter(category__slug=category_slug)
        if not goods.exists():
            raise Http404

    if on_sale:
        goods: BaseManager[Products] | Any = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods: BaseManager[Products] | Any = goods.order_by(order_by)

    paginator = Paginator(object_list=goods, per_page=3)

    current_page = paginator.page(int(page))

    context: dict[str, Any] = {
        'title': 'Home - Каталог',
        'goods': current_page,
        'slug_url': category_slug,
    }

    return render(request, 'goods/catalog.html', context)


def product(request, product_slug: str = False, product_id: int = False) -> HttpResponse:
    if product_id:
        product_obj: Products = Products.objects.get(id=product_id)
    else:
        product_obj: Products = Products.objects.get(slug=product_slug)

    context: dict[str, Products] = {
        'product': product_obj,
    }
    return render(request, 'goods/product.html', context=context)
