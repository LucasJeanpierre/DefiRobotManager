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


    #get the second best score for each team if it exists

    second_best_scores = []

    for score in best_scores:
        team = score["team"]

        #get the num_rum of the best score
        num_run = Run.objects.filter(team=team, score=score["score"], time=score["time"])[0].num_run
        other_num_run = 1 if num_run == 2 else 2

        #get the second best score
        second_best_score = Run.objects.filter(team=team, num_run=other_num_run).order_by('-score', 'time')[0]
        second_best_scores.append({"team": team, "score" : second_best_score.score, "time" : second_best_score.time})

    #sort the second best scores by score and time reversed
    second_best_scores.sort(key=lambda x: (x["score"], -x["time"]), reverse=True)



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
        bool_ex_aequo = False
        ranking = {"team": Team.objects.get(id=score['team'].id), "score": score['score'], "time": score['time']}

        #handle ex aequo
        if len(rankings) > 0:
            if ranking["score"] == rankings[-1]["score"] and ranking["time"] == rankings[-1]["time"]:
                ranking["rank"] = rankings[-1]["rank"]
            else:
                ranking["rank"] = len(rankings) + 1
        else:
            ranking["rank"] = 1
        
        rankings.append(ranking)


    #create a list with the number of teams for each rank
    num_teams = []
    for ranking in rankings:
        if len(num_teams) < ranking["rank"]:
            num_teams.append(1)
        else:
            num_teams[ranking["rank"]-1] += 1

    print(num_teams)

    for i in num_teams:
        if i > 1:
            current_rank = rankings[i-1]["rank"]
            #handle ex aequo, update the rank of the teams according the index of the team in the second best scores list
            ex_eaquo_teams = rankings[current_rank-1:current_rank-1+i]

            for team in ex_eaquo_teams:
                if team["rank"] == current_rank:
                    #get the index of the team in the second best scores list
                    for j, score in enumerate(second_best_scores):
                        if score["team"].id == team["team"].id:
                            index = j
                            break
                    team["rank"] = current_rank + index
            
            #sort the ex aequo teams by rank
            ex_eaquo_teams.sort(key=lambda x: x["rank"])

            #update the rankings
            for j, team in enumerate(ex_eaquo_teams):
                rankings[current_rank-1+j] = team
            
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
        
        if len(institution.scores) > 0:
            avg_score /= len(institution.scores)
            avg_time /= len(institution.scores)
        else:
            avg_score = 0
            avg_time = 999
        
        institutionRankings.append({"institution": institution, "avg_score": avg_score, "avg_time": avg_time})

    institutionRankings.sort(key=lambda x: (-x["avg_score"], x["avg_time"]))

    for i, institution in enumerate(institutionRankings):

        if i > 0:
            if institution["avg_score"] == institutionRankings[i-1]["avg_score"] and institution["avg_time"] == institutionRankings[i-1]["avg_time"]:
                institution["rank"] = institutionRankings[i-1]["rank"]
            else:
                institution["rank"] = i+1
        else:
            institution["rank"] = 1


    return render(request, 'stats/institutionsRanking.html', {'institutionRankings': institutionRankings})


def aesteticRankings(request):
    aestetic_scores = AesteticScores.objects.all()

    teams = Team.objects.all()

    aestetic_rankings = {}

    for team in teams:
        aestetic_rankings.update({team.id: {"team": team, "score": 0}})
        

    for aestetic_score in aestetic_scores:
        aestetic_rankings[aestetic_score.first_rank.id]["score"] += 10
        aestetic_rankings[aestetic_score.second_rank.id]["score"] += 5
        aestetic_rankings[aestetic_score.third_rank.id]["score"] += 2

    aestetic_rankings = list(aestetic_rankings.values())

    aestetic_rankings.sort(key=lambda x: x["score"], reverse=True)

    for i, aestetic_ranking in enumerate(aestetic_rankings):
        #handle ex aequo
        if i > 0 and aestetic_ranking["score"] == aestetic_rankings[i-1]["score"]:
            aestetic_ranking["rank"] = aestetic_rankings[i-1]["rank"]
        else:
            aestetic_ranking["rank"] = i+1


    return render(request, 'stats/aesteticRanking.html', {'aestetic_rankings': aestetic_rankings})



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
        
        return redirect('/stats/teamList/?reveal=true')
    
    #return an error 500
    return HttpResponse("Method not allowed",status=500)


def teamList(request):
    #get all teams
    teams = Team.objects.all().order_by('order')

    #get all runs
    runs = Run.objects.all()

    #get the reveal get parameter
    reveal = request.GET.get('reveal', False)

    #link each team to its runs
    for team in teams:
        team.runs = []
        for run in runs:
            if run.team.id == team.id:
                if run.num_run == 1:
                    if len(team.runs) == 0:
                        team.runs.append(run)
                    else:
                        team.runs[0] = run
                elif run.num_run == 2:
                    if len(team.runs) == 1:
                        team.runs.append(run)
                    else:
                        team.runs.append(None)
                        team.runs.append(run)

    content = {"teams": teams, "reveal": reveal}

    return render(request, 'stats/teamList.html', {'content': content})

    
