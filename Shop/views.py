from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.shortcuts import  render_to_response
from django.template.context import RequestContext
from Shop.models import Product, Category

def index(request):
    newestProducts = Product.objects.all().order_by('createdDate')[:10]

    return render_to_response('Shop/index.html', {'products': newestProducts, 'is_display_banner' : True })

def product_list(request, slug, pIndex=1, pSize=15, orderBy='name', sortOrder='desc', mode='grid'):
    category = Category.objects.get(slug=slug)
    categoryIdList = [category.id]
    for subCategory in category.children.all():
        categoryIdList.append(subCategory.id)

    query = Product.objects.filter(category__id__in=categoryIdList).order_by(orderBy)

    if sortOrder == 'desc':
        query = query.reverse()

    paginator = Paginator(query.all(), pSize)

    display_info = {'pIndex' : pIndex,
                   'pSize' : str(pSize),
                   'orderBy' : orderBy,
                   'sortOrder' : sortOrder,
                   'mode': mode }

    viewmodel = {'curPage': paginator.page(pIndex),
                 'current' : category,
                 'display_info': display_info }

    return render_to_response('Shop/product_list.html', {'viewmodel': viewmodel}, context_instance = RequestContext(request) )

def search_result(request, pIndex=1, pSize=15, orderBy='name', sortOrder='desc', mode='grid'):
    query = request.GET['q']

    categoryResults = Category.objects.filter(name__contains=query)

    product_ids_list = [x.id for x in categoryResults]

    result = Product.objects.filter(Q(category_id__in=product_ids_list) | Q(name__contains=query)).order_by(orderBy)

    if sortOrder == 'desc':
        result = result.reverse()

    paginator = Paginator(result, pSize)

    display_info = {'pIndex' : pIndex,
                    'pSize' : str(pSize),
                    'orderBy' : orderBy,
                    'sortOrder' : sortOrder,
                    'mode': mode }

    viewmodel = {'curPage': paginator.page(pIndex),
                 'current' : None,
                 'display_info': display_info }

    return render_to_response('Shop/product_list.html', {'viewmodel': viewmodel}, context_instance = RequestContext(request) )

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)

    viewmodel = {'current' : product}

    return render_to_response('Shop/product_detail.html', {'viewmodel' : viewmodel })