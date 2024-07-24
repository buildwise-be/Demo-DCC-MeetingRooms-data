# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:24:46 2024

@author: aca
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from booking import Booking

import re

# Helper function to convert 'Available in' time to minutes
def convert_to_minutes(available_in):
    if "hour" in available_in:
        return int(available_in.split()[2]) * 60
    else:
        return int(available_in.split()[2])

def test_regex(pattern):
    test_strings = [
    "08:00 Feedback-momenten - Blop HR - Jon Snow",
    "09:30 Product Review - Phase 1 - Team Discussion - Alice Johnson",
    "14:15 Lunch - Break - Bob Smith",
    "15:45 Project Update - Marketing Strategy - Mary-Jane Watson",
    "17:00 Client Meeting - Important Notes - Jean-Claude Van Damme",
    "08:00 Feedback-momenten - Weevo HR - Floris Caluwaerts",
    "15:27 mfkldsgh-kk - stuff - Martha"
    ]

    for test_string in test_strings:
        match = re.match(pattern, test_string)
        
        if match:
            time = match.group(1)
            event = match.group(2)
            person = match.group(3)
            
            print(f"Time: {time}")
            print(f"Event: {event}")
            print(f"Person: {person}")
            print("---")
        else:
            print(f"No match found for: {test_string}")
            print("---")

PATH = './webdrivers/chromedriver'

# Set up Edge options
print("Setting Options")
chrome_options = Options()
chrome_options.add_argument('--headless')

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

bindingSearch = driver.find_elements(By.CLASS_NAME, 'ng-binding')
scopeSearch = driver.find_elements(By.CLASS_NAME, 'ng-scope')
bindings = [element.text for element in bindingSearch]
scopes = [element.text for element in scopeSearch]

all_booking_data = bindings + scopes

# Initialize the lists
room_ids = []
locations = []
start_hours = []
organizers = []
remaining_times = []
booking_titles = []
bookings = []

# Regex to capture fields
pattern = r'^(\d{2}:\d{2})\s(.*)\s-\s([^-].*\S)$'
#test_regex(pattern)

# Iterate through the meeting rooms
i = 0
look_for_details = False
look_for_remainingTime = False

while i < len(all_booking_data):    
    line = all_booking_data[i].strip()
    #print(line)
    if line.startswith("Meeting room"):
        # Initialize defaults
        start_hour = "00:00"
        organizer = "NA"
        remaining_time = 0
        booking_title = "NA"
        
        # Extract room ID and location
        parts = line.split(" - ")
        room_id = int(parts[0].split()[2])
        location = parts[1]
        '''
        if (look_for_details):
            start_hours.append(start_hour)
            organizers.append(organizer)
            booking_titles.append(booking_title)
            
        if (look_for_remainingTime):
            remaining_times.append(remaining_time)
        '''
        room_ids.append(room_id)
        locations.append(location)
        
        look_for_details = True

    # Check next line for meeting details
    if look_for_details:
        print(line)
    if look_for_details and ":" in line:
        match = re.match(pattern, line)
        if match:
            start_hour = match.group(1)
            booking_title = match.group(2)
            organizer = match.group(3)
            
            start_hours.append(start_hour)
            organizers.append(organizer)
            booking_titles.append(booking_title)
            
            look_for_details = False
            look_for_remainingTime = True
    elif look_for_details and "No booking" in line:
        start_hours.append(start_hour)
        organizers.append(organizer)
        booking_titles.append(booking_title)
        
        look_for_details = False
        look_for_remainingTime = True
            
    # Check for remaining time
    if i < len(all_booking_data) and all_booking_data[i].startswith("Available in") and look_for_remainingTime:
        remaining_time = convert_to_minutes(all_booking_data[i].strip())
        remaining_times.append(remaining_time)
        look_for_remainingTime = False
        print("remaining_time: " + str(remaining_time))
    elif i < len(all_booking_data) and all_booking_data[i].startswith("Now available") and look_for_remainingTime:
        remaining_times.append(remaining_time)

    i += 1

print("------------")
print(len(room_ids))
print(len(locations))
print(len(start_hours))
print(len(organizers))
print(len(remaining_times))
print("------------")


i = 0
while i < len(room_ids):
    booking = Booking(room_ids[i], locations[i], start_hours[i], organizers[i], remaining_times[i])
    bookings.append(booking)
    print(i)
    i += 1


# Print the lists
print("Room IDs:", room_ids)
print("Locations:", locations)
print("Start Hours:", start_hours)
print("Organizers:", organizers)
print("Remaining Times:", remaining_times)
print("Titles: ", booking_titles)

print("Quit")
driver.quit()
