import json
from watson_developer_cloud import ToneAnalyzerV3
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pyaudio
import wave
import requests

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
FILE_NAME = "sentence.wav"

p = pyaudio.PyAudio()


# language = json_response["document_tone"]["tone_categories"][1]
# social = json_response["document_tone"]["tone_categories"][2]


def make_pie_charts(json_array):
    grid = GridSpec(1,2)
    color_array = ['steelblue', 'crimson', 'darkseagreen', 'darkcyan', 'orange']
    pos = 0
    color_pos = 0
    for category in json_array:
        category_name = category["category_name"]
        if (category_name != "Language Tone"):
            labels = []
            scores = []
            colors = []
            for obj in category["tones"]:
                labels.append(obj["tone_name"])
                scores.append(obj["score"])
                colors.append(color_array[color_pos])
                color_pos += 1
            color_pos = 0

            plt.subplot(grid[0,pos], aspect=1)
            plt.pie(scores, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
            plt.title(category_name)
            pos += 1
    plt.show()

def record_audio(time):

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)

    print "...Recording"
    frames = []
    for i in range(0, 44100 / chunk * time):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print ("Stop talking now")
    return frames

def record_to_file(path, frames):
    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

def analyze_tone(sentence):
    tone_analyzer = ToneAnalyzerV3(
       username='8c8c2845-4efe-4967-a3b1-55852d495815',
       password='z6EdeWkWiEtt',
       version='2016-05-19')

    # sentence = raw_input("Enter a sentence to have analyzed: ")
    json_response = tone_analyzer.tone(text=sentence)
    categories = json_response["document_tone"]["tone_categories"]
    return categories

def post_audio(filename):

    url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
    username = 'eda72472-1240-40e4-97fd-5753985fbe1a'
    password = '67xzwJ7ibn1q'

    headers={'Content-Type': 'audio/wav'}

    audio = open(filename, 'rb')
    response = requests.post(url, data=audio, headers=headers, auth=(username, password))
    json_response = json.loads(response.text)
    text = json_response["results"][0]["alternatives"][0]["transcript"]
    return text


time = raw_input("How many seconds to record: ")
data = record_audio(int(time))

record_to_file(FILE_NAME, data)
response = post_audio(FILE_NAME)
print(response)
categories = analyze_tone(response)
make_pie_charts(categories)
