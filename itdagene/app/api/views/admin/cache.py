from itdagene.app.api.util import login_or_token_required
from itdagene.core.util.cache import flush_cache
from django.http import HttpResponse

@login_or_token_required()
def flush(request):
    flush_cache()
    return HttpResponse()