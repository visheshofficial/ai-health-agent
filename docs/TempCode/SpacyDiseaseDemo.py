import spacy
from spacy import displacy

nlp = spacy.load("en_ner_bc5cdr_md")
text = "Skin changes are the only signs of acanthosis nigricans. Youll notice dark thickened velvety skin in body folds and creases  typically in your armpits groin and back of the neck. The skin changes usually appear slowly. The affected skin may also have an odor or itch. Consult your doctor if you notice changes in your skin  especially if the changes appear suddenly. You may have an underlying condition that needs treatment."


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
