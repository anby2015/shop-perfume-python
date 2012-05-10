from django.core.paginator import Paginator
from django.shortcuts import  render_to_response
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
        query.reverse()

    paginator = Paginator(query.all(), pSize)

    viewmodel = {'curPage': paginator.page(pIndex),
                 'current' : category,
                 'pIndex' : pIndex,
                 'pSize' : str(pSize),
                 'orderBy' : orderBy,
                 'sortOrder' : sortOrder,
                 'mode': mode }

    return render_to_response('Shop/product_list.html', {'viewmodel': viewmodel})

def search_result(request):
    query = request.GET['q']

    result = []

    categoryResults = Category.objects.filter(name__contains=query)

    for categoryResult in categoryResults:
        result.extend(categoryResult.products.all())

    product_ids_list = [x.id for x in result]

#    not in product_ids_list
    result.extend(Product.objects.filter(id__in=product_ids_list).filter(name__contains=query).all())

    return render_to_response('Shop/search_result.html', {'result': result})

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)

    viewmodel = {'current' : product}

    return render_to_response('Shop/product_detail.html', {'viewmodel' : viewmodel })