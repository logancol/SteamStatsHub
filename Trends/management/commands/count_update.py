from django.core.management.base import BaseCommand
import requests
from Trends.models import PlayerCount
from django.utils import timezone

class Command(BaseCommand):
    help = 'Update PlayerCount values in db'

    def handle(self, *args, **options):
        id_list = ['730', '10']  # Game IDS for cs source and cs2 for testing api calls from steam web api
        self.retrieve_pc_data(id_list)
        self.stdout.write(self.style.SUCCESS('Successfully updated player count data'))

    def retrieve_pc_data(self, id_list):
        api_key = '35882968C96E5A431D550FCEFA43C449'
        for game_id in id_list:
            game_name = "Unknown Game"  # will create a file/dict with id and game associations (unless these end up changing frequently?)
            url = f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={game_id}&key={api_key}'
            response = requests.get(url)
            

            self.stdout.write(f'Request URL: {url}')
            self.stdout.write(f'Response Text: {response.text}')
            
            if response.status_code == 200: #if successful
                try:
                    data = response.json()
                    player_count = data.get('response', {}).get('player_count', 0)
                    
                    PlayerCount.objects.update_or_create(
                        game_id=game_id,
                        defaults={'game_name': game_name, 'player_count': player_count, 'timestamp': timezone.now()}
                    )
                except ValueError: # error formatting into data json object
                    self.stdout.write(self.style.ERROR(f'Failed to parse JSON response for game ID {game_id}.'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to retrieve data for game ID {game_id}. Status code: {response.status_code}'))