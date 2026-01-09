from django.shortcuts import render, redirect
from .models import Resource, CommunityLink
from assessments.models import SelfAssessment
from django.contrib.auth.decorators import login_required
from .utils import recommend_resources

def resources_view(request):
    severity = None
    if request.user.is_authenticated:
        latest = (
            SelfAssessment.objects
            .filter(user=request.user)
            .order_by('-created_at')
            .first()
        )
        if latest and latest.severity:
            severity = latest.severity.lower()

    # Define Instant Self-Help tools here to avoid template split errors
    instant_tools = [
        {'id': 'Breathing', 'icon': 'fa-wind', 'title': 'Breathing Exercises', 'desc': 'Short guided practices to calm the nervous system.'},
        {'id': 'Grounding', 'icon': 'fa-earth-americas', 'title': 'Grounding Methods', 'desc': 'The 5-4-3-2-1 technique to regain control during panic.'},
        {'id': 'Sleep', 'icon': 'fa-moon', 'title': 'Sleep Hygiene', 'desc': 'Practical tips to improve sleep quality and reduce insomnia.'},
        {'id': 'Yoga', 'icon': 'fa-spa', 'title': 'Yoga & Flow', 'desc': 'Gentle body-based relaxation to reduce physical tension.'},
        {'id': 'Sound', 'icon': 'fa-music', 'title': 'Music Therapy', 'desc': 'Curated calming sounds to regulate mood and focus.'},
        {'id': 'Crisis', 'icon': 'fa-heart-pulse', 'title': 'When to Seek Help', 'desc': 'Guidance on identifying clinical warning signs.'},
    ]

    # recommendation logic
    recommendations = recommend_resources(severity=severity)

    return render(request, 'resources/resources.html', {
        'resources': recommendations,
        'severity': severity,
        'instant_tools': instant_tools,  # Added this
    })
def community_view(request):
    # Handle POST for Volunteers/Admins to add new forms
    if request.method == 'POST':
        if request.user.is_authenticated and (request.user.role == 'peer' or request.user.is_staff):
            title = request.POST.get('title')
            description = request.POST.get('description')
            form_link = request.POST.get('form_link')
            
            if title and form_link:
                CommunityLink.objects.create(
                    title=title,
                    description=description,
                    form_link=form_link
                )
            return redirect('community_view')

    # 2. Fetch all links to render for students and volunteers
    links = CommunityLink.objects.all().order_by('-created_at')
    
    return render(request, 'resources/community.html', {
        'links': links
    })

@login_required
def manage_resources(request):
    if request.user.role != 'counsellor':
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        category = request.POST.get('category')
        description = request.POST.get('description', '')
        
        Resource.objects.create(
            title=title, 
            link=link, 
            category=category,
            description=description
        )
        return redirect('manage_resources')
    
    all_resources = Resource.objects.all().order_by('-id')
    return render(request, 'dashboard/counsellor_resources.html', {'resources': all_resources})