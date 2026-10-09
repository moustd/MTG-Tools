import os
from models import CardRecord

DATABASE_URL = os.getenv("MTG_DATABASE_URL", "sqlite:///mtg_cards.db")

def create_tables():
    """Create database tables using SQLAlchemy."""
    try:
        from sqlalchemy import create_engine, Column, Integer, String, Float
        from sqlalchemy.ext.declarative import declarative_base
        
        Base = declarative_base()
        
        class CardRecordModel(Base):
            __tablename__ = 'card_records'
            id = Column(Integer, primary_key=True)
            name = Column(String(255))
            scryfall_id = Column(String(100))
            cost = Column(String(50))
            type_line = Column(String(100))
            rarity = Column(String(50))
            power_toughness = Column(String(50))
            idhrec_rank = Column(Integer)
            idhrec_inclusion_rate = Column(Float)
        
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        print(f"Database tables created at: {DATABASE_URL}")
        
    except Exception as e:
        print(f"Error creating database tables: {e}")

if __name__ == "__main__":
    create_tables()