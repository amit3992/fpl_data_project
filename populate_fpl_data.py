import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_tables import Base, PlayerMatrix, TeamHistory, Player
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import re
from collections import defaultdict

# Load environment variables
load_dotenv()

# Get database connection details
CONNECT_SUPABASE = os.getenv('CONNECT_SUPABASE', 'false').lower() == 'true'

if CONNECT_SUPABASE:
    # Use Supabase connection
    DATABASE_URL = os.getenv('DIRECT_URL')
    if not DATABASE_URL:
        raise ValueError("DIRECT_URL not found in environment variables")
else:
    # Use local PostgreSQL connection
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'fpl_data')
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def extract_season_from_url(url):
    """Extract season from URL using regex"""
    match = re.search(r'/season/(\d{4}-\d{2})', url)
    if match:
        return match.group(1)
    raise ValueError("Could not extract season from URL")

def fetch_fpl_data(url):
    """Fetch data from Fantasy Nutmeg API"""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def process_gameweek_data(data):
    """Process gameweek data from the API response"""
    gameweek_data = defaultdict(dict)
    
    # Process fixture data
    if 'dd_agg_fixture' in data:
        for fixture in data['dd_agg_fixture']:
            fixture_name = fixture['fixture']
            count = fixture['count']
            # Extract team and home/away from fixture name (e.g., "LEI(H)" -> "LEI", "H")
            team = fixture_name[:-3]
            location = fixture_name[-2]
            gameweek_data[team][location] = count
    
    # Process player data
    if 'dd_agg_player' in data:
        for player in data['dd_agg_player']:
            player_name = player['player']
            count = player['count']
            gameweek_data[player_name]['count'] = count
    
    return gameweek_data

def populate_player_matrix(data, season):
    """Populate player_matrix table"""
    if 'matrix' in data:
        for player_data in data['matrix']:
            web_name = player_data.get('web_name')
            player_gw_data = player_data.get('gw_points', {})
            
            # Create base player data
            player = PlayerMatrix(
                web_name=web_name,
                season=season,
                team_name=player_data.get('team_name'),
                position=player_data.get('position'),
                total_points=player_data.get('total_points'),
            )
            
            # Add gameweek points
            for gw in range(1, 39):
                gw_key = f'gw_{gw}'
                setattr(player, gw_key, player_gw_data.get(str(gw)))
            
            session.merge(player)

def populate_team_history(data, season):
    """Populate team_history table"""
    if 'team_history' in data:
        for team_data in data['team_history']:
            team = TeamHistory(
                team_id=team_data.get('team_id'),
                season=season,
                team_name=team_data.get('team_name'),
                total_points=team_data.get('total_points'),
                goals=team_data.get('goals'),
                assists=team_data.get('assists'),
                clean_sheets=team_data.get('clean_sheets'),
                goals_conceded=team_data.get('goals_conceded'),
                home_goals_scored=team_data.get('home_goals_scored'),
                home_goals_conceded=team_data.get('home_goals_conceded'),
                away_goals_scored=team_data.get('away_goals_scored'),
                away_goals_conceded=team_data.get('away_goals_conceded'),
                own_goals=team_data.get('own_goals'),
                penalties_missed=team_data.get('penalties_missed'),
                penalties_saved=team_data.get('penalties_saved'),
                red_cards=team_data.get('red_cards'),
                yellow_cards=team_data.get('yellow_cards'),
                in_dreamteam=team_data.get('in_dreamteam'),
                xG=team_data.get('xG'),
                xA=team_data.get('xA'),
                xGI=team_data.get('xGI'),
                xGC=team_data.get('xGC'),
                xG5=team_data.get('xG5'),
                xGC5=team_data.get('xGC5')
            )
            session.merge(team)

def populate_player(data, season):
    """Populate player table"""
    if 'history' in data:
        for player_data in data['history']:
            # Convert date strings to datetime objects if they exist
            birth_date = None
            if player_data.get('birth_date'):
                birth_date = datetime.strptime(player_data['birth_date'], '%Y-%m-%d').date()
            
            team_join_date = None
            if player_data.get('team_join_date'):
                team_join_date = datetime.strptime(player_data['team_join_date'], '%Y-%m-%d').date()
            
            news_added = None
            if player_data.get('news_added'):
                news_added = datetime.strptime(player_data['news_added'], '%Y-%m-%dT%H:%M:%S.%fZ')

            player = Player(
                id=player_data.get('id'),
                season=season,
                web_name=player_data.get('web_name'),
                first_name=player_data.get('first_name'),
                second_name=player_data.get('second_name'),
                position=player_data.get('position'),
                team=player_data.get('team'),
                team_code=player_data.get('team_code'),
                team_name=player_data.get('team_name'),
                birth_date=birth_date,
                team_join_date=team_join_date,
                status=player_data.get('status'),
                now_cost=player_data.get('now_cost'),
                total_points=player_data.get('total_points'),
                minutes=player_data.get('minutes'),
                goals_scored=player_data.get('goals_scored'),
                assists=player_data.get('assists'),
                clean_sheets=player_data.get('clean_sheets'),
                goals_conceded=player_data.get('goals_conceded'),
                own_goals=player_data.get('own_goals'),
                penalties_saved=player_data.get('penalties_saved'),
                penalties_missed=player_data.get('penalties_missed'),
                yellow_cards=player_data.get('yellow_cards'),
                red_cards=player_data.get('red_cards'),
                saves=player_data.get('saves'),
                bonus=player_data.get('bonus'),
                bps=player_data.get('bps'),
                influence=player_data.get('influence'),
                creativity=player_data.get('creativity'),
                threat=player_data.get('threat'),
                ict_index=player_data.get('ict_index'),
                expected_goals=player_data.get('expected_goals'),
                expected_assists=player_data.get('expected_assists'),
                expected_goal_involvements=player_data.get('expected_goal_involvements'),
                expected_goals_conceded=player_data.get('expected_goals_conceded'),
                form=player_data.get('form'),
                points_per_game=player_data.get('points_per_game'),
                selected_by_percent=player_data.get('selected_by_percent'),
                transfers_in=player_data.get('transfers_in'),
                transfers_out=player_data.get('transfers_out'),
                event_points=player_data.get('event_points'),
                news=player_data.get('news'),
                news_added=news_added,
                can_select=player_data.get('can_select'),
                can_transact=player_data.get('can_transact'),
                chance_of_playing_this_round=player_data.get('chance_of_playing_this_round'),
                chance_of_playing_next_round=player_data.get('chance_of_playing_next_round'),
                removed=player_data.get('removed'),
                photo=player_data.get('photo'),
                opta_code=player_data.get('opta_code')
            )
            session.merge(player)

def main():
    try:
        # API URL
        url = "https://www.fantasynutmeg.com/api/history/season/2022-23"
        
        # Extract season from URL
        season = extract_season_from_url(url)
        print(f"Processing data for season: {season}")
        
        # Fetch data from API
        data = fetch_fpl_data(url)
        
        # Print the structure of the data to understand what we're working with
        print("Available data keys:", data.keys())
        
        # Populate tables
        populate_player_matrix(data, season)
        populate_team_history(data, season)
        populate_player(data, season)
        
        # Commit changes
        session.commit()
        print("Data successfully populated!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main() 