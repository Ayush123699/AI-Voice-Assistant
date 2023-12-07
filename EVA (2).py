import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import os
import webbrowser
import datetime
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import wikipedia
import pywhatkit



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
def get_joke():
    joke_url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(joke_url)
    joke_data = response.json()

    if joke_data['type'] == 'twopart':
        return f"{joke_data['setup']} {joke_data['delivery']}"
    else:
        return joke_data['joke']
def get_weather():
    # You can replace 'YOUR_API_KEY' with a valid OpenWeatherMap API key
    api_key = '1d90bf712f3617feb1b372bcf8cfd9ad'
    city = 'Talcher'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(base_url)
    weather_data = response.json()

    if 'cod' in weather_data and weather_data['cod'] == '404':
        return 'Weather information not available.'
    
    description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    temperature_celsius = round(temperature - 273.15, 2)
    return f'The weather in {city} is {description}. The temperature is {temperature_celsius} degrees Celsius.'

def get_news():
    # You can 8'
    api_key='d4c5416fd42d4bfe81d5a09e904b0f04'
    url = f'https://newsapi.org/v2/everything?domains=wsj.com&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()

    if 'status' in news_data and news_data['status'] == 'ok':
        articles = news_data['articles']
        news_list = [article['title'] for article in articles]
        return '\n'.join(news_list)
    else:
        return 'News information not available.'
def get_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.WikipediaException as e:
        return f"Sorry, I couldn't find information about {topic} on Wikipedia."
def  search_music(query):
    pywhatkit.playonyt(query)

def send_email(subject, body):
    # Replace these placeholders with your own email and SMTP server details
    sender_email = 'nayaknishthanivedita@gmail.com'
    sender_password = 'nishtha@18'
    receiver_email = 'jsprateekk@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
       
def send_whatsapp_message(contact, message, hours, minutes):
    pywhatkit.sendwhatmsg(contact, message, hours, minutes)
def assistant(query):
    if query is None:
        return
    if 'goodbye' in query:
        speak("Goodbye! Have a great day.")
        exit()

    if 'hello' in query:
        speak("Hello! How can I help you today?")
    elif 'how are you' in query:
        speak("I'm doing well, thank you!")
    elif 'open youtube' in query:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com/")
    elif 'open whatsapp' in query:
        speak("Opening WhatsApp.")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'open spotify' in query:
        speak("Opening Spotify.")
        webbrowser.open("https://open.spotify.com/")
    elif 'tell me the date' in query:
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        speak(f'Today is {current_date}.')
    elif 'tell me the time' in query:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        speak(f'The time is {current_time}.')
    elif 'tell me the weather' in query:
        weather_info = get_weather()
        speak(weather_info)
    elif 'tell me the news' in query:
        news_info = get_news()
        speak('Here are the top headlines:\n' + news_info)
    elif 'search music' in query:
        query_music = query.replace('search music', '').strip()
        search_music(query_music)
    elif 'tell me about' in query:
        topic = query.replace('tell me about', '').strip()
        summary = get_wikipedia_summary(topic)
        print("Wikipedia Summary:")
        print(summary)
        speak(summary)
    elif 'send whatsapp message' in query:
        speak("Please provide the contact number.")
        contact = input("Enter the contact number: ")  # Allow user to enter the contact number
        speak("What message would you like to send?")
        message = listen()
        speak("At what time should I send this message? Please provide the hours.")
        hours = int(listen())
        speak("And the minutes?")
        minutes = int(listen())
        send_whatsapp_message(contact, message, hours, minutes)
        speak("WhatsApp message scheduled successfully.")
    
    elif 'send email' in query:
        speak("What is the subject of the email?")
        subject = listen()
        speak("What is the body of the email?")
        body = listen()
        send_email(subject, body)
        speak("Email sent successfully.")
    elif 'tell me a joke' in query:
        joke = get_joke()
        speak("Here's a joke for you:")
        speak(joke)
    else:
        speak("I'm sorry, I didn't understand that.")

if __name__ == "__main__":
    speak("Hello! I'm your AI assistant. How can I help you today?")

    while True:
        query = listen()

        if query:
            assistant(query)