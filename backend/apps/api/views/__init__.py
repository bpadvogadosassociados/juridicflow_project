# apps/api/views/__init__.py

from .auth import login_view, logout_view, me_view, refresh_token_view
from .customers import CustomerViewSet
from .processes import ProcessViewSet
from .deadlines import DeadlineViewSet
from .documents import DocumentViewSet
from .finance import FeeAgreementViewSet, PaymentViewSet

__all__ = [
    'login_view',
    'logout_view',
    'me_view',
    'refresh_token_view',
    'CustomerViewSet',
    'ProcessViewSet',
    'DeadlineViewSet',
    'DocumentViewSet',
    'FeeAgreementViewSet',
    'PaymentViewSet',
]