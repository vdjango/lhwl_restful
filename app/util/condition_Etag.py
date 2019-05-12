from app.models import WareApp


def latest_entry(request, details_id, *args, **kwargs):
    '''
    Last-Modified和ETag实现
    :param request:
    :param details_id: WareApp ID
    :return:
    '''
    Ware = WareApp.objects.filter(id=details_id)
    if Ware.exists():
        return Ware.latest("time_now").time_now.now()

    return Ware
