#
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         symptoms = tracker.get_slot("symptoms")
#         if symptoms:
#             dispatcher.utter_message(text=f"Sorry to know about your {symptoms}")
#         else:
#             dispatcher.utter_message(text="Hello World!")
#
#         return []
