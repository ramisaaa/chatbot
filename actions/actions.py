from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import os
import re

class ActionFindLaptop(Action):
    def name(self) -> Text:
        return "action_find_laptop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Load laptop dataset
        laptops_data = pd.read_csv("/home/ramisa/Documents/IMT/NLP/chatbot/data/datasets/laptops.csv")

        # Initialize variables
        brand = tracker.get_slot('brand')
        cpu = tracker.get_slot('cpu')
        ram = tracker.get_slot('ram')
        storage = tracker.get_slot('storage')
        budget = tracker.get_slot('budget')

        print(f"Brand: {brand}")
        print(f"CPU: {cpu}")
        print(f"RAM: {ram}")
        print(f"Storage: {storage}")
        print(f"Budget: {budget}")

        # Extract digits from RAM, Storage, and Budget
        ram_digits = re.search(r'\d+', ram).group() if ram else None
        storage_digits = re.search(r'\d+', storage).group() if storage else None
        budget_digits = re.search(r'\d+', budget).group() if budget else None

        # Apply filters based on user input
        filtered_laptops = laptops_data
        if brand:
            brand = str(brand)
            filtered_laptops = filtered_laptops[filtered_laptops['Brand'].str.lower() == brand.lower()]
        if cpu:
            cpu = str(cpu)
            filtered_laptops = filtered_laptops[filtered_laptops['CPU'].str.lower() == cpu.lower()]
        if ram_digits:
            filtered_laptops = filtered_laptops[filtered_laptops['RAM'] == int(ram_digits)]
        if storage_digits:
            filtered_laptops = filtered_laptops[filtered_laptops['Storage'] == int(storage_digits)]
        if budget_digits:
            filtered_laptops = filtered_laptops[filtered_laptops['Final Price'] <= float(budget_digits)]

        # Respond to the user with the search results
        if not filtered_laptops.empty:
            filtered_laptops = filtered_laptops.sort_values(by='Final Price', ascending=False)
            laptop_list = filtered_laptops[['Laptop', 'Final Price']].head(20)
            laptop_list['Final Price'] = laptop_list['Final Price'].astype(str)  # Convert to string for concatenation
            laptop_list['Combined'] = laptop_list['Laptop'] + ' - Price: $' + laptop_list['Final Price']
            laptop_list = laptop_list['Combined'].to_string(index=False)
            response = f"Here are some laptops that match your criteria:\n\n{laptop_list}"
        else:
            response = "Sorry, no laptops match your criteria. Please try adjusting your preferences."

        dispatcher.utter_message(response)

        return []