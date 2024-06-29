import speech_recognition as sr
import webbrowser
from gtts import gTTS
import pygame
import io
import datetime
from tkinter import messagebox
import requests
import pytz
import os
import psutil
from pytube import Search
import random
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import time
import wikipedia
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import schedule
import pyttsx3
from googletrans import Translator
import qrcode
import cv2



# Global initialization
recognizer = sr.Recognizer()
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = True
microphone = sr.Microphone(device_index=1)  # Update the device index if necessary

pygame.mixer.init()

responses = {
    "hello" : "Hello sir ! Glad to see you how can i help you today",
    "who are you" : "I'm Bujji your personal voice assisstant",
    "how are you" : "I'm a Virtual assistant i dont have any feelings, but im doing well",
    "what can you do" : "I'm capable of performing simple tasks such as opening and closing applications,\n identify date, time, weather in various countries,\n i can generate random quotations facts jokes and motivational sentences \n i can calculate the distance between any two places, \n i can generate qr codes, \n I can capture the images  and i can provide some normal responses",
    "bye" : "Bye sir, I'm here to assisst you any time.",
    "who created you" : "Mr Vamsi krishna"
}

websites = {
    "facebook" : "https://www.facebook.com/",
    "youtube" : "https://www.youtube.com/",
    "hackerrank" : "https://www.hackerrank.com/",
    "lead" : "https://leetcode.com/",
    "codechef" : "https://www.codechef.com/",
    "chat" : "https://chatgpt.com/",
    "hanuman" : "https://www.hanooman.ai/",
    "aits" : "https://aitsrajampet.ac.in/",
    "github" : "https://github.com/pandu-069/OIBSIP",
    "leet" : "https://leetcode.com/",
    "instagram" : "https://www.instagram.com/accounts/edit/",
    "snapchat" : "https://www.bing.com/ck/a?!&&p=77f519e2b80fa21bJmltdHM9MTcxODc1NTIwMCZpZ3VpZD0yYjA1NGNhNi02M2E0LTZhNzEtMjY5Zi01ZTk3NjIwOTZiZWMmaW5zaWQ9NTIyMQ&ptn=3&ver=2&hsh=3&fclid=2b054ca6-63a4-6a71-269f-5e9762096bec&psq=snapchat+web&u=a1aHR0cHM6Ly93ZWIuc25hcGNoYXQuY29tLw&ntb=1"

}

pcapps = {
    "anydesk" : r"C:\Program Files (x86)\AnyDesk\AnyDesk.exe",
    "whatsapp" : r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2424.6.0_x64__cv1g1gvanyjgm\WhatsApp.exe",
    "linkedin" : r"C:\Program Files\WindowsApps\7EE7776C.LinkedInforWindows_3.0.30.0_x64__w1wdnht996qgy\LinkedIn.exe",
    "github" : r"C:\Users\vamsi\AppData\Local\GitHubDesktop\app-3.4.1\GitHubDesktop.exe",
    "phone" : r"C:\Program Files\WindowsApps\Microsoft.YourPhone_1.24051.101.0_x64__8wekyb3d8bbwe\PhoneExperienceHost.exe",
    "file" : r"C:\Windows\explorer.exe",
    "bluestacks" : r"C:\Program Files\BlueStacks_nxt\HD-Player.exe",
    "spider-man" : r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Marvel’s Spider-Man Miles Morales.lnk",
    "teams" : r"C:\Users\vamsi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Microsoft Teams classic (work or school).lnk",
    "notepad": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Notepad++.lnk",
    "note" : r"C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_11.2404.10.0_x64__8wekyb3d8bbwe\Notepad\Notepad.exe",
    "python" : r"C:\Users\vamsi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.11\IDLE (Python 3.11 64-bit).lnk",
    "chrome" : r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "microsoft" : r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk",
    "edge" : r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk",
    "ms" : r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk",
    "code" :  r"C:\Users\vamsi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk",
    "settings" : r"C:\Windows\ImmersiveControlPanel\SystemSettings.exe"
}

