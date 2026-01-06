from django.shortcuts import render
from .models import Resource , CommunityLink
from .utils import recommend_resources
from assessments.models import SelfAssessment

def resources_view(request):
    severity = None

    if request.user.is_authenticated:
        latest = SelfAssessment.objects.filter(user=request.user).order_by('-created_at').first()
        if latest:
            severity = latest.severity.lower()

    resources = recommend_resources(severity=severity)

    return render(request, 'resources/resources.html', {
        'resources': resources,
        'severity': severity
    })


def community_view(request):
    links = CommunityLink.objects.all().order_by('-created_at')
    return render(request, 'resources/community.html', {
        'links': links
    })