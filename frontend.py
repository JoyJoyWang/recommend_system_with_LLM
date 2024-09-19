import streamlit as st
import torch
from PIL import Image, ImageOps
from transformers import pipeline

# Load Hugging Face text generation model
text_generator = pipeline("text-generation", model="distilgpt2")

# Sample data (replace with real Yelp data)
stores_data = [
    {
        "name": "Joe's Pizza",
        "category": "Restaurant",
        "rating": 4.5,
        "open_time": "10 AM - 11 PM",
        "sentiment_score": 0.85,
        "image_url": None,
        "description": "Best pizza in town!"
    },
    {
        "name": "Central Coffee",
        "category": "Cafe",
        "rating": 4.2,
        "open_time": "6 AM - 9 PM",
        "sentiment_score": 0.9,
        "image_url": None,
        "description": "Cozy coffee shop with great lattes."
    },
    {
        "name": "The Night Owl Bar",
        "category": "Bar",
        "rating": 4.8,
        "open_time": "5 PM - 2 AM",
        "sentiment_score": 0.82,
        "image_url": None,
        "description": "A lively bar with great cocktails."
    }
]

# Function to simulate recommendation engine based on store type
def get_recommendations(store_type):
    return [store for store in stores_data if store["category"] == store_type]

# Function to generate a personalized description using Hugging Face model
def generate_description(store_name, user_preferences):
    prompt = f"Based on {user_preferences}, describe the experience of visiting {store_name}. What potential pitfalls should the user be aware of?"
    response = text_generator(prompt, max_length=100, num_return_sequences=1)
    return response[0]["generated_text"]

# Function to create a placeholder image
def placeholder_image():
    img = Image.new('RGB', (200, 200), color=(192, 192, 192))
    img = ImageOps.grayscale(img)
    return img

# User login section
st.sidebar.title("User Login")
if 'username' not in st.session_state:
    username = st.sidebar.text_input("Enter your username")
    if username:
        st.session_state['username'] = username
        st.sidebar.success(f"Welcome, {username}!")
else:
    st.sidebar.success(f"Logged in as {st.session_state['username']}")

# User preferences input
user_preferences = st.sidebar.text_input("Enter your preferences (e.g., cozy, lively, quiet)")

# Main app title
st.title("Personalized Yelp Store Recommendations")

# Sidebar for selecting store types
store_types = ["Restaurant", "Cafe", "Bar"]
selected_store_type = st.sidebar.selectbox("Choose a store type", store_types)

# Get recommendations based on the selected store type
recommended_stores = get_recommendations(selected_store_type)

# Display recommended stores
st.subheader(f"Recommended {selected_store_type}s")

for store in recommended_stores:
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if store["image_url"]:
            image = Image.open(store["image_url"])
        else:
            image = placeholder_image()
        st.image(image, width=150)

    with col2:
        st.write(f"**Name:** {store['name']}")
        st.write(f"**Rating:** {store['rating']} stars")
        st.write(f"**Open Time:** {store['open_time']}")
        st.write(f"**Sentiment Score:** {store['sentiment_score']:.2f}")
        
        # Generate description button
        if st.button(f"Generate description for {store['name']}"):
            if user_preferences:
                description = generate_description(store['name'], user_preferences)
                st.write(description)
            else:
                st.warning("Please enter your preferences to generate a personalized description.")

# Sidebar icon for profile image (optional)
if st.sidebar.button("View Profile"):
    st.sidebar.image(placeholder_image(), caption="User Icon", use_column_width=True)

st.sidebar.write("Choose a store type to see recommendations and generate personalized descriptions.")
