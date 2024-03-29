import streamlit as st
import json
from datetime import date
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title='KnessChat', page_icon='https://github.com/TheBlueBear02/KnessChat/blob/master/Images/Knesset.png?raw=true', initial_sidebar_state='auto'
) # site config

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

BACKGROUND_COLOR = 'white'
COLOR = 'black'

# remove the top margin
st.markdown(" <style> div[class^='block-container'] { padding-top: 0rem; } </style> ", unsafe_allow_html=True)
st.markdown(" <style> div[class^='st-emotion-cache-16txtl3 eczjsme4'] { padding-top: 3rem; } </style> ", unsafe_allow_html=True)

def display_user_message(tweet,all_tweets): # print the latest tweets
    id = tweet["UserId"]
    profile = next((p for p in all_tweets["Members"] if p["Id"] == id), None) # search for the specific user
    hasRole = ""
    if profile["additional_role"] != "": # checks if the user has additional role
        hasRole = "|"

    text_color = "black"
    border_radius = "25px"

    if profile["is_coalition"] == True: # Define styles for coalition or other users
        alignment = "flex-end"
        background_color = "#DEEFFF"
        halign = "right"
        talign = "left"
        table = "ltr"
    else:  # Define styles for oposition or other users
        alignment = "flex-start"
        background_color = "#FFF5EC"      
        halign = "left"
        talign = "right"
        table = "rtl"

    
    # Custom styling for the message bubble
    bubble = f"""

    <div style=" display: flex; flex-direction: column; align-items: {alignment}; margin-top: 4px;">
        <div style="box-shadow: 0 2px 5px rgb(0 0 0 / 0.2); max-width: 70%; margin: 10px; padding: 10px; background-color: {background_color}; border-radius: {border_radius}; color: {text_color}; text-align: right">
            <table style="direction: {table};">
                <tr style="padding:0px; margin:0px; border: none;"> 
                    <th style="margin: 0;border: none; text-align: {halign};">
                        <h6 style="margin:0; margin-left: 50px; padding: 0;">{profile["name"]}</h6>
                        <i style="margin: 0px;padding:0px;">{profile["additional_role"]} {hasRole} {profile["party"]}</i>
                    </th>
                    <th style="border: none;float: right;margin:0; padding: 0;">
                        <img style=" padding:0; margin:0; width:40px; height:40px; border-radius: 50%;" src="{profile["image"]}">
                    </th>
                </tr>
                <tr style="padding:0px; margin:0px; border: none;">
                    <td style="margin: 0;padding:0; padding-right: 10px;border: none;">
                    <p dir= "rtl" style="font-size:17px;color: {text_color}; margin-down:5px; padding:0px;">{tweet["Text"]}</p>
                    </td>
                    <td style="margin: 0;padding:0;border: none;"></td>
                </tr>
                <tr style="margin: 0;padding:0;border: none;">
                    <th style="margin: 0;padding:0;border: none;">                     
                      <object style="border-radius:{border_radius}; width:100%;" data="https://github.com/TheBlueBear02/KnessChat/blob/master/tweetsImages/{tweet["Id"]}.jpg?raw=true" type="image/jpeg">
                      </object>
                      <p style="color: {text_color}; text-align: {talign}; font-size: 14px;margin:0; margin-{talign}:10px; padding:0px;">{tweet["Time"]}</p>
                    </th>
                </tr>
        </div>
    </div>
    """

    st.markdown(bubble, unsafe_allow_html=True) # print the tweet bubble


# Reads the tweets json file
with open('Tweets.json', 'r',  encoding='utf-8') as file:
    all_tweets = json.load(file)


st.markdown( # fixed width to sidebar
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 255px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar: # side bar
    st.markdown("[![Foo](https://github.com/TheBlueBear02/KnessChat/blob/master/Images/sideBanner.png?raw=true)](https://twitter.com/KnessChat)") # sidebar banner


st.image("https://raw.githubusercontent.com/TheBlueBear02/KnessChat/master/Images/banner2.png") #Banner


#feed = st.container(border=0,height=600)
today = date.today()



for tweet in reversed(all_tweets["Tweets"]):         # Display the messages
    #if tweet["Date"] == str(today):
    display_user_message(tweet,all_tweets)

#st.container(height=20,border=0)
#st.link_button(label="לתרומה",help="האתר לא מעודכן כרגע. על מנת שהאתר יעבוד 24/7 אני צריך לשלם 100$ בחודש לטוויטר. מוזמנים לעזור",url="https://www.paypal.com/donate/?hosted_button_id=2ANRW8V38KYZS",use_container_width=True)
