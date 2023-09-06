from typing import Any, Dict
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from .forms import UserPromoCodeForm
from .models import UserPromoCode

# Create your views here.


class UserPromoCodesListView(LoginRequiredMixin, ListView):
    model = UserPromoCode
    template_name = "user_promo_codes_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        # Will be used in UserPromoCodePostView
        ctx["promo_code_form"] = UserPromoCodeForm(user=self.request.user)
        return ctx


class UserPromoCodePostView(LoginRequiredMixin, View):
    form_class = UserPromoCodeForm
    template_name = "promotions/partials/userpromocode_form.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            promo_code = form.cleaned_data["promo_code"]
            UserPromoCode.objects.create(user=request.user, promo_code=promo_code)
            messages.success(request, _("Promo code added successfully to your list."))
        # Return HTMX
        return render(request, self.template_name, {"form": form})
