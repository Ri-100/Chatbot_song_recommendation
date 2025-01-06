# Hi this is Rishav 👋

# Emotionally Aware Music Recommendation Chatbot 🎵🤖  

## Overview  
The Emotionally Aware Music Recommendation Chatbot is an AI-powered chatbot designed to recommend music based on the user’s emotional state. By analyzing text inputs to detect sentiments, the chatbot provides personalized music suggestions that align with the user’s mood.  

## Features  
- **Sentiment Analysis:** Identifies the user's mood through natural language processing (NLP).  
- **Music Recommendation:** Suggests songs or playlists tailored to the user's sentiment using the Last.fm API.  
- **Real-Time Interaction:** Provides quick and dynamic responses for a seamless user experience.  
- **Scalable Backend:** Built with Flask for efficient data handling and API integration.  



## Tech Stack  
- **Programming Languages:** Python, JavaScript  
- **Frameworks:** Flask, TextBlob  
- **APIs:** Last.fm API  
- **Frontend Tools:** HTML, CSS, JavaScript  
- **IDE/Tools:** Visual Studio Code, JSON  

## How It Works  
1. **Input Analysis:** The user interacts with the chatbot by entering text messages.  
2. **Sentiment Detection:** The chatbot uses TextBlob to classify the input as positive, negative, or neutral.  
3. **Music Recommendation:** Based on the detected sentiment, the chatbot queries the Last.fm API to retrieve relevant songs or playlists.  
4. **Response Generation:** The chatbot displays the music suggestions to the user.  

## Installation and Setup  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/Ri-100/Chatbot_song_recommendation.git  
   cd Chatbot_song_recommendation  
2. Install dependencies:
```bash  
pip install -r requirements.txt  

3. Set up the Last.fm API:
```bash  
 a Last.fm developer account.
Obtain your API key and update the config.py file with your key.

5.Run the Flask application:
python app.py  
Access the chatbot in your browser at http://localhost:5000.
