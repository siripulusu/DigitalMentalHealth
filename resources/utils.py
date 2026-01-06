def recommend_resources(severity=None, category=None):
    from .models import Resource

    qs = Resource.objects.all()

    if severity:
        qs = qs.filter(severity__in=['all', severity.lower()])

    if category:
        qs = qs.filter(category=category)

    return qs
