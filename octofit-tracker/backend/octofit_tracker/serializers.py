from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team, Activity, Workout, LeaderboardEntry
from bson import ObjectId

User = get_user_model()

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value) if value else None
    def to_internal_value(self, data):
        return ObjectId(data) if data else None

class UserSerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff']

class TeamSerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)
    members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = ['id', 'name', 'members']

class ActivitySerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    class Meta:
        model = Activity
        fields = ['id', 'user', 'team', 'activity_type', 'duration_minutes', 'distance_km', 'points', 'timestamp']

class WorkoutSerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Workout
        fields = ['id', 'user', 'name', 'notes', 'created_at']

class LeaderboardEntrySerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)
    team = TeamSerializer(read_only=True)
    class Meta:
        model = LeaderboardEntry
        fields = ['id', 'team', 'points']
