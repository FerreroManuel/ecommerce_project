from .models import Category


def categories(request):
    return {
        # 'categories': Category.objects.all()                  <- Retorna todas las categorías y sub-categorías
        'categories': Category.objects.filter(level=0)      #   <- Retorna sólo las categorías primarias
    }
