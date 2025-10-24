from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, blank=True, related_name='teams')

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('run', 'Running'),
        ('walk', 'Walking'),
        ('strength', 'Strength Training'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration_minutes = models.PositiveIntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    points = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.activity_type} @ {self.timestamp}"


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"


class LeaderboardEntry(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='leaderboard_entries')
    points = models.FloatField(default=0)

    def __str__(self):
        return f"{self.team.name}: {self.points} pts"
