from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Numeric, Double, Text, TIMESTAMP, PrimaryKeyConstraint, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv

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
Base = declarative_base()

class PlayerMatrix(Base):
    __tablename__ = 'player_matrix'
    
    web_name = Column(Text, nullable=False)
    season = Column(Text, nullable=False)
    team_name = Column(Text, nullable=False)
    position = Column(Text, nullable=False)
    total_points = Column(Integer, nullable=False)
    
    # Gameweek columns
    gw_1 = Column(Integer)
    gw_2 = Column(Integer)
    gw_3 = Column(Integer)
    gw_4 = Column(Integer)
    gw_5 = Column(Integer)
    gw_6 = Column(Integer)
    gw_7 = Column(Integer)
    gw_8 = Column(Integer)
    gw_9 = Column(Integer)
    gw_10 = Column(Integer)
    gw_11 = Column(Integer)
    gw_12 = Column(Integer)
    gw_13 = Column(Integer)
    gw_14 = Column(Integer)
    gw_15 = Column(Integer)
    gw_16 = Column(Integer)
    gw_17 = Column(Integer)
    gw_18 = Column(Integer)
    gw_19 = Column(Integer)
    gw_20 = Column(Integer)
    gw_21 = Column(Integer)
    gw_22 = Column(Integer)
    gw_23 = Column(Integer)
    gw_24 = Column(Integer)
    gw_25 = Column(Integer)
    gw_26 = Column(Integer)
    gw_27 = Column(Integer)
    gw_28 = Column(Integer)
    gw_29 = Column(Integer)
    gw_30 = Column(Integer)
    gw_31 = Column(Integer)
    gw_32 = Column(Integer)
    gw_33 = Column(Integer)
    gw_34 = Column(Integer)
    gw_35 = Column(Integer)
    gw_36 = Column(Integer)
    gw_37 = Column(Integer)
    gw_38 = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('web_name', 'season'),
    )

class TeamHistory(Base):
    __tablename__ = 'team_history'
    
    team_id = Column(Integer, nullable=False)
    season = Column(Text, nullable=False)
    team_name = Column(Text, nullable=False)
    total_points = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    clean_sheets = Column(Integer)
    goals_conceded = Column(Integer)
    home_goals_scored = Column(Integer)
    home_goals_conceded = Column(Integer)
    away_goals_scored = Column(Integer)
    away_goals_conceded = Column(Integer)
    own_goals = Column(Integer)
    penalties_missed = Column(Integer)
    penalties_saved = Column(Integer)
    red_cards = Column(Integer)
    yellow_cards = Column(Integer)
    in_dreamteam = Column(Integer)
    xG = Column(Double)
    xA = Column(Double)
    xGI = Column(Double)
    xGC = Column(Double)
    xG5 = Column(Double)
    xGC5 = Column(Double)

    __table_args__ = (
        PrimaryKeyConstraint('team_id', 'season'),
    )

class Player(Base):
    __tablename__ = 'player'
    
    id = Column(Integer, nullable=False)
    season = Column(Text, nullable=False)
    web_name = Column(Text, nullable=False)
    first_name = Column(Text)
    second_name = Column(Text)
    position = Column(Text)
    team = Column(Integer)
    team_code = Column(Integer)
    team_name = Column(Text)
    birth_date = Column(Date)
    team_join_date = Column(Date)
    status = Column(Text)
    now_cost = Column(Numeric(4,2))
    total_points = Column(Integer)
    minutes = Column(Integer)
    goals_scored = Column(Integer)
    assists = Column(Integer)
    clean_sheets = Column(Integer)
    goals_conceded = Column(Integer)
    own_goals = Column(Integer)
    penalties_saved = Column(Integer)
    penalties_missed = Column(Integer)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    saves = Column(Integer)
    bonus = Column(Integer)
    bps = Column(Integer)
    influence = Column(Text)
    creativity = Column(Text)
    threat = Column(Text)
    ict_index = Column(Text)
    expected_goals = Column(Text)
    expected_assists = Column(Text)
    expected_goal_involvements = Column(Text)
    expected_goals_conceded = Column(Text)
    form = Column(Text)
    points_per_game = Column(Text)
    selected_by_percent = Column(Text)
    transfers_in = Column(Integer)
    transfers_out = Column(Integer)
    event_points = Column(Integer)
    news = Column(Text)
    news_added = Column(TIMESTAMP)
    can_select = Column(Boolean)
    can_transact = Column(Boolean)
    chance_of_playing_this_round = Column(Integer)
    chance_of_playing_next_round = Column(Integer)
    removed = Column(Boolean)
    photo = Column(Text)
    opta_code = Column(Text)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'season'),
    )

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully!") 