from dotenv import load_dotenv
load_dotenv()  
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Setting page config
st.set_page_config(page_title="Facetify: The AI Aesthetics Companion", page_icon="🌿")

# Setting header
st.title("👩‍⚕️ Your Personal AI Mirror")
st.subheader("Upload an image and get detailed self image insights")


input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("RATE ME (EVERYONE IS BEAUTIFUL IN THEIR OWN ASPECTS )")

# Prompt Template
input_prompt = """
Judge the person in the image on a scale of 1 to 10. Physiognomy, judge on looks and how they appear. Miss world Judge Superficial and provide constructive feedback for improvement.
Image: {image}

RATING:
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)