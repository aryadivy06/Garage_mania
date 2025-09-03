from .models import UserRegister
from garage.models import ServiceProviderTable

def global_user_context(request):
    """
    Makes both 'normal user' and 'service provider' available in all templates.
    """
    normal_user = None
    sp = None

    # Normal user via session
    user_id = request.session.get('user_id')
    if user_id:
        try:
            normal_user = UserRegister.objects.get(id=user_id)
        except UserRegister.DoesNotExist:
            request.session.flush()

    # Service provider via Django auth
    if request.user.is_authenticated:
        try:
            sp = getattr(request.user, "service_provider", None) or getattr(request.user, "serviceprovidertable", None)
        except ServiceProviderTable.DoesNotExist:
            sp = None

    return {
        "normal_user": normal_user,
        "service_provider": sp,
    }
