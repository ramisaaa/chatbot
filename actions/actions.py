from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

class ActionFindLaptop(Action):
    def name(self) -> Text:
        return "ac"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Load your laptop dataset
        laptops_data = pd.read_csv("../data/datasets/laptops.csv")

        # Extract user preferences from the entities
        brand = tracker.get_slot('brand')
        cpu = tracker.get_slot('CPU')  # Assuming 'CPU' is the entity for the CPU
        ram = tracker.get_slot('RAM')
        storage = tracker.get_slot('Storage')  # Assuming 'Storage' is the entity for storage
        budget = tracker.get_slot('budget')

        # Apply filters based on user input
        filtered_laptops = laptops_data
        if brand:
            filtered_laptops = filtered_laptops[filtered_laptops['Brand'].str.lower() == brand.lower()]
        if cpu:
            filtered_laptops = filtered_laptops[filtered_laptops['CPU'].str.lower() == cpu.lower()]
        if ram:
            filtered_laptops = filtered_laptops[filtered_laptops['RAM'] == int(ram)]
        if storage:
            # Assuming 'Storage' is a numerical value, adjust the condition accordingly
            filtered_laptops = filtered_laptops[filtered_laptops['Storage'] >= int(storage)]
        if budget:
            filtered_laptops = filtered_laptops[filtered_laptops['Final Price'] <= float(budget)]

        # Respond to the user with the search results
        if not filtered_laptops.empty:
            laptop_list = filtered_laptops[['Brand', 'Model', 'Final Price']].to_string(index=False)
            response = f"Here are some laptops that match your criteria:\n\n{laptop_list}"
        else:
            response = "Sorry, no laptops match your criteria. Please try adjusting your preferences."

        dispatcher.utter_message(response)

        # Return the top N laptops as suggestions
        suggestions = filtered_laptops.head(5).to_dict('records')
        return suggestions
