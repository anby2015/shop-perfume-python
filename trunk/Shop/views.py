from django.core.paginator import Paginator
from django.shortcuts import  render_to_response
from Shop.menus import get_main_menu, get_menu_path
from Shop.models import Product, Category

def index(request):
    newestProducts = Product.objects.all().order_by('createdDate')[:10]

    return render_to_response('Shop/index.html', {'products': newestProducts })

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
                 'category' : category,
                 'pIndex' : pIndex,
                 'pSize' : str(pSize),
                 'orderBy' : orderBy,
                 'sortOrder' : sortOrder,
                 'mode': mode }

    return render_to_response('Shop/product_list.html', {'viewmodel': viewmodel})


