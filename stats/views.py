from django.shortcuts import render
from django.http import HttpResponse

from .models import Institution, Team, AesteticScores, Run

# Create your views here.

def index(request):
    message = "Hello, world. You're at the stats index."
    return render(request, template_name='stats/index.html', context={'message': message})

def rankings(request):
    #get all institutions
    institutions = Institution.objects.all()
    #get all teams
    teams = Team.objects.all()
    #get all aestetic scores
    aestetic_scores = AesteticScores.objects.all()
    #get all runs
    runs = Run.objects.all().order_by('-score')

    scores = []

    #for each runs add the bonus time
    for i, run in enumerate(runs):
        if (run.score == 160) and (i < 8):
            scores.append([run.team.id, run.score + 40 - i*5])
        else:
            scores.append([run.team.id, run.score])

    #add the aestetic scores
    for aestetic_score in aestetic_scores:
        for score in scores:
            if aestetic_score.first_rank.id == score[0]:
                score[1] += 10
            if aestetic_score.second_rank.id == score[0]:
                score[1] += 5
            if aestetic_score.third_rank.id == score[0]:
                score[1] += 2

    
    #sort the scores by the score
    scores.sort(key=lambda x: x[1], reverse=True)

    rankings = []

    #create a list of the rankings
    for score in scores:
        rankings.append({"team": Team.objects.get(id=score[0]), "score" : score[1], "rank": scores.index(score) + 1})

    print(rankings)

    #create an object to store all the data
    content = {"institution": institutions, "team": teams, "aestetic_scores": aestetic_scores, "run": runs, "rankings": rankings}

    return render(request, 'stats/rankings.html', {'content': content})