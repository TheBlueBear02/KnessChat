import streamlit as st
import datetime
import json

def display_user_message(tweet,all_tweets):
    # Define styles for user1
    id = tweet["UserId"]
    profile = next((p for p in all_tweets["Members"] if p["Id"] == id), None)
    hasRole = ""
    if profile["additional_role"] != "":
        hasRole = "|"

    if profile["is_coalition"] == True: # Define styles for coalition or other users
        alignment = "flex-end"
        background_color = "#DEEFFF"
        text_color = "black"
        border_radius = "15px"
        halign = "right"
        talign = "left"
        table = "ltr"
    else:  # Define styles for oposition or other users
        alignment = "flex-start"
        background_color = "#FFF8F8"
        text_color = "black"
        border_radius = "15px"
        halign = "left"
        talign = "right"
        table = "rtl"


    # Custom styling for the message bubble
    bubble = f"""
    <div style="display: flex; flex-direction: column; align-items: {alignment}; margin-top: 4px;">
        <div style="max-width: 80%; margin: 5px; padding: 10px; background-color: {background_color}; border-radius: {border_radius}; color: {text_color}; text-align: right">
            <table style="direction: {table};">
                <tr style="border: none;"> 
                    <th style="border: none; text-align: {halign};">
                        <h5 style="margin:0; margin-left: 40px; padding: 0;">{profile["name"]}</h5>
                        <i style="margin-left: 0px;">{profile["additional_role"]} {hasRole} {profile["party"]}</i>
                    </th>
                    <th style="border: none;float: right;margin:0; padding: 0;">
                        <img style=" padding:0; margin:0; width:40px; height:40px; border-radius: 50%;" src="{profile["image"]}">
                    </th>
                </tr>
                <tr style="border: none;">
                    <td style="border: none;">
                    <p dir= "rtl" style="margin-top: 10px; color: {text_color}; margin:0px; padding:0px;">{tweet["Text"]}</p>
                    <p style="color: {text_color}; text-align: {talign}; font-size: small; margin:0px; padding:0px;">{tweet["Time"]}</p></td>
                    <td style="border: none;"></td>
    </div>
    """
    st.markdown(bubble, unsafe_allow_html=True)

# Reads the tweets json file
with open('Tweets.json', 'r',  encoding='utf-8') as file:
    all_tweets = json.load(file)


st.image("https://github.com/TheBlueBear02/KnessChat/blob/master/Images/banner1.png?raw=true")
# Display the chat interface
#st.markdown("### KnessChat")
#st.markdown("---")

# Display the messages
for tweet in all_tweets["Tweets"]:
    display_user_message(tweet,all_tweets)
