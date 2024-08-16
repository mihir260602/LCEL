import requests
import streamlit as st
from streamlit_lottie import st_lottie

def get_groq_response(input_text):
    json_body = {
        "input": {
            "language": "French",
            "text": f"{input_text}"
        },
        "config": {},
        "kwargs": {}
    }
    response = requests.post("http://127.0.0.1:8000/chain/invoke", json=json_body)
    
    try:
        response_json = response.json()
        st.write("API Response:", response_json)
        return response_json
    except ValueError:
        st.error("The response is not a valid JSON. Received the following text:")
        st.text(response.text)
        return None

# Load Lottie animation from URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Streamlit app configuration
st.set_page_config(
    page_title="Text to French Converter",
    page_icon="🌍",
    layout="centered"
)

# Lottie animation for better UI
lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_zd7IlgYpPY.json")
if lottie_animation:
    st_lottie(lottie_animation, height=200, key="animation")

# Title and description
st.title("🌍 LLM Application Using LCEL")
st.markdown("""
    #### Convert your text into French instantly with the power of Language Models.
    """)

# User input section with a neat layout
input_text = st.text_area("Enter the text you want to convert to French", height=150)

# Convert button with feedback
if st.button("Convert to French"):
    if input_text:
        with st.spinner("Converting..."):
            response = get_groq_response(input_text)
            if response:
                # Check if 'output' is a string
                if isinstance(response, dict) and 'output' in response and isinstance(response['output'], str):
                    st.success("Text successfully converted!")
                    st.markdown(f"**Translated Text:**\n\n{response['output']}")
                    
                    # Display crackers image as a celebratory effect
                    st.image("https://your-image-url-of-crackers-or-fireworks.gif", use_column_width=True)
                    
                    # Alert box using st.write with custom styling
                    st.markdown("""
                        <div style="padding: 10px; background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;">
                            <strong>Translation Complete!</strong><br>
                            Your text has been successfully translated to French. Enjoy the translation! 🎉
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Unexpected response format. Please check the API response.")
            else:
                st.error("Failed to get a valid response from the API.")
    else:
        st.warning("Please enter some text to convert!")

# Footer with custom styling
st.markdown("""
    <style>
    footer {
        visibility: hidden;
    }
    footer:after {
        content:'🌍 Created by Mihir Joshi'; 
        visibility: visible;
        display: block;
        position: relative;
        padding: 5px;
        top: 2px;
        color: gray;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
