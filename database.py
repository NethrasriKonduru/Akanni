from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Import the Base from models.base
from models.base import Base

# Load environment variables
load_dotenv()

# Database configuration
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'rootpass')
DB_HOST = os.getenv('DB_HOST', 'localhost')  # 'postgres' when running in Docker network
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'akkani_db')

# Check if running in Docker
IS_DOCKER = os.environ.get('DOCKER_CONTAINER', False)
if IS_DOCKER:
    DB_HOST = 'postgres'  # Docker service name as host when in Docker network

def ensure_database_exists():
    """Ensure the database exists, create it if it doesn't"""
    db_created = False
    try:
        # Connect to the default 'postgres' database to check if our database exists
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        
        with conn.cursor() as cursor:
            # Check if database exists
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
            exists = cursor.fetchone()
            
            if not exists:
                print(f"Creating database: {DB_NAME}")
                cursor.execute(f"CREATE DATABASE {DB_NAME}")
                print(f"Database {DB_NAME} created successfully")
                db_created = True
            
    except Exception as e:
        print(f"Error checking/creating database: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
    
    return db_created

def create_tables():
    """Create all tables in the database"""
    try:
        print("Creating database tables...")
        # Import models to ensure they are registered with SQLAlchemy's metadata
        from models.user import User
        from models.oauth_token import OAuthToken
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

# Ensure database exists before creating engine
db_was_created = ensure_database_exists()

# Create database URL with psycopg2
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
    echo=True  # Enable SQL query logging for debugging
)

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if the database was just created or if tables don't exist
if db_was_created:
    create_tables()

# Create database URL with psycopg2
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
    echo=True  # Enable SQL query logging for debugging
)

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()