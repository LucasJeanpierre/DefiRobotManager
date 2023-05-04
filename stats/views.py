from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max
import random

from .models import Institution, Team, AesteticScores, Run

# Create your views here.

def index(request):
    return render(request, 'stats/index.html')


def getScores():
    #get the max number of runs
    max_num_runs = Run.objects.aggregate(Max('num_run'))['num_run__max']

    scores_list = []

    for i_run in range(1, max_num_runs+1):
        runs = Run.objects.filter(num_run=i_run).order_by('-score', 'time')

        scores = []

        #for each runs add the bonus time
        for i, run in enumerate(runs):
            if (run.score == 160) and (i < 8):
                scores.append({"team" : run.team, "score" : run.score + 40 - i*5, "time" : run.time})
            else:
                scores.append({"team" : run.team, "score" : run.score, "time" : run.time})

        scores_list.append(scores)

   

    return scores_list

  

def getRankings():

    scores_list = getScores()

    #get all teams
    teams = Team.objects.all()

    #keep only the best score for each team

    best_scores = []
    
    for team in teams:
        best_score = -1
        best_time = 1000
        found = False
        for scores in scores_list:
            for score in scores:
                if score["team"].id == team.id:
                    if score["score"] > best_score or (score["score"] == best_score and score["time"] < best_time):
                        best_score = score["score"]
                        best_time = score["time"]
                        found = True
                    break
        if found:
            best_scores.append({"team": team, "score" : best_score, "time" : best_time})

    aestetic_scores = AesteticScores.objects.all()

    #add the aestetic scores
    for aestetic_score in aestetic_scores:
        for score in best_scores:
            if aestetic_score.first_rank.id == score["team"].id:
                score["score"] += 10
            if aestetic_score.second_rank.id == score["team"].id:
                score["score"] += 5
            if aestetic_score.third_rank.id == score["team"].id:
                score["score"] += 2

    
    #sort the scores by score reversed and time not reversed
    best_scores.sort(key=lambda x: (x["score"], -x["time"]), reverse=True)

    rankings = []
    #create a list of the rankings
    for score in best_scores:
        rankings.append({"team": Team.objects.get(id=score['team'].id), "score": score['score'], "time": score['time'], "rank": best_scores.index(score)+1})

    return rankings

def rankings(request):
    #get all institutions
    institutions = Institution.objects.all()
    #get all teams
    teams = Team.objects.all()
    #get all aestetic scores
    aestetic_scores = AesteticScores.objects.all()
    #get all runs
    runs = Run.objects.all()
    
    #get rankings
    rankings = getRankings()

    #print(rankings)

    #create an object to store all the data
    content = {"institution": institutions, "team": teams, "aestetic_scores": aestetic_scores, "run": runs, "rankings": rankings}

    return render(request, 'stats/rankings.html', {'content': content})



def institutionRankings(request):
    institutions = Institution.objects.all()

    scores_list = getScores()

    for institution in institutions:
        institution.scores = []
        institution.team = {}
        for scores in scores_list:
            for score in scores:
                if score["team"].institution.id == institution.id:
                    institution.scores.append(score)
                    if institution.team.get(score["team"].id) == None:
                        institution.team[score["team"].id] = 1
                    else:
                        institution.team[score["team"].id] += 1
        
        #check if all the teams have the same number of runs
        if len(institution.team) > 0:
            for team in institution.team:
                if institution.team[team] == 1:
                    institution.scores.append({"team" : Team.objects.get(id=team), "score" : 0, "time" : 999})

    
    institutionRankings = []

    for institution in institutions:
        avg_score = 0
        avg_time = 0
        for score in institution.scores:
            avg_score += score["score"]
            avg_time += score["time"]
        avg_score /= len(institution.scores)
        avg_time /= len(institution.scores)
        institutionRankings.append({"institution": institution, "avg_score": avg_score, "avg_time": avg_time})

    institutionRankings.sort(key=lambda x: (-x["avg_score"], x["avg_time"]))

    for i, institution in enumerate(institutionRankings):
        institution["rank"] = i+1



    return render(request, 'stats/institutionsRanking.html', {'institutionRankings': institutionRankings})


def round(request):
    scores = getScores()

    #GET parameters
    round = request.GET.get('round', 1)

    #add the rank
    for i, score in enumerate(scores[int(round)-1]):
        score["rank"] = i+1

    return render(request, 'stats/round.html', {'scores': scores[int(round)-1], 'round': round})


def generateOrder(request):
    #if the request is a POST request
    if request.method == 'POST':
        #get all teams
        teams = Team.objects.all()

        order = [i for i in range(1, len(teams)+1)]
        random.shuffle(order)

        for i, team in enumerate(teams):
            team.order = order[i]
            team.save()
        
        return redirect('/stats/teamList')
    
    #return an error 500
    return HttpResponse("Method not allowed",status=500)


def teamList(request):
    #get all teams
    teams = Team.objects.all().order_by('order')

    #get all runs
    runs = Run.objects.all()

    #link each team to its runs
    for team in teams:
        team.runs = []
        for run in runs:
            if run.team.id == team.id:
                team.runs.append(run)

    content = {"teams": teams}

    return render(request, 'stats/teamList.html', {'content': content})

    
