from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max

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

    #get the max number of runs
    max_num_runs = Run.objects.aggregate(Max('num_run'))['num_run__max']

    scores_list = []

    for i_run in range(1, max_num_runs+1):
        runs = Run.objects.filter(num_run=i_run).order_by('-score', 'time')

        scores = []

        #for each runs add the bonus time
        for i, run in enumerate(runs):
            if (run.score == 160) and (i < 8):
                scores.append([run.team.id, run.score + 40 - i*5, run.time])
            else:
                scores.append([run.team.id, run.score, run.time])


        scores_list.append(scores)

    #keep only the best score for each team

    best_scores = []
    
    for team in teams:
        best_score = 0
        best_time = 999
        found = False
        for scores in scores_list:
            for score in scores:
                if score[0] == team.id:
                    if score[1] > best_score or (score[1] == best_score and score[2] < best_time):
                        best_score = score[1]
                        best_time = score[2]
                        found = True
                    break
        if found:
            best_scores.append([team.id, best_score, best_time])


    #add the aestetic scores
    for aestetic_score in aestetic_scores:
        for score in best_scores:
            if aestetic_score.first_rank.id == score[0]:
                score[1] += 10
            if aestetic_score.second_rank.id == score[0]:
                score[1] += 5
            if aestetic_score.third_rank.id == score[0]:
                score[1] += 2

    
    #sort the scores by score reversed and time not reversed
    best_scores.sort(key=lambda x: (x[1], -x[2]), reverse=True)

    rankings = []
    #create a list of the rankings
    for score in best_scores:
        rankings.append({"team": Team.objects.get(id=score[0]), "score": score[1], "time": score[2], "rank": best_scores.index(score)+1})

    #print(rankings)

    #create an object to store all the data
    content = {"institution": institutions, "team": teams, "aestetic_scores": aestetic_scores, "run": runs, "rankings": rankings}

    return render(request, 'stats/rankings.html', {'content': content})