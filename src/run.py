# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:24:46 2024

@author: aca
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from sqlalchemy import inspect

import time
import uuid
import re
from datetime import datetime

from booking import Booking
from database import Base, engine, Session

# Helper function to convert 'Available in' time to minutes
def convert_to_minutes(available_in):
    if "hour" in available_in:
        return int(available_in.split()[2]) * 60
    else:
        return int(available_in.split()[2])

# Get current time as a time struct
current_time = time.localtime()

# Format the time struct into a string
formatted_date = time.strftime("%Y-%m-%d", current_time)
print("Current date: " + formatted_date)

PATH = '../webdrivers/chromedriver'

# Set up Chrome options
print("Setting Options")
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")  # This can help with the DevTools issue

# Initialize the Edge WebDriver
print("Initialize the Chrome WebDriver")
service = ChromeService(executable_path=PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the website
url = 'https://t1b.gobright.cloud/portal/#/loginDisplay/117525992268228746302400058579894172338389585'
print("getting page")
driver.get(url)

# Wait for the page to load (optional)
print("sleep 3 sec")
time.sleep(3)

print(driver.title)

search = driver.find_elements(By.CLASS_NAME, 'item-block-content')
all_booking_data = [element.text for element in search]

# Initialize the lists
room_ids = []
locations = []
start_times = []
organizers = []
remaining_times = []
booking_titles = []
bookings = []

# Regex to capture fields
pattern = r'^(\d{2}:\d{2})\s(.*)\s-\s([^-].*\S)$'

# Iterate through the meeting rooms
i = 0
look_for_details = False
look_for_remainingTime = False

while i < len(all_booking_data):    
    booking = all_booking_data[i].strip()
    lines = booking.splitlines()
    j = 0
    while j < len(lines):
        line = lines[j]
        if line.startswith("Meeting room"):
            # Initialize defaults
            start_time = datetime(1900,1,1,0,0)
            organizer = "NA"
            remaining_time = datetime(1900,1,1,0,0)
            booking_title = "NA"
            
            # Extract room ID and location
            parts = line.split(" - ")
            room_id = int(parts[0].split()[2])
            location = parts[1]

            room_ids.append(room_id)
            locations.append(location)
            
            look_for_details = True

        # Check next line for meeting details   
        if look_for_details and ":" in line:
            match = re.match(pattern, line)
            if match:
                start_timestr = match.group(1)
                booking_title = match.group(2)
                organizer = match.group(3)
                
                start_time = datetime.strptime(start_timestr, "%H:%M").time()
                start_times.append(start_time)
                organizers.append(organizer)
                booking_titles.append(booking_title)
                
                look_for_details = False
                look_for_remainingTime = True
        elif look_for_details and "No booking" in line:
            start_times.append(start_time)
            organizers.append(organizer)
            booking_titles.append(booking_title)
            
            look_for_details = False
            look_for_remainingTime = True
                
        # Check for remaining time
        if i < len(all_booking_data) and line.startswith("Available in") and look_for_remainingTime:
            remaining_time = convert_to_minutes(line.strip())
            remaining_times.append(remaining_time)
            look_for_remainingTime = False
        elif i < len(all_booking_data) and (line.startswith("Now available") or line.startswith("Next")) and look_for_remainingTime:
            remaining_times.append(remaining_time)
            look_for_remainingTime = False


        j += 1
    i += 1

i = 0
while i < len(room_ids):
    uid4 = uuid.uuid4()
    line = Booking(uid4, room_ids[i], locations[i], start_times[i], organizers[i], remaining_times[i], formatted_date)
    bookings.append(line)
    i += 1

# Print Bookings summary
print("Bookings summary")
for b in range(len(bookings)):
    print(bookings[b])

# Interact with DB
Base.metadata.create_all(engine)
with engine.connect() as connection:
    print("Successfully connected to the database.")

inspector = inspect(engine)
table_names = inspector.get_table_names()
print(f"Tables in the database: {table_names}")

session = Session()

for b in range(len(bookings)):
    session.add(bookings[b])
session.commit()

print("Quit")
driver.quit()