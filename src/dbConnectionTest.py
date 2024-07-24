from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Import the Base and Booking class definitions
from booking import Base, Booking

import uuid

def setup_database():
    url = URL.create(
        drivername="postgresql",
        username="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        database="postgres"
    )
   
    try:
        engine = create_engine(url)
        
        # Create all tables defined in the Base
        Base.metadata.create_all(engine)
        
        # Create a session factory
        Session = sessionmaker(bind=engine)
        
        with engine.connect() as connection:
            print("Successfully connected to the database.")
           
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        print(f"Tables in the database: {table_names}")
       
        if 'testbwz' in table_names:
            print("The 'testbwz' table exists.")
            columns = [col['name'] for col in inspector.get_columns('testbwz')]
            print(f"Columns in 'testbwz': {columns}")
        else:
            print("The 'testbwz' table does not exist.")
        
        return Session
       
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def add_sample_data(session):
    # Create a sample booking
    current_time = datetime.now()
    end_time = current_time + timedelta(minutes=60)
    
    uid4 = uuid.uuid4()
    sample_booking = Booking(
        bookingID=uid4,
        room_id=101,
        location="Conference Room B",
        start_time=current_time,
        organizer="John Doe",
        remaining_time=end_time,  # Now this is a datetime object
        date=current_time.date()
    )
    
    # Add the sample booking to the session and commit
    session.add(sample_booking)
    session.commit()
    print("Sample booking added successfully.")

if __name__ == "__main__":
    Session = setup_database()
    if Session:
        session = Session()
        add_sample_data(session)
        session.close()