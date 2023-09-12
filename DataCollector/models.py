# models.py
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class SportEvent(Base):
    __tablename__ = 'sport_events'

    event_id = Column(String, primary_key=True)
    event_start_time = Column(TIMESTAMP)
    sport_name = Column(String)
    category_name = Column(String)
    competition_name = Column(String)
    season_name = Column(String)
    stage_type = Column(String)
    stage_phase = Column(String)
    round_name = Column(String)
    best_of = Column(Integer)
    competitor_1_name = Column(String)
    competitor_1_country = Column(String)
    competitor_2_name = Column(String)
    competitor_2_country = Column(String)
    venue_name = Column(String)
    venue_city = Column(String)
    venue_country = Column(String)
    event_status = Column(String)
    match_status = Column(String)
    home_score = Column(Integer)
    away_score = Column(Integer)
    winner_id = Column(String)
