import json
from watson_developer_cloud import ToneAnalyzerV3
import matplotlib.pyplot as plt


tone_analyzer = ToneAnalyzerV3(
   username='8c8c2845-4efe-4967-a3b1-55852d495815',
   password='z6EdeWkWiEtt',
   version='2016-05-19')

sentence = raw_input("Enter a sentence to have analyzed: ")


json_response = tone_analyzer.tone(text=sentence)

emotion = json_response["document_tone"]["tone_categories"][0]
language = json_response["document_tone"]["tone_categories"][1]
social = json_response["document_tone"]["tone_categories"][2]

print(emotion)

def make_pie_charts(json):
    category_name = json["category_name"]
    print("Category: " + category_name)
    labels = []
    scores = []
    for obj in json["tones"]:
        labels.append(obj["tone_name"])
        scores.append(obj["score"])

    plt.pie(scores, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title(category_name)
    plt.show()


make_pie_charts(emotion)
make_pie_charts(language)
make_pie_charts(social)