original_names = {
    "anydesk" : "Anydesk",
    "whatsapp" : "WhatsApp",
    "linkedin" : "LinkedIn",
    "github" : "GitHub Desktop",
    "file" : "File Explorer",
    "bluestacks" : "Bluestacks",
    "notepad" : "Notepad++",
    "note" : "Notepad",
    "teams" : "Microsoft Teams",
    "python" : "python IDLE",
    "chrome" : "Chrome Browser",
    "microsoft" : "Microsoft Edge",
    "code" : "Virtual Studio Code",
    "chat" : "CHAT-GPT",
    "hanuman" : "Hanuman Ai",
    "aits" : "Annamacharya university website",
    "spiderman" : "Marvel spider-man Miles morales",
    "lead" : "Leet-code",
    "leet" : "Leet-Code",
    "ms" : "Microsoft Edge",
    "edge" : "Microsoft Edge",
    "snapchat" : "Snap-chat",
    "settings" : "System settings"

}

def get_lat_long(place_name, api):
    # Initialize OpenCage Geocode API
    geocoder = OpenCageGeocode(api)
    
    # Get location
    results = geocoder.geocode(place_name)
    
    # Check if the location exists
    if results and len(results) > 0:
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']
        return (latitude, longitude)
    else:
        return None
    
def get_distance(coord1, coord2):
    api = "218b906eee124a53b8c0e9dff83cb123"
    return int(geodesic(get_lat_long(coord1,api), get_lat_long(coord2,api)).km)

timezones = {
    'USA': 'America/New_York',
    'UK': 'Europe/London',
    'India': 'Asia/Kolkata',
    'Japan': 'Asia/Tokyo',
    'Australia': 'Australia/Sydney',
    'Brazil': 'America/Sao_Paulo',
    'South Africa': 'Africa/Johannesburg',
    'Germany': 'Europe/Berlin',
    'China': 'Asia/Shanghai',
    'Russia': 'Europe/Moscow'
}
authors = ["Mark Twain", "Oscar Wilde", "Maya Angelou", "Ernest Hemingway", "Jane Austen", 
           "William Shakespeare", "J.K. Rowling", "George Orwell", "Albert Camus", "Ralph Waldo Emerson"]
def get_random_author_quote():
    author = random.choice(authors)
    url = f"https://api.quotable.io/random?author={author}"
    response = requests.get(url)
    quote = response.json()
    return f"{quote['content']}, said by {quote['author']}"

def get_word_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    definitions = response.json()[0]["meanings"][0]["definitions"]
    definition_text = [f"Definition : {definition['definition']}" for i, definition in enumerate(definitions)]
    return definition_text[0]

def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return str(e)
def get_motivational_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        quote = data[0]['q']
        author = data[0]['a']
        return f"{quote} said by {author}"
    else:
        return "Error fetching quote."
def capture_image(file_name):
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Capture a frame
    ret, frame = cap.read()

    if ret:
        # Display the captured frame
        cv2.imshow('Captured Image', frame)

        # Wait for a key press
        cv2.waitKey(0)

        # Save the captured image to a file with the given name
        cv2.imwrite(file_name, frame)

        print(f"Image saved as '{file_name}'.")

    else:
        print("Error: Could not capture image.")

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volume_level / 100, None)

def reminder(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def set_reminder(time_str, message):
    schedule.every().day.at(time_str).do(reminder, message=message)
    while True:
        schedule.run_pending()
        time.sleep(1)

def get_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=3)
        return  summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options}"
    except wikipedia.exceptions.PageError:
        return "Page not found."

def set_timer(seconds):
    print(f"Timer set for {seconds} seconds.")
    text_to_speech(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    print("Time's up!")
    text_to_speech("Time's up!")
def get_latest_news(api_key, country='in'):  # 'in' for India
    base_url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
    response = requests.get(base_url)
    articles = response.json()["articles"]
    news = []
    for article in articles[:5]:  # Get top 5 news articles
        news.append(f"Title: {article['title']}\nDescription: {article['description']}")
        
    return random.choice(news)
def get_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    return current_volume
def gen_random_pass():
    UpperCase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase_letters = UpperCase_letters.lower()
    digits = "0123456789"
    sym = "(){}//!@#$%^&*<>:;|"

    full = ""

    UpperCase, lowercase, nums, symbols = True, True, True, True
    if UpperCase:
        full = full + UpperCase_letters
    if lowercase:
        full = full + lowercase_letters
    if nums:
        full = full + digits
    if symbols:
        full = full + sym

    length = 16
    amount = 1

    for i in range(amount):
        pas = "".join(random.sample(full, length))
        print(pas)
def get_covid_stats(country):
    url = f"https://disease.sh/v3/covid-19/countries/{country}"
    response = requests.get(url)
    data = response.json()
    return (f"COVID-19 Stats for {country}:\n"
            f"Cases: {data['cases']}\n"
            f"Deaths: {data['deaths']}\n"
            f"Recovered: {data['recovered']}")
def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)

