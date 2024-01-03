import random
import json
import requests
from textblob import TextBlob  # Import TextBlob for sentiment analysis

import torch
from model import NeuralNet
from my_nltk import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('venv\job_intents1.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

sentiments = []  # List to store individual sentiments

def get_response(msg):
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
        suggestions = [f"{track['name']} by {track['artist']['name']} - {track['url']}" for track in tracks]
        return suggestions
    else:
        return ["Unable to fetch music suggestions."]

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

    # Calculate overall sentiment
    overall_sentiment = sum(sentiments) / len(sentiments)

    # Print the final emotion
    print("\nFinal Emotion:")
    if overall_sentiment > 0:
        print("What a fun to talk to you, your day went well as expected :)")
        print("Here are some happy song suggestions😊:")
        music_suggestions = get_music_suggestions(1)
    elif overall_sentiment < 0:
        print("Seems you are sad.")
        print("Here are some suggestions for you🫂:")
        music_suggestions = get_music_suggestions(-1)
    else:
        print("Your day went well!")
        print("Here are some song suggestions🎶:")
        music_suggestions = get_music_suggestions(0)

    for suggestion in music_suggestions:
        print(suggestion)