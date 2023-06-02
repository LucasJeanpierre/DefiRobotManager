from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max
from django.contrib.auth.decorators import login_required
import random

from .models import Institution, Team, AesteticScores, Run

# Create your views here.

def index(request):
    return render(request, 'stats/index.html')


def getScores():
    #get the max number of runs
    max_num_runs = Run.objects.aggregate(Max('num_run'))['num_run__max']

    scores_list = []

    if max_num_runs:
        for i_run in range(1, max_num_runs+1):
            runs = Run.objects.filter(num_run=i_run).order_by('-score', 'time')

            scores = []

            #for each runs add the bonus time
            for i, run in enumerate(runs):
                if (run.score == 160) and (i < 8):
                    #check for ex aequo
                    if i > 0 and run.time == runs[i-1].time:
                        scores.append({"team" : run.team, "score" : scores[i-1]["score"], "time" : run.time, "num_run" : run.num_run})
                    else:
                        scores.append({"team" : run.team, "score" : run.score + 40 - i*5, "time" : run.time, "num_run" : run.num_run})
                else:
                    scores.append({"team" : run.team, "score" : run.score, "time" : run.time, "num_run" : run.num_run})

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
        best_num_run = 0
        found = False
        for scores in scores_list:
            for score in scores:
                if score["team"].id == team.id:
                    if score["score"] > best_score or (score["score"] == best_score and score["time"] < best_time):
                        best_score = score["score"]
                        best_time = score["time"]
                        best_num_run = score["num_run"]
                        found = True
                    break
        if found:
            best_scores.append({"team": team, "score" : best_score, "time" : best_time, "num_run" : best_num_run})


    #get the second best score for each team if it exists

    second_best_scores = []

    for score in best_scores:
        team = score["team"]

        #get the num_rum of the best score
        num_run = score["num_run"]
        other_num_run = 1 if num_run == 2 else 2

        #get the second best score
        second_best_score_request = Run.objects.filter(team=team, num_run=other_num_run).order_by('-score', 'time')
        if (len(second_best_score_request) > 0):
            second_best_score = second_best_score_request[0]
            second_best_scores.append({"team": team, "score" : second_best_score.score, "time" : second_best_score.time})

    #sort the second best scores by score and time reversed
    second_best_scores.sort(key=lambda x: (x["score"], -x["time"]), reverse=True)

    #add rank to the second best scores
    for i, score in enumerate(second_best_scores):
        score["rank"] = i+1


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
    ranks = [0 for i in range(len(rankings))]

    for i in range(1, len(rankings)+1):
        ranks[i-1] = rankings[i-1]["rank"]

    #print(ranks)
    for i in range(1, len(rankings)+1):
        num_teams.append(ranks.count(i))

    #print(num_teams)
    
    #solve ex aequo if possible
    for i, nb_teams in enumerate(num_teams):
        if (nb_teams > 1):
            #get the teams with the same rank
            same_rank_teams = [ranking for ranking in rankings if ranking["rank"] == i+1]
           # print("same team rank", same_rank_teams)

            #get the second best score of the teams with the same rank
            second_scores = [score for score in second_best_scores if score["team"].id in [team["team"].id for team in same_rank_teams]]
            #sort the second best scores by score and time reversed
            second_scores.sort(key=lambda x: (x["score"], -x["time"]), reverse=True)
            #print("second scores", second_scores)

            #solve ex aequo with the rank of the second best score
            for i in range(i, i+nb_teams):
                rankings[i]["rank"] += second_scores.index([score for score in second_scores if score["team"].id == rankings[i]["team"].id][0])

    #sort the rankings by rank
    rankings.sort(key=lambda x: x["rank"])

            
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

    #check the max score
    max_score = aestetic_rankings[0]["score"]

    if (max_score == 0):
        aestetic_rankings = {}

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
    #if the request is not a POST request
    if request.method != 'POST':
        return HttpResponse("Method not allowed",status=500)
    
    #if user is not authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized",status=401)


    teams = Team.objects.all()

    order = [i for i in range(1, len(teams)+1)]
    random.shuffle(order)

    for i, team in enumerate(teams):
        team.order = order[i]
        team.save()
    
    return redirect('/stats/teamList/?reveal=true')

    


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

    
