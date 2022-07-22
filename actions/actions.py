from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class RememberSymptoms(Action):

    def name(self) -> Text:
        return "action_remember_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("inside action_remember_symptoms ")
        diseases: list = list(tracker.get_latest_entity_values("DISEASE"))
        if diseases:
            print("Symptoms from the last message are: :" + str(diseases))
        # if tracker.get_intent_of_latest_message() == "inform_symptoms":
        #     entities = tracker.latest_message['entities']
        #     print(entities)
        #     # if symptoms:
        #     #     dispatcher.utter_message(text=f"Sorry to know about your {symptoms}")
        #     # else:
        #     #     dispatcher.utter_message(text="Hello World!")

        return []
