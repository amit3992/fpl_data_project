from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    try:
        # Get database connection details
        CONNECT_SUPABASE = os.getenv('CONNECT_SUPABASE', 'false').lower() == 'true'
        
        if CONNECT_SUPABASE:
            # Use Supabase connection
            DATABASE_URL = os.getenv('DIRECT_URL')
            if not DATABASE_URL:
                raise ValueError("DIRECT_URL not found in environment variables")
            print("Using Supabase connection...")
        else:
            # Use local PostgreSQL connection
            DB_USER = os.getenv('DB_USER', 'postgres')
            DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
            DB_HOST = os.getenv('DB_HOST', 'localhost')
            DB_PORT = os.getenv('DB_PORT', '5432')
            DB_NAME = os.getenv('DB_NAME', 'fpl_data')
            DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            print("Using local PostgreSQL connection...")

        print("Attempting to connect to database...")
        
        # Create SQLAlchemy engine
        engine = create_engine(DATABASE_URL)
        
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Test the connection with a simple query
        result = session.execute(text("SELECT version();"))
        version = result.scalar()
        print(f"Successfully connected to database!")
        print(f"Database version: {version}")
        
        # Test if we can access our tables
        print("\nChecking tables...")
        result = session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_name IN ('player_matrix', 'team_history', 'player');
        """))
        
        tables = [row[0] for row in result]
        print("Found tables:", tables)
        
        # Close the session
        session.close()
        
        return True
        
    except Exception as e:
        print(f"Error testing connection: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 