def get_random_joke():
    url = "https://official-joke-api.appspot.com/jokes/random"
    response = requests.get(url)
    joke = response.json()
    return f"{joke['setup']} haha {joke['punchline']}"

def get_random_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    fact = response.json()["text"]
    return fact

def play_youtube_video(video_name):
    search = Search(video_name)
    results = search.results
    if results:
        video_url = results[0].watch_url
        webbrowser.open(video_url)
        print(f"Opening {video_name} video song")
        text_to_speech(f"Opening {video_name} video song")
    else:
        print("No results found.")

def close_application(app_names):
    for proc in psutil.process_iter(['pid', 'name']):
        for app_name in app_names:
            if app_name.lower() in proc.info['name'].lower():
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                except psutil.NoSuchProcess:
                    pass
                except psutil.TimeoutExpired:
                    proc.kill()

def get_current_time(timezone):
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    current_date = now.strftime('%B %d, %Y')
    current_time = now.strftime('%I:%M %p')
    return current_date, current_time

def get_timezone_for_country(country):
    return timezones.get(country)

def audio_to_text():
    print("Listening...")
    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print(f"Error occurred; {e}")
            return None


def find_recipe(ingredient):
    api_url = f"http://www.recipepuppy.com/api/?i={ingredient}"
    response = requests.get(api_url)
    recipes = response.json().get('results', [])
    recipe_list = [f"{recipe['title']} - {recipe['href']}" for recipe in recipes]
    return "\n".join(recipe_list)


