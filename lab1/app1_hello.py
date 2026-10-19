import streamlit as st
# Page configuration - must be the FIRST Streamlit command
st. set_page_config (
page_title =" Hello App",
page_icon ="H",
layout ="wide"
)
# Text elements
st. title (" Hello Streamlit ")
st. header ("My First App ")
st. subheader (" Learning Basics ")
st. write (" Streamlit converts Python scripts into web apps .")
st. markdown ("** Bold ** , * Italic * , and ‘code ‘ work here .")
# Messages
st. success ("App loaded successfully !")
st. info (" This is an info message .")
st. warning (" This is a warning .")
st. error (" This is an error .")
# Simple inputs
name = st. text_input (" Enter your name ")
age = st. number_input (" Enter your age ", min_value =1 , max_value =100)
# Display data as table
st. write (" ### Sample Data ")
st. table ({" Name ": ["A", "B"] , " Marks ": [85 , 90]})
st. code ("""
def greet ( name ):
return f"Hello , { name }!"
""", language =" python ")
st. divider ()