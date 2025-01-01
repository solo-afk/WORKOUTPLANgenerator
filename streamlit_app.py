import streamlit as st
import os
import google.generativeai as ggi


 # Page title
    
st.set_page_config(page_title='Workout Plan Generator', page_icon='💪🏾')
st.title("💪🏾Athletes' AI")

tab1, tab2, tab3 = st.tabs(["Workout Plan", "Premade plans", "Diets"])

# Initialize variables
gender = ""
height = ""
sport = ""
goal = ""
days = []
age = ""
place = ""
kind = ""
extras = []
pt = ""
ptmore = ""

# Load environment variables and configure the API key

api_key = st.secrets["api_keys"]["API_KEY"]
ggi.configure(api_key=api_key)

# Create and start the chatbot
model = ggi.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def LLM_Response(question):
    response = chat.send_message(question)
    return response.text

def generate_workout_plan():
    # Construct the message with user inputs
    if kind == "Physical Therapy":
        message = (
            f"Create a one day physical therapy session with the following information: "
            f"I am a {age} year old {gender}."
            f"I am {height} inches tall and weigh {weight} lbs."
            f"I need physical therapy for my {pt} I want to do it at my {place}."
            f"Some extra info about my injury is {ptmore}"
            f"Make the headers like the days bigger and bold."
            f"I have {extras} that i want to use in the workout"
            f"At home = no equipment unless otherwise stated"
           
        )
    else:
        message = (
            f"Create a {kind} workout routine with the following information: "
            f"I am a {age} year old {gender}."
            f"I am {height} inches tall and weigh {weight} lbs."
            f"I play {sport} and my goal is to {goal}."
            f"I can workout on {', '.join(days)} and I want to do it at my {place}."
            f"Make the headers like the days bigger and bold."
            f"I have {extras} that i want to use in the workout"
            f"At home = no equipment unless otherwise stated and include at least 5 workouts for each day."
    
        )
    response = LLM_Response(message)
    
    # Store the generated plan in session state
    st.session_state['workout_plan'] = response

    return response

def chatbot():
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_quest = st.text_input("Say something:")
    btn = st.button("Enter")

    if btn and user_quest:
        result = LLM_Response(user_quest)
        st.session_state['chat_history'].append(('You', user_quest))
        st.session_state['chat_history'].append(("Gemini", result))

    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

    user_quest = st.text_input

# Sidebar for accepting input parameters
with st.sidebar:
    st.header('What kind of workout?')
    with st.expander('What kind of workout?'):
        kind = st.radio("One Week or One Day?", ('One Week','One Day',"Physical Therapy"))

    st.header('About You')
    with st.expander('Gender and Age'):
        gender = st.radio("Gender", ("male", "female"))
        age = st.slider("Age", 1, 100, 15, 1)

    with st.expander('Height and Weight'):
        height = st.slider('Height (in.)', 1, 96, 70, 1)
        heightin = height % 12
        heightft = (height - heightin) / 12
        st.header(f"{int(heightft)}'{heightin}\"")
        st.header('---------------------------------------')
        weight = st.slider('Weight (lbs.)', 10, 300, 180, 1)

    with st.expander('What sport do you play?'):
        sport = st.radio("Select your sport", ('Soccer⚽', 'Basketball🏀', 'Football🏈', 'Baseball⚾','No Sport'))

    with st.expander('What is your workout goal?'):
        goal = st.radio("Select your goal", ('Gain muscle mass', 'Lose weight', "Improve endurance"))

    st.header('Location')
    with st.expander('Where do you want to workout?'):
        place = st.radio("Where?", ('Gym', 'Home'))

    if kind == 'One Week':
        st.header('Time')
        with st.expander("What days can you work out?"):
            days = st.multiselect("Select days", ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
    
    
    elif kind == "Physical Therapy":
        st.header("PT Specifics")
        with st.expander("What body part hurts"):
            pt = st.radio("Select Body Part", ['Ankle','Shoulder','Knees','Wrists','Back','Neck','Other'])
            ptmore = st.text_input("Anything else I should know?")
    

    st.header('Extras')
    if place == "Home":
        with st.expander('Do you have any equipment at home?'):
            extras = st.text_input("Enter equipment here")


with tab1:

# App description
    with st.expander('About this app'):
        st.markdown('**What can this app do?**')
        st.info('This app allows users to create a workout routine specifically to help achieve their goals.')

# How to use the app
    with st.expander('How to use it'):
        st.markdown('**How do I use this?**')
        st.info("This app is very simple. All you have to do is click each drop-down menu to the left and answer the questions. Once you've finished, press the generate my plan button below.")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_button = st.button('Generate my plan')

# Check if the generate button was pressed
    if generate_button:
        workout_plan = generate_workout_plan()

# Always display the workout plan if it exists in session state
    if 'workout_plan' in st.session_state:
        st.subheader("Your workout plan:")
        st.markdown(st.session_state['workout_plan'])
        st.download_button("Copy Workout to Clipboard", st.session_state['workout_plan'], file_name="workout_plan.txt", key="download_button_2")

    chatbot()

with tab2:
    with st.expander("Messi's ab workout"):
        "- 30 knee touches"
        "- 30 heel touches"
        "- 30 leg kicks"
        "- 20 leg raises"
        "- 30 toe touches"
        "- 90 second plank"
        "Repeat twice with 1-2 minutes rest"
