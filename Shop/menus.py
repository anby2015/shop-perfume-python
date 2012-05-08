from Shop.models import Category

class Menu:
    def __init__(self, category, index = 0, parentIndex = 0, listSize = 0 ):
        self.index = index
        self.parentIndex = parentIndex
        self.category = category
        self.listSize = listSize
        self.children = []

    def cssClass(self):
        cssOrder = ''
        if self.index == self.listSize:
            cssOrder = 'last'
        elif self.index == 1:
            cssOrder = 'first'

        if not self.parentIndex:
            return 'level0 nav-%(param1)d level-top %(param2)s parent' % {"param1": self.index, "param2": cssOrder}
        else:
            return 'level1 nav-%(param1)d-%(param2)d %(param3)s' % {"param1": self.index, "param2": self.parentIndex, "param3" : cssOrder}

    def displayName(self):
        return self.category.name

    def link(self):
        return self.category.get_absolute_url()

    def isLast(self):
        return self.index == self.listSize

def get_main_menu():
    categories = Category.objects.filter(parent__isnull=True)

    mainMenu = []

    index = 1
    parentListSize = categories.count()
    for category in categories:

        menu = Menu(category, index, 0, parentListSize)

        subIndex = 1
        subListSize = category.children.count()
        for subCategory in category.children.all():
            menu.children.append(Menu(subCategory, subIndex, index, subListSize))
            subIndex += 1

        mainMenu.append(menu)
        index += 1

    return mainMenu

def get_menu_path(category):
    menuPaths = []

    if category.parent is not None:
        menuPaths.append(Menu(category.parent, 1, 0, 2))
    menuPaths.append(Menu(category,2, 0, 2))

    return menuPaths