from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
import json
from textblob import TextBlob
from model import NeuralNet
from my_nltk import bag_of_words, tokenize
import torch
import requests

app = Flask(__name__)

# Load the model and other necessary data
with open('venv/job_intents1.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

sentiments = []  # List to store individual sentiments
messages = []

class Chatbox:
    def __init__(self):
        self.state = False

    def toggle_state(self):
        self.state = not self.state

    def get_response(self, msg):
        sentence = tokenize(msg)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(msg)
        sentiment = analysis.sentiment.polarity
        sentiments.append(sentiment)

        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    response = random.choice(intent['responses'])

                    # Add sentiment information to the response
                    return response

        # Add sentiment information to the default response
        default_response = "I do not understand..."
        return default_response

chatbox = Chatbox()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['user_message']
    bot_response = chatbox.get_response(user_message)

    if user_message.lower() == 'quit':
        # Separate response for 'quit' scenario
        final_emotion, music_suggestions = get_final_emotion_and_suggestions()
        return jsonify({'bot_response': final_emotion, 'music_suggestions': music_suggestions, 'redirect': True})

    messages.append({'name': 'User', 'message': user_message})
    messages.append({'name': 'Sam', 'message': bot_response})
    chatbox.toggle_state()  # Toggle state to show chatbox
    return jsonify({'bot_response': bot_response, 'redirect': False})

def get_final_emotion_and_suggestions():
    overall_sentiment = sum(sentiments) / len(sentiments)

    if overall_sentiment > 0:
        final_emotion = "What a fun to talk to you, your day went well as expected :)"
        music_suggestions = get_music_suggestions(1)
    elif overall_sentiment < 0:
        final_emotion = "Seems you are sad."
        music_suggestions = get_music_suggestions(-1)
    else:
        final_emotion = "Your day went well!"
        music_suggestions = get_music_suggestions(0)

    return final_emotion, music_suggestions

def get_music_suggestions(emotion):
    lastfm_api_key = "efd811825189b15bcf211cc55b1cbe40"
    base_url = "http://ws.audioscrobbler.com/2.0/"

    params = {
        'method': 'chart.gettoptracks',
        'api_key': lastfm_api_key,
        'format': 'json',
        'limit': 5  # You can adjust the limit as needed
    }

    if emotion > 0:
        params['method'] = 'tag.gettoptracks'
        params['tag'] = 'happy'
    elif emotion < 0:
        params['method'] = 'tag.gettoptracks'
        params['tag'] = 'Sad'

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'tracks' in data and 'track' in data['tracks']:
        tracks = data['tracks']['track']
        suggestions = [{'name': track['name'], 'artist': track['artist']['name'], 'url': track['url']} for track in tracks]
        return suggestions
    else:
        return [{"name": "Unable to fetch music suggestions.", "artist": "", "url": ""}]

@app.route('/result')
def result():
    # Render the result.html page with final emotion and suggested songs
    final_emotion, music_suggestions = get_final_emotion_and_suggestions()
    return render_template('result.html', final_emotion=final_emotion, music_suggestions=music_suggestions)

if __name__ == "__main__":
    app.run(debug=True)
