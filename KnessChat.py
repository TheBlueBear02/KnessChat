import streamlit as st
import json

st.set_page_config(page_title='KnessChat', page_icon='https://github.com/TheBlueBear02/KnessChat/blob/master/Images/Knesset.png?raw=true', initial_sidebar_state='collapsed'
) # site config
                
def display_user_message(tweet,all_tweets): # print the latest tweets
    id = tweet["UserId"]
    profile = next((p for p in all_tweets["Members"] if p["Id"] == id), None) # search for the specific user
    hasRole = ""
    if profile["additional_role"] != "": # checks if the user has additional role
        hasRole = "|"

    text_color = "black"
    border_radius = "15px"
    
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
    <div style="display: flex; flex-direction: column; align-items: {alignment}; margin-top: 4px;">
        <div style="max-width: 80%; margin: 5px; padding: 10px; background-color: {background_color}; border-radius: {border_radius}; color: {text_color}; text-align: right">
            <table style="direction: {table};">
                <tr style="padding:0px; margin:0px; border: none;"> 
                    <th style="border: none; text-align: {halign};">
                        <h5 style="margin:0; margin-left: 40px; padding: 0;">{profile["name"]}</h5>
                        <i style="margin-left: 0px;">{profile["additional_role"]} {hasRole} {profile["party"]}</i>
                    </th>
                    <th style="border: none;float: right;margin:0; padding: 0;">
                        <img style=" padding:0; margin:0; width:40px; height:40px; border-radius: 50%;" src="{profile["image"]}">
                    </th>
                </tr>
                <tr style="padding:0px; margin:0px; border: none;">
                    <td style="border: none;">
                    <p dir= "rtl" style="color: {text_color}; margin:0px; padding:0px;">{tweet["Text"]}</p>
                    <p style="color: {text_color}; text-align: {talign}; font-size: small; margin:0px; padding:0px;">{tweet["Time"]}</p></td>
                    <td style="border: none;"></td>
    </div>
    """
    st.markdown(bubble, unsafe_allow_html=True) # print the tweet bubble
# Reads the tweets json file
with open('Tweets.json', 'r',  encoding='utf-8') as file:
    all_tweets = json.load(file)

welcomeT = f"""
    <div dir= "rtl" style="display: flex; flex-direction: column; align-items: right; margin-top: 4px;">
    <h4>על מה חברי הכנסת מדברים?</h4>
    <h4>קשה לעקוב אחרי כל מה שקורה?</h4>
    <h4>כל ההודעות במקום אחד!</h4>
    <h4>ברוכים הבאים ל</h4>
    <img style=" padding:0; margin:0; width:210px; height:60px; border-radius: 0%;" src="https://raw.githubusercontent.com/TheBlueBear02/KnessChat/master/Images/banner1.png">
    <h4>הכנסצ'אט הוא צ'אט של חברי הכנסת בו תוכלו לקרוא את כל ההודעות שלהם במקום אחד</h4>

"""
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

with st.sidebar:
    st.markdown("[![Foo](http://www.google.com.au/images/nav_logo7.png)](http://google.com.au/)")



st.image("https://raw.githubusercontent.com/TheBlueBear02/KnessChat/master/Images/banner1.png") #Banner

feed = st.container(border=0,height=500)

with feed: # Tweets containter
        for tweet in reversed(all_tweets["Tweets"]):         # Display the messages
            display_user_message(tweet,all_tweets)



