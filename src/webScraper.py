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
import re

from datetime import datetime
from entityType import EntityType

class MeetingRoomScraper:
    def __init__(self, driver_path: str, url: str):
        self.driver_path = driver_path
        self.url = url
        self.driver = self._initialize_webdriver()

    def _initialize_webdriver(self):
        print("Setting Chrome Options")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")

        print("Initialize the Chrome WebDriver")
        service = ChromeService(executable_path=self.driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def scrape(self) -> list[EntityType]:
        print("Getting page")
        self.driver.get(self.url)

        print("Sleeping 3 seconds")
        time.sleep(3)

        search = self.driver.find_elements(By.CLASS_NAME, 'item-block-content')
        all_booking_data = [element.text for element in search]

        entities = self._extract_entities(all_booking_data)

        print("Quit")
        self.driver.quit()

        return entities
    
    def _extract_entities(self, all_booking_data: list[str]) -> list[EntityType]:
        entities = []
        pattern = r'^(\d{2}:\d{2})\s(.*)\s-\s([^-].*\S)$'
        default_start_time = datetime(1900, 1, 1, 0, 0)

        for booking in all_booking_data:
            lines = booking.strip().splitlines()
            room_id = None
            location = None
            start_time = default_start_time
            organizer = "NA"
            booking_title = "NA"
            look_for_details = False

            for line in lines:
                if line.startswith("Meeting room"):
                    parts = line.split(" - ")
                    room_id = int(parts[0].split()[2])
                    location = parts[1]
                    look_for_details = True

                elif look_for_details and ":" in line:
                    match = re.match(pattern, line)
                    if match:
                        start_timestr = match.group(1)
                        booking_title = match.group(2)
                        organizer = match.group(3)
                        start_time = datetime.strptime(start_timestr, "%H:%M").time()
                        look_for_details = False
                elif look_for_details and "No booking" in line:
                    look_for_details = False

            if room_id and location:
                entity = EntityType(
                    PartitionKey="BWZ",
                    RowKey=f"MR_{room_id}_{datetime.now()}",
                    room=str(room_id),
                    start_time=start_time,
                    organizer=organizer,
                    title=booking_title
                )
                if start_time != default_start_time:
                    entities.append(entity)
                else:
                    print("Skipping")

        return entities
