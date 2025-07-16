# app.py

import streamlit as st
from PIL import Image
import warnings

# Import both of our backend functions
from story_generator import generate_story_from_images, narrate_story

# Ignore deprecation warnings for a cleaner interface
warnings.filterwarnings(action='ignore',category=DeprecationWarning)

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Story Generator",
    page_icon="📖",
    layout="wide"
)

# --- UI Elements ---
st.title("📖 AI Story Generator from Images")
st.markdown("Upload 1 to 10 images, choose a style, and let the AI write and narrate a tale for you!")

# --- Sidebar for Controls ---
with st.sidebar:
    st.header("Controls")
    uploaded_files = st.file_uploader(
        "Upload your images...",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )
    story_style = st.selectbox(
        "Choose a story style:",
        ("Comedy", "Thriller", "Fairy Tale", "Sci-Fi", "Mystery", "Adventure", "Morale")
    )
    generate_button = st.button("Generate Story & Narration", type="primary")

# --- Main Logic ---
if generate_button:
    if not uploaded_files:
        st.warning("Please upload at least one image.")
    elif len(uploaded_files) > 10:
        st.warning("Please upload a maximum of 10 images.")
    else:
        with st.spinner("The AI is writing and narrating your story... This may take a moment."):
            try:
                pil_images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]

                st.subheader("Your Visual Inspiration:")
                image_columns = st.columns(len(pil_images))
                for i, image in enumerate(pil_images):
                    with image_columns[i]:
                        st.image(image, caption=f'Image {i + 1}', use_container_width=True)

                # --- Story Generation ---
                generated_story = generate_story_from_images(pil_images, story_style)

                # Check if the story was generated successfully before proceeding
                if "Error" in generated_story or "failed" in generated_story or "API Key" in generated_story:
                    st.error(generated_story)
                else:
                    # --- Display Story ---
                    st.subheader(f"Your {story_style} Story:")
                    st.success(generated_story)

                    # --- NARRATION LOGIC ---
                    st.subheader("Listen to the Story:")
                    audio_file = narrate_story(generated_story)
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
                    else:
                        st.error("Sorry, the audio narration could not be generated.")

            except Exception as e:
                st.error(f"An application error occurred: {e}")
else:
    st.info("Upload some images and click the button to begin.")