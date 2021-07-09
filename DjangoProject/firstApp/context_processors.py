import datetime

from . import models


def shared_context(request):
    """
    this function holds the shared conrtext variables across all templates
    """
    return {
        'year': datetime.datetime.today().year,
        'category_list': models.Category.objects.values_list('name')
        # values_list returns a list of model fields and in () we say
        # which fields we want and pass them as an argument
    }
