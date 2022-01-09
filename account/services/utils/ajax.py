def is_ajax(request):
    '''Проверяет, является ли запрос ajax-запросом'''
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'