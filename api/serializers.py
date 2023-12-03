from rest_framework import serializers

from events.models import Event, Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'event', 'author', 'text']


class EventSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'event_date', 'price', 'presale', 'presale_tickets', 'sale_date', 'total_tickets', 'tickets_left', 'waiting_tickets', 'author', 'photo_url', 'comment_set']
