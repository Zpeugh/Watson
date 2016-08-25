import json
from watson_developer_cloud import ToneAnalyzerV3
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pyaudio
import wave


tone_analyzer = ToneAnalyzerV3(
   username='8c8c2845-4efe-4967-a3b1-55852d495815',
   password='z6EdeWkWiEtt',
   version='2016-05-19')

sentence = raw_input("Enter a sentence to have analyzed: ")

json_response = tone_analyzer.tone(text=sentence)

categories = json_response["document_tone"]["tone_categories"]
# language = json_response["document_tone"]["tone_categories"][1]
# social = json_response["document_tone"]["tone_categories"][2]


def make_pie_charts(json_array):
    grid = GridSpec(1,3)
    color_array = ['steelblue', 'crimson', 'darkseagreen', 'darkcyan', 'orange']
    pos = 0
    color_pos = 0
    for category in json_array:
        category_name = category["category_name"]
        print("Category: " + category_name)
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

def record_audio():

    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)

    print "* recording"
    for i in range(0, 44100 / chunk * RECORD_SECONDS):
        data = stream.read(chunk)

        # check for silence here by comparing the level with 0 (or some threshold) for
        # the contents of data.
        # then write data or not to a file

    stream.stop_stream()
    stream.close()
    p.terminate()
    print(data)
    return data

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record_audio()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


data = record_audio()
record_to_file("sentence.wav", data)
make_pie_charts(categories)
