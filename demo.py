import speech_recognition as sr
from gtts import gTTS
import os
from openai import OpenAI
from time import sleep
OPENAI_API_KEY = "sk-...."
import json

jd = """
Technician Job Summary
We are seeking a technician who will manage, direct, and install electrical wiring and installation for all building projects. In this position, you will work with contractors, builders, and architects, and will install and maintain electrical wiring systems, circuitry, and follow safety practices and standards codes to meet high-quality standards. You will review and compare pricing, document materials needed and used, and track changes to plans.

Technician Duties and Responsibilities
Monitor and analyze electrical systems
Collaborate with architects and engineers to determine the best placement of electrical wiring
Test devices for improvement, safety, and quality control
Update older electrical systems for changes, cost reductions, improvements, safety, and quality control
Repair broken equipment and wiring
Review architectural plans
Perform and analyze tests to track results and make improvements
Work with builders and make recommendations
Perform calibrations for wire placement and electronic components
Responsible for all required electrical qualification tests on projects and ensure compliance with all outside parties involved
Participate in test runs and meet safety regulations
Modify systems to be environmentally friendly
Technician Requirements and Qualifications
Able to multitask, prioritize, and manage time efficiently
Excellent verbal and written communication skills
Creative problem solver who thrives when presented with a challenge
Able to analyze problems and strategize for better solutions
Flexible and able to multitask on several different aspects of a project or on multiple projects
Able to take initiative to recommend projects, product improvements, or cost reductions
In-depth understanding of electrical regulations, construction, materials, and industry
Strict attention to detail
Technical school degree and certification for technicians; license as required by state
Four to five years of experience as a technician, technician apprentice, or relevant work experience
Proficient computer skills, Microsoft Office Suite (Word, PowerPoint, Outlook, and Excel)
Excellent communicator; able to understand instructions and communicate effectively
Knowledge of local, state, and federal property and safety regulations
Strong mathematical and technical skills
"""

client = OpenAI(api_key=OPENAI_API_KEY)

def show_json(obj):
    print(json.loads(obj.model_dump_json()))

def audio_player(text):
    exceptionErr = False
    ex = ''
    try:
        print("Playing recognized text back...")
        myobj = gTTS(text=text, lang='en', slow=False)
        print("Saving the converted audio in a mp3 file named")
        myobj.save("C:/tmp/chat.mp3")
        print("Playing the converted file")
        os.system("start C:/tmp/chat.mp3")
    except Exception as ex:
        print("Error during recognition:", ex)
def speach_toTXT():
    recognizer = sr.Recognizer()
    exceptionErr = False
    try:
        # List available microphones (optional)
        print("Available microphones:")
        print(sr.Microphone.list_microphone_names())
        # Select a specific microphone (optional)
        # with sr.Microphone(device_index=1) as source:
        with sr.Microphone() as source:
            print("Adjusting noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Recording for 10 seconds...")
            recorded_audio = recognizer.listen(source, timeout=10)
            print("Done recording.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        exceptionErr = True
        ex = "Google Speech Recognition could not understand the audio"
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        ex = "Could not request results from Google Speech Recognition service"
        exceptionErr = True
    try:
        print("Recognizing the text...")
        text = recognizer.recognize_google(recorded_audio, language="en-US")
        print("Decoded Text: {}".format(text))
    except Exception as ex:
        print("Error during recognition:", ex)
        ex = str(ex)
        exceptionErr = True
    if exceptionErr is True:
        return ex
    else:
        return text

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        sleep(0.5)
    return run

assistant_id = 'asst_...'

print("New thread for existing assistant_id")
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=jd,
)

show_json(message)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
)

run = wait_on_run(run, thread)

messages = client.beta.threads.messages.list(thread_id=thread.id)

print("Got response: %s" %(messages.data[0].content[0].text.value))
msg = messages.data[0].content[0].text.value
audio_player(msg)
sleep(10)

# Response from user
usr_response = speach_toTXT()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=usr_response,
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
)
run = wait_on_run(run, thread)

messages = client.beta.threads.messages.list(thread_id=thread.id)

print("Got response: %s" %(messages.data[0].content[0].text.value))
msg = messages.data[0].content[0].text.value
audio_player(msg)
