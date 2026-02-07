from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse


def healthz(request):
    db_ok = True
    try:
        connections['default'].cursor()
    except OperationalError:
        db_ok = False

    status = 200 if db_ok else 503

    return JsonResponse(
        {
            'status': 'ok' if db_ok else 'degraded',
            'database': db_ok,
        },
        status=status,
    )
