from yanvision_ecommerce.basket.utils import get_user_basket


def context(request):
    ctx = dict()
    ctx["basket"] = get_user_basket(request)
    return ctx
