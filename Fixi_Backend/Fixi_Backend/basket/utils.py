from .models import Basket


def get_user_basket(request):
    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        basket, created = Basket.objects.get_or_create(session_key=session_key)
    return basket
