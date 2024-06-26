import streamlit as st
from streamlit_float import float_css_helper
from streamlit_float import float_init
import json
from datetime import datetime, timedelta, date
from streamlit_javascript import st_javascript
from user_agents import parse 
from enum import Enum
import time

st.set_page_config(page_title='KnessChat', page_icon='https://github.com/TheBlueBear02/KnessChat/blob/master/Images/Knesset.png?raw=true', initial_sidebar_state='collapsed') # site config


float_init() # from float library


class Topics(Enum): # topics enum
    topic1 = "חטופים"
    topic2 = "חוק הגיוס"
    topic3 = "מלחמה"
    all_topics = "all"

# remove the top margin
st.markdown(" <style> div[class^='block-container'] { padding-top: 0rem; } </style> ", unsafe_allow_html=True)
st.markdown(" <style> div[class^='st-emotion-cache-16txtl3 eczjsme4'] { padding-top: 3rem; } </style> ", unsafe_allow_html=True)



def reload(): # reload the code
    st.rerun()

def scroll_to_top(unique_id): # scroll the page to the top using javascript
    js = f'''
    <script>
        {unique_id}
        var body = window.parent.document.querySelector(".main");
        body.scrollTop = 0;
    </script>

    '''
    st.components.v1.html(js)

def topics_menu(chosen_topic): # print the topics buttons menu and return the selected topic
    col1, col2, col3, col4 = st.columns([1.5,1.5,1.5,1])  # filter buttons table
    with col1:
        topic3 = st.button(label="🪖 מלחמה" ,key=1,use_container_width=True)
    with col2:
        topic2 = st.button(label="👮 חוק הגיוס‍️",key=2,use_container_width=True)
    with col3:
        topic1 = st.button(label="🎗 חטופים",key=3,use_container_width=True)
    with col4:
        reloadB = st.button(label="כל הציוצים",key=4,use_container_width=True,type="primary") # re
        
    if reloadB:
        chosen_topic = Topics.all_topics.value
        scroll_to_top(unique_id)
    elif topic1:
        chosen_topic = Topics.topic1.value
        scroll_to_top(unique_id)
    elif topic2:
        chosen_topic = Topics.topic2.value
        scroll_to_top(unique_id)
    elif topic3:
        chosen_topic = Topics.topic3.value
        scroll_to_top(unique_id)
    return  chosen_topic

def show_feed(tweet,all_tweets,knesset_members,on_pc,chosen_topic): # print the latest tweets
    if tweet["Topic"] == chosen_topic or chosen_topic == Topics.all_topics.value:
        id = tweet["UserId"]
        profile = next((p for p in knesset_members["Members"] if p["Id"] == id), None) # search for the specific user
        hasRole = ""
        text = tweet["Text"]
        if profile["additional_role"] != "": # checks if the user has additional role
            hasRole = "|"

        
        day = datetime.strptime(tweet["Date"], '%Y-%m-%d').date() # gets the tweet date
        yesterday = datetime.today() - timedelta(days=1) # yesterday's date

        if day == date.today():
            day = "היום"
        elif day == yesterday.date():
            day = "אתמול"
        else:
            day = datetime.strftime(day, '%d/%m/%y')
        topic = tweet['Topic']

        # pc deisgn
        bubble_width = "70%"    
        container_width = "80%"
        margin_left = "10%"
        text_color = "black"
        border_radius = "25px 5px 25px 25px"
        padding = "0px"
        
        if not on_pc: # checks if on pc or not
            # phone design
            bubble_width = "100%"
            container_width = "100%"
            margin_left = "0%"
            padding = "15px"
            margin_left = "0%"

        
        if profile["is_coalition"] == True: # Define styles for coalition or other users
            alignment = "flex-end"
            background_color = "#DEEFFF"
            halign = "right"
            talign = "left"
            table = "ltr"
        else:  # Define styles for oposition or other users
            alignment = "flex-start"
            background_color = "#FFEEDF"      
            halign = "left"
            talign = "right"
            table = "rtl"
            border_radius = "5px 25px 25px 25px"
        
        bubble = f"""
        <div style="padding-{talign}:{padding}; margin-left: {margin_left}; width: {container_width};display: flex; flex-direction: column; align-items: {alignment}; margin-top: 4px;">
            <div style="box-shadow: 0 2px 5px rgb(0 0 0 / 0.2); max-width: {bubble_width}; margin: 10px; padding: 10px; background-color: {background_color}; border-radius: {border_radius}; color: {text_color}; text-align: right">
                <table style="direction: {table};">
                    <tr style="direction: {table}; padding:0px; margin:0px; border: none;"> 
                        <th style="margin: 0;border: none; text-align: {halign};">
                            <table style="border: none; width:100%;">
                                <tr style="border: none; margin:0; padding: 0;">
                                    <th style="border: none;margin:0; padding: 0;">
                                        <div style=" text-align: center; box-shadow: 0 2px 5px rgb(0 0 0 / 0.2); border-radius: {border_radius}; display:flex; margin:0px; background-color:#C3FBC2; width:80px;">
                                            <p style="font-weight: 700; margin: auto; padding:0px;">{topic}</p>
                                        </div>                              
                                    </th>
                                    <th style="border: none; margin:0; padding: 0;">
                                        <h5 style="margin:0; margin-left: 50px; padding: 0;">{profile["name"]}</h5>
                                    </th>
                                </tr>
                            </table>
                            <i style=" margin: 0px;padding:0px;">{profile["additional_role"]} {hasRole} {profile["party"]}
                        </th>
                        <th style="border: none;float: right;margin:0; padding: 0;">
                            <img style="box-shadow: 0 3px 6px rgb(0 0 0 / 0.3); padding:0; margin:0; width:40px; height:40px; border-radius: 50%;" src="{profile["image"]}">
                        </th>
                    </tr>
                    <tr style="padding:0px; margin:0px; border: none;">
                        <td style="margin: 0;padding:0; padding-right: 10px;border: none;">
                        <p dir= "rtl" style="line-height:120%;font-size:17px;color: {text_color}; margin-down:5px; padding:0px;">{text}</p>
                        </td>
                        <td style="margin: 0;padding:0;border: none;"></td>
                    </tr>
                    <tr style="margin: 0;padding:0;border: none;">
                        <th style="margin: 0;padding:0;border: none;">                     
                        <img style="margin-bottom:5px;border-radius:25px; width:100%;" src="https://github.com/TheBlueBear02/KnessChat/blob/master/tweetsImages/{tweet["Id"]}.jpg?raw=true" alt=""/>
                        <p style="color: {text_color}; text-align: {talign}; font-size: 14px;margin:0; margin-{talign}:10px; padding:0px;">{tweet["Time"]} | {day}</p>
                        </th>
                    </tr>
            </div>
        </div>
        """
        st.markdown(bubble, unsafe_allow_html=True) # print the tweet bubble


