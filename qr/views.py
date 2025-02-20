from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from base.models import EventDates
from django.utils import timezone
from .models import Profile, Card, Qr, Scan
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import csv, json

BONUS_POINTS = 25

def checkBonus(collection, card):
    bonus = False

    tier_score_initial = 1
    for i in collection[card.tier]:
        tier_score_initial *= i

    collection[card.tier][card.identity] += 1

    tier_score_final = 1
    for i in collection[card.tier]:
        tier_score_final *= i

    if tier_score_initial == 0 and tier_score_final != 0:
        bonus = True

    return bonus

def home(request):
    event_dates = EventDates.objects.filter(type="hunt").order_by('-event_start').first()
    context = {}
    msg = "Hunt has ended"
    time_diff = -1
    end = True
    if event_dates is not None:
        current_time = timezone.now()
        time_diff = 0
        end = False
        if event_dates.event_start > current_time:
            time_diff = (event_dates.event_start - current_time).total_seconds()
            msg = "Hunt Starts in"
        elif event_dates.event_end > current_time:
            time_diff = (event_dates.event_end - current_time).total_seconds()
            msg = "Hunt Ends in"
        else:
            time_diff = (event_dates.event_end - current_time).total_seconds()
            msg = "Hunt has ended"
            end = True
    context['msg'] = msg
    context['time_diff'] = int(time_diff)
    context['has_ended'] = end
    return render(request, 'qr/home.html', context)

def leaderboard(request):
    profiles = Profile.objects.all().order_by('-points')
    return render(request, 'qr/leaderboard.html', {'profiles': profiles})

@login_required
def scan(request, code):
    context = {}
    profile = Profile.objects.filter(user=request.user).first() 
    if profile is None:
        messages.error(request, "Please register first.")
        return redirect('/qr/register')
    context['profile'] = profile

    try:
        qr = Qr.objects.get(uniqueId=code)
    except Qr.DoesNotExist:
        messages.error(request, "Invalid QR Code.")
        return redirect('qr:home')

    card = qr.card
    context['card'] = card

    # Prevent duplicate scans for the same QR
    if Scan.objects.filter(profile=profile, qr=qr).exists():
        context['duplicate'] = True
        messages.info(request, "You have already scanned this card.")
        return render(request, 'qr/scan.html', context)

    # Award points and record the scan directly
    Scan.objects.create(profile=profile, qr=qr)
    profile.points += card.point

    collection_obj = json.loads(profile.collections)
    bonus = checkBonus(collection_obj, card)
    if bonus:
        profile.points += BONUS_POINTS
    context['bonus'] = bonus

    profile.collections = json.dumps(collection_obj)
    profile.save()

    context['success'] = f"Card '{card.name}' collected! Points awarded: {card.point + (BONUS_POINTS if bonus else 0)}"
    return render(request, 'qr/scan.html', context)

@login_required 
def profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if profile is None:
        messages.info(request, 'Please register first')
        return redirect('/qr/register')
    
    context = {'profile': profile}
    rank = Profile.objects.filter(points__gt=profile.points).count() + 1
    context['rank'] = rank

    cards = Card.objects.all()
    context['cards'] = cards

    collection = json.loads(profile.collections)
    context['collection'] = collection
    return render(request, 'qr/profile.html', context)

@login_required
def register_for_hunt(request):
    if request.method == 'POST':
        profile = Profile.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            picture='https://ui-avatars.com/api/?name=' + request.user.first_name + '+' + request.user.last_name + '&background=fdba74&color=282319',
            email=request.POST.get('email'),
            mobile=request.POST.get('phone_number'),
            registration=request.POST.get('reg'),
        )
        messages.success(request, 'Profile created successfully')
        return redirect('/qr/profile')

    if Profile.objects.filter(user=request.user).exists():
        messages.info(request, 'You have already registered')
        return redirect('/qr/profile')
    return render(request, 'qr/register.html')

@login_required
def scanner(request):
    profile = Profile.objects.filter(user=request.user).first()
    if profile is None:
        return redirect('/qr/profile')
    return render(request, 'qr/scanner.html')

def generate_qr(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            if Qr.objects.all().count() == 0:
                for card in Card.objects.all():
                    for i in range(10):
                        Qr.objects.create(card=card)
                        
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="qrs.csv"'

            writer = csv.writer(response)
            writer.writerow(['Card Name', 'Tier', 'Identity', 'Unique ID'])
            for qr in Qr.objects.all():
                writer.writerow([qr.card.name, qr.card.tier, qr.card.identity, qr.uniqueId])
            return response

        return render(request, 'qr/generate_qr.html')
    return redirect('/qr/')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('qr:home')
