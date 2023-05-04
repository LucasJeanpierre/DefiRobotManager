from django.db import models

# Create your models here.


class Institution(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Team(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class AesteticScores(models.Model):
    # id = models.IntegerField(primary_key=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    first_rank = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='first_rank')
    second_rank = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='second_rank')
    third_rank = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='third_rank')

    def __str__(self):
        return self.institution.name + " " + str(self.first_rank) + " " + str(self.second_rank) + " " + str(self.third_rank)


class Run(models.Model):
    # id = models.IntegerField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    time = models.FloatField(default=999)
    num_run = models.IntegerField()
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.team.name + " " + str(self.time) + "s " + str(self.score)