def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)

    pygame.mixer.music.load(audio_data, 'mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def RPS():
    print("Welcome to rock paper scissors game")
    flag = True
    print("1.Rock 2.Paper 3.Scissors 4.Exit the game")
    text_to_speech('The correct pronunciation is rock paper and scissors')
    computer_score = 0
    user_score = 0
    computer_inputs = ['rock', 'paper', 'scissors']
    while flag:

        print("Enter your choice: ")
        user_input = audio_to_text()
        print("user : ", user_input)
        computer_input = random.randrange(0, 3)
        if user_input == 'rock':
            if computer_inputs[computer_input].lower() == "rock":
                print("computer: Rock")
                text_to_speech('rock')
                print("Same choice so no scores")
                continue
            elif computer_inputs[computer_input].lower() == "paper":
                text_to_speech('paper')
                print("computer: paper ")
                computer_score += 1
                print("Now computer score is ", computer_score)
            elif computer_inputs[computer_input].lower() == "scissors":
                text_to_speech('scissors')
                print("Computer: Scissors")
                user_score += 1
                print("Now score of user is : ", user_score)

        elif user_input == 'paper':
            if computer_inputs[computer_input] == "rock":
                text_to_speech('rock')
                print("computer: Rock")
                user_score += 1
                print("Now user score is ", user_score)
            elif computer_inputs[computer_input] == "paper":
                text_to_speech('paper')
                print("computer: paper ")
                print("Same choice so no scores")
                continue
            elif computer_inputs[computer_input] == "scissors":
                text_to_speech('scissors')
                print("Computer: Scissors")
                computer_score += 1
                print("Now score of computer is : ", computer_score)

        elif user_input == 'scissors':
            if computer_inputs[computer_input] == "rock":
                text_to_speech('rock')
                print("computer: Rock")
                computer_score += 1
                print("Now computer score is ", computer_score)

            elif computer_inputs[computer_input] == "paper":
                text_to_speech('paper')
                print("computer: paper ")
                user_score += 1
                print("Now score of user is : ", user_score)

            elif computer_inputs[computer_input] == "scissors":
                text_to_speech('scissors')
                print("Computer: Scissors")
                print("Same choice so no scores")
                continue

        elif user_input == 'exit':
            print("The game is ending")
            text_to_speech('The Game is ending')
            flag = False
        else:
            text_to_speech('Invalid input' + str(user_input))

    print("Now Scoreboard is: ")
    print("Computer score: ", computer_score)
    text_to_speech("computer score is" + str(computer_score))
    print("User score: ", user_score)
    text_to_speech("and user score is" + str(user_score))
    if computer_score > user_score:
        print("Computer won the game")
        print("Better luck next time")
        text_to_speech("Computer won the game")
        text_to_speech('Better luck next time')
        print("Run the program to play again")
    elif user_score > computer_score:
        print("Congratulations! You Won the game")
        text_to_speech('Congratulations')
        text_to_speech('You won the game')
        print("To play again run the program")
    else:
        print("Both has same score")
        print("----------------------------------- Tie ------------------------------------------------")
        text_to_speech('The Game is tied')

def get_weather(city):
    API_key = "5731c0a66b712c17b67b85ef40bdf7d9"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        exit(0)

    weather = res.json()
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    return temperature, description, city
def opening(name):
    if name in websites and name in pcapps:
            text_to_speech("website or application")
            cmd = list(audio_to_text().split())[0]
            if "web" in cmd:
                webbrowser.open(websites[name])
                text_to_speech(f"Opening {name}")
            elif "pc" or "computer" in cmd:
                process = pcapps[name]
                try:
                    os.startfile(process)
                except Exception as e:
                    print(f"Error: {e}")
                text_to_speech(f"Opening {name} ")
    elif name in websites:
        webbrowser.open(websites[name])
        if name in original_names:
            text_to_speech(f"Opening {original_names[name]}")
        else:
            text_to_speech(f"Opening {name}")

        
    elif name in pcapps:
        process = pcapps[name]
        try:
            os.startfile(process)
        except Exception as e:
            print(f"Error: {e}")
        if name in original_names:
            text_to_speech(f"Opening {original_names[name]} ")
    elif name not in pcapps and name not in websites:
        url = "https://www.google.co.in/search?q="
        webbrowser.open(url + name)
        text_to_speech(f"Searching about {name} in browser")
    else:
        text_to_speech("Invalid Application or website")

def action(command):
    if "open" in command.lower():
        flag = True
        while flag:
            try:
                name = list(command.split())[1].lower()
                flag = False
            except IndexError:
                command = audio_to_text()
                continue
        opening(name)
    elif "close" in command.lower():
        text_to_speech("Tell the names of the apps to be closed")
        apps = audio_to_text().split()
        close_application(apps)
    elif "exit" in command.lower() or "bye" in command.lower():
        text_to_speech(responses['bye'])
        exit(0)
    elif "weather" in command:
        text_to_speech("Tell the name of the city")
        city = audio_to_text()
        temperature, description, city = get_weather(city.lower())
        print(f"{city}: \nTemperature: {int(temperature)}°C \nWeather: {description}")
        text_to_speech(f"It's {int(temperature)} degrees Celsius with {description} weather in {city}")
    elif 'time' in command.lower() and 'timer' not in command.lower():
        text_to_speech("In which country")
        name = list(audio_to_text().split())
        if name[1] in timezones:
            c_name = get_timezone_for_country(name[1])
            time = get_current_time(c_name)
            print(name[1] ,":", time[1])
            text_to_speech("Its "+time[1]+" in country of "+name[1])
        
    elif 'date' in command.lower():
        text_to_speech("In which country")
        name = list(audio_to_text().split())
        if name[1] in timezones:
            c_name = get_timezone_for_country(name[1])
            date = get_current_time(c_name)
            print(name[1] ,":", date[0])
            text_to_speech("Its "+date[0]+" in country of "+name[1])
    elif 'play a song' in command.lower() or 'play a video' in command.lower():
        text_to_speech("Tell the name of song to be played")
        name = audio_to_text()
        play_youtube_video(name)
    elif 'game' in command.lower():
        text_to_speech("Starting Rock paper scissors game")
        print("Rock paper scissors game")
        RPS()
    elif "distance" in command.lower():
        text_to_speech("Tell the name od starting point")
        p1 = audio_to_text()
        text_to_speech("Tell the name of ending point")
        p2 = audio_to_text()
        dis = get_distance(p1, p2)
        text_to_speech(f"The distance between {p1} and {p2} is {dis} kilo meters ")
        print(f"The distance between {p1} and {p2} is {dis} KM ")
    elif "quote" in command.lower() or "quotation" in command.lower():
        quote = get_random_author_quote()
        print(quote)
        text_to_speech(quote)
    elif "fact" in command.lower():
        fact  = get_random_fact()
        print(fact)
        text_to_speech(fact)
    elif "joke" in command.lower():
        joke = get_random_joke()
        print(joke)
        text_to_speech(joke)
    elif 'timer' in command.lower():
        text_to_speech("Enter number of seconds")
        sec = int(input("Enter no of seconds"))
        set_timer(sec)
    elif "news" in command.lower():
        api = "c6482a75ab074d0fa1f8a150d5ba405c"
        news = get_latest_news(api)
        print(news)
        text_to_speech(news)
    elif "covid" in command.lower():
        text_to_speech("Tell the name of country")
        name = audio_to_text()
        res = get_covid_stats(name)
        print(res)
        text_to_speech(res)
    elif "definition" in command.lower():
        text_to_speech(f"The definition of {command.split()[-1]} is ")
        mean = get_word_definition(command.split()[-1])
        print(mean)
        text_to_speech(mean)
    elif "summary" in command.lower():
        text_to_speech("Tell the topic name to provide summary")
        name = audio_to_text()
        res = get_wikipedia_summary(name)
        print(res)
        text_to_speech(res)
    elif "volume" in command.lower():
        cmd = command.split()[0]
        vol = get_volume()
        if cmd.lower() == "increase":
            set_volume(vol + 20)
        elif cmd.lower() == "decrease":
            set_volume(vol - 20)
    elif "reminder" in command.lower():
        text_to_speech("Enter the time to remind")
        time = input("Enter in this railway format ex: 21 : 30 ")
        text_to_speech("What is the message to remind")
        message = audio_to_text()
        set_reminder(time, message)
    elif "expression" in command.lower():
        text_to_speech("Enter the expression to evaluate")
        exp = input("Enter the expression to eval")
        res = calculate(exp)
        print(f"The result of expression {exp} is {res}")
        text_to_speech(f"The result of expression {exp} is {res}")
    elif "motivate" in command.lower():
        qot = get_motivational_quote()
        print(f"Hey, {qot}")
        text_to_speech(f"Hey, {qot}")
    elif "password" in command.lower():
        gen_random_pass()
    elif "qr" in command.lower():
        text_to_speech("Enter the url and filename to generate")
        url = input("paste the url here")
        filename = input("Enter the name of the file along with extension (ex : qr.png)")
        generate_qr_code(url, filename)
        print(f"The file is saved as {filename} ")
    elif "capture" in command.lower() or "photo" in command.lower():
        text_to_speech("Enter the name of the photo to be captured")
        name = input("Enter along with its extension: ")
        capture_image(name)
    elif "search" in command.lower():
        name = command.split()[1]
        url = "https://www.google.co.in/search?q="
        webbrowser.open(url + name)
        text_to_speech(f"Searching about {name} in browser")
        
    
    else:
        if command.lower() in responses :
            print(responses[command.lower()])
            text_to_speech(responses[command.lower()])
            



if __name__ == "__main__":
    text_to_speech("Tell the secret password to access the voice assistant")
    print("Speak out the password to access BUJJI")
    count = 3
    while True:
        user_input = audio_to_text().lower()
        if "jarvis" in user_input or "bujji" in user_input:
            text_to_speech("Access granted")
            print("<-------------Access granted----------->")
            text_to_speech("Hello sir, how can I help you?")

            while True:
                try:
                    command = audio_to_text().lower()
                    action(command)
                    time.sleep(3)
                except AttributeError:
                    continue

        else:
            print("<---------Access Denied---------->")
            text_to_speech("Access denied")
            count = count - 1
            text_to_speech(f"{count} more chance are balance")
            if count == 0:
                exit(0)
        
        



        