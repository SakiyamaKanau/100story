from .models import Category

def all_category(request):
  category_list = Category.objects.all()

  params = {
    'category_list': category_list,#categoryリストを全てのページで利用可能にする
  }

  return params