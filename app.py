import streamlit as st
import requests
from PIL import Image
from io import BytesIO


# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HEADERS = {"Authorization": "Bearer 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"}  # Replace with your token

# Set page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🖼️",
    layout="wide",
)

# Function to generate images
def generate_images(prompt, num_images=1):
    images = []
    for _ in range(num_images):
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            images.append(Image.open(BytesIO(response.content)))
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return []
    return images

st.sidebar.write("""
    **Welcome to the AI Image Generator!**  
    Enter a prompt below and generate stunning AI-created images!
""")

st.sidebar.markdown("---")
st.sidebar.title("Developed by")
st.sidebar.write("""
Pavan Bendre R   
AI Image Generator  
[LinkedIn](https://www.linkedin.com/in/pavan-bendre-r)  
""")

st.title("🖼️ AI Image Generator")
st.write("Describe a scenario, and AI will generate images for you.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Input Scenario")
    prompt = st.text_input("Describe your scenario", "A butterfly in the sky")
    num_images = st.slider("Number of images:", 1, 5, 1)
    if st.button("Generate Image"):
        with st.spinner("Generating..."):
            images = generate_images(prompt, num_images)
            st.session_state["generated_images"] = images if images else []

with col2:
    st.subheader("Output Images")
    if "generated_images" in st.session_state and st.session_state["generated_images"]:
        for img in st.session_state["generated_images"]:
            st.image(img, caption=f"Generated for: '{prompt}'", use_column_width=True)
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            st.download_button("Download Image", img_bytes.getvalue(), file_name="generated_image.png", mime="image/png")
    else:
        st.info("Your generated images will appear here.")

st.markdown(
    """
    <style>
    footer {
        visibility: hidden;
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f0f0f0;
        padding: 10px;
        text-align: center;
        font-size: 12px;
    }
    </style>
    <div class="footer">
        Developed by Pavan Bendre R  
    </div>
    """,
    unsafe_allow_html=True
)
