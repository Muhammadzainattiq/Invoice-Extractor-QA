import streamlit as st
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai

genai.configure(api_key= st.secrets["GOOGLE_API_KEY"])


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
created_style = """
    color: #888888; /* Light gray color */
    font-size: 99px; /* Increased font size */
""" 
st.markdown("<p style='{}'>➡️created by 'Muhammad Zain Attiq'</p>".format(created_style), unsafe_allow_html=True)
title_style = """
    color: #8B13CC; /* Dark cyan color */
    font-size: 36px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 30px;
"""
st.markdown("<h1 style='{}'>Invoices info Extractor</h1>".format(title_style), unsafe_allow_html=True)
with st.expander("About the app"):
    st.info("This app can extract and present any information you required from an invoice. You will just upload the invoice picture and it will read it and you will be able to query any of its part.")
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
