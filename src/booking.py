from sqlalchemy import Column, Integer, String, DateTime, Uuid, Time
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Booking(Base):
    __tablename__ = 'testbwz'
    
    bookingid = Column(Uuid(), primary_key=True)
    roomid = Column(Integer(), nullable=False)
    location = Column(String(50), nullable=False)
    starttime = Column(Time(), nullable=False)
    organizer = Column(String(50), nullable=False)
    remainingtime = Column(Time())
    bookingdate = Column(DateTime())
    
    def __init__(self, bookingID, room_id, location, start_time, organizer, remaining_time, date):
        self.bookingid = bookingID
        self.roomid = room_id
        self.location = location
        self.starttime = start_time
        self.organizer = organizer
        self.remainingtime = remaining_time
        self.bookingdate = date
    
    def __str__(self):
        return (f"Booking Details:\n"
                f"RoomID: {self.roomid}\n"
                f"Location: {self.location}\n"
                f"StartTime: {self.starttime}\n"
                f"Organizer: {self.organizer}\n"
                f"RemainingTime: {self.remainingtime}\n"
                f"Date: {self.bookingdate}\n")