st.markdown( # fixed width to sidebar
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 300px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar: # side bar
    st.markdown("[![Foo](https://github.com/TheBlueBear02/KnessChat/blob/master/Images/SideBanner1.png?raw=true)](https://twitter.com/KnessChat)") # sidebar banner
    #st.link_button(label="לתרומה",help="24/7 אני צריך לשלם 100$ בחודש לטוויטר. מוזמנים לעזור",url="https://www.paypal.com/donate/?hosted_button_id=2ANRW8V38KYZS",use_container_width=True)


# checks if the user is from phone or pc
ua_string = st_javascript("""window.navigator.userAgent;""") 
user_agent = parse(str(ua_string))
st.session_state.is_session_pc = user_agent.is_pc
on_pc = st.session_state.is_session_pc  

info = st.container()
with info:
    st.markdown("**לעוד מידע**")
info_css = float_css_helper(left="2.5rem",top= "3rem",background="#0082FB",css="color:white;width:100px;padding:15px; margin:0px; border-radius:0px 50px 50px 50px") 
info.float(info_css) # set the popup footer

# Reads the tweets and knesset members json files
with open('Tweets.json', 'r',  encoding='utf-8') as file:
    all_tweets = json.load(file)
with open('KnessetMembers.json', 'r',  encoding='utf-8') as file:
    knesset_members = json.load(file)


chosen_topic = Topics.all_topics.value # set the defualt topic to all topics
unique_id = int(time.time()) # Get the current time to create unique id for the scroll up function
header = st.container() # the header container
footer = st.container() # the header container

banner_src = "https://raw.githubusercontent.com/TheBlueBear02/KnessChat/master/Images/banner3.png"

if on_pc: # pc header
    with header:
        banner = st.image(banner_src) #Banner
        chosen_topic = topics_menu(chosen_topic)
       
    top = st.container(height=80,border=0)          
    header_css = float_css_helper(top= "0rem",background="white",css="padding-top:50px;padding-bottom:10px;border-radius:15px")

else: # Phone header and footer
    with footer:
        with st.expander(label="סנן על פי נושא"):
            chosen_topic = topics_menu(chosen_topic) # topics filter buttons table

    footer_css = float_css_helper(bottom= "0.5rem",background="white",css="padding:0px; margin:0px; border-radius:0px") 
    footer.float(footer_css) # set the popup footer
    with header:
        banner = st.image(banner_src) #Banner
    
    header_css = float_css_helper(top= "2.86rem",background="white",css="padding:0px; margin:0px; border-radius:0px") 


# feed
for tweet in reversed(all_tweets):   # Display the tweets
    show_feed(tweet,all_tweets,knesset_members,on_pc,chosen_topic)

header.float(header_css) # set the popup header

