from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'payment'

urlpatterns = [
 path(_('process/'), views.payment_process, name='process'),
 path(_('done/'), views.PaymentDoneView.as_view(), name='done'),
 path(_('canceled/'), views.PaymentCancelledView.as_view(), name='canceled'),
]