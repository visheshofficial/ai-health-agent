import spacy
from spacy import displacy

nlp = spacy.load("en_ner_bionlp13cg_md")
text = "I have stomach ache and stomachache. also headache and head ache and headach" \
       "I also have diarrhea and dehydration. I have seen abdominal pain and Muscle weakness, " \
       " debilitation, impaired cognition, drool, pin-point pupils, " \
       " tremor resting, groggy, adverse reaction, adverse effect " \
       " i have neck pain , pain neck , back pain, dizzy spells, shooting pain, hyperemesis, dizziness," \
       " feces in rectum, prodrome, hypoproteinemia"
text = "i am feeling dizzy"
text = "skin irritation around the anus"

# text ="Anemia signs and symptoms vary depending on the cause. If the anemia is caused by a chronic disease, " \
#       "the disease can mask them, so that the anemia might be detected by tests for another condition., " \
#       "Depending on the causes of your anemia, you might have no symptoms. Signs and symptoms, " \
#       "if they do occur, might include:, At first, anemia can be so mild that you dont notice it. " \
#       "But symptoms worsen as anemia worsens. Make an appointment with your doctor if youre feeling fatigued and you dont know why." \
#       "Fatigue has many causes besides anemia, so dont assume that if youre tired you must be anemic. " \
#       "Some people learn that their hemoglobin is low, which indicates anemia, when they donate blood. " \
#       "If youre told that you cant donate because of low hemoglobin, make an appointment with your doctor." \
#       "Fatigue, Weakness, Pale or yellowish skin, Irregular heartbeats, Shortness of breath, Dizziness or lightheadedness, Chest pain, Cold hands and feet, Headaches"

# Create the Doc object
doc = nlp(text)
# extract entities
for ent in doc.ents:
    print(ent.text, ent.label_)
