"""View module for handling requests about events"""

from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models import Game
from levelupapi.models import Gamer

class EventView(ViewSet):
    """Level up events view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single event 

        Returns:
              Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self, request):
        """Handle GET requests to get all events and events by game id

          Returns:
              Response -- JSON serialized list of game types and events by game id
        """
        events = Event.objects.all()
        
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns
            Respond -- JSON serialized event instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for an event
        
        Returns:
            Response -- Empty body with 204 status code
        """
        
        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):
        """JSON serializer for events"""
        class Meta:
            model = Event
            fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
            depth = 2 #awesome
            
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'game', 'description', 'date', 'time', 'organizer']  

      