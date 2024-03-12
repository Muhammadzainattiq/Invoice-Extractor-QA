from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(instructions, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([instructions, image[0], prompt])
    return response.text

def set_image_data(uploaded_image):
    if uploaded_image is not None:
        bytes = uploaded_image.getvalue()

        image_data = [
            {
            "mime_type": uploaded_image.type,
            "data": bytes
        }
        ]
        return image_data
    else:
        raise FileNotFoundError("No file uploaded.")
    


st.set_page_config(page_title= 'Invoice Extractor')
prompt = st.text_input("Input Prompt: ", key = "input")
uploaded_image = st.file_uploader("Choose an image...", type= ['jpg', "png", 'jpeg'])
    
image = ""

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption= 'Uploaded image: ', use_column_width = True)

submit = st.button("Ask")

instructions = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

if submit:
    image_data = set_image_data(uploaded_image)
    response = get_response(instructions, image_data, prompt)
    st.subheader("Response")
    st.write(response)
