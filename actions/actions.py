from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import os


class ActionFindLaptop(Action):
    def name(self) -> Text:
        return "action_find_laptop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load your laptop dataset
        laptops_data = pd.read_csv("/home/ramisa/Documents/IMT/NLP/chatbot/data/datasets/laptops.csv")

        # Extract user preferences from the entities
        user_entities = tracker.latest_message.get("entities", [])

        # Initialize variables
        brand = None
        cpu = None
        ram = None
        storage = None
        budget = None

        # Extract values from entities
        for entity in user_entities:
            if entity["entity"] == "brand":
                brand = entity["value"]
            elif entity["entity"] == "CPU":
                cpu = entity["value"]
            elif entity["entity"] == "RAM":
                ram = entity["value"]
            elif entity["entity"] == "Storage":
                storage = entity["value"]
            elif entity["entity"] == "budget":
                budget = entity["value"]

        # Apply filters based on user input
        filtered_laptops = laptops_data
        if brand:
            filtered_laptops = filtered_laptops[filtered_laptops['Brand'].str.lower() == brand.lower()]
        if cpu:
            filtered_laptops = filtered_laptops[filtered_laptops['CPU'].str.lower() == cpu.lower()]
        if ram:
            filtered_laptops = filtered_laptops[filtered_laptops['RAM'] == int(ram)]
        if storage:
            filtered_laptops = filtered_laptops[filtered_laptops['Storage'] >= int(storage)]
        if budget:
            filtered_laptops = filtered_laptops[filtered_laptops['Final Price'] <= float(budget)]

        # Respond to the user with the search results
        if not filtered_laptops.empty:
            laptop_list = filtered_laptops[['Laptop']].head(5).to_string(index=False)
            response = f"Here are some laptops that match your criteria:\n\n{laptop_list}"
        else:
            response = "Sorry, no laptops match your criteria. Please try adjusting your preferences."

        dispatcher.utter_message(response)

        # Return the top N laptops as suggestions
        suggestions = filtered_laptops.head(5).to_dict('records')
        return suggestions
