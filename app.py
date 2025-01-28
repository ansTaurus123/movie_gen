import streamlit as st
from groq import Groq

# Initialize the Groq client with your API key
client = Groq(api_key="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")

# Define the system message for the model
system_message = {
    "role": "system",
    "content": "You are an experienced scriptwriter who generates engaging and creative movie content based on a given theme. Provide main characters, a storyline, and a movie script."
}

def generate_movie_content(theme):
    # Generate main characters and storyline using Groq
    setup_prompt = f"Generate main characters and a storyline for a movie with the theme: '{theme}'."
    response = client.chat(messages=[
        system_message,
        {"role": "user", "content": setup_prompt}
    ])
    setup = response["choices"][0]["message"]["content"]

    # Extract characters and storyline
    if "Main Characters:" in setup and "Storyline:" in setup:
        characters_start = setup.index("Main Characters:") + len("Main Characters:")
        storyline_start = setup.index("Storyline:") + len("Storyline:")
        characters = setup[characters_start:storyline_start].strip()
        storyline = setup[storyline_start:].strip()
    else:
        characters = "Unknown characters"
        storyline = "Unknown storyline"

    # Generate movie script using Groq
    script_prompt = (
        f"Write a movie script based on the theme: '{theme}', with main characters: {characters}, and storyline: {storyline}."
    )
    script_response = client.chat(messages=[
        system_message,
        {"role": "user", "content": script_prompt}
    ])
    script = script_response["choices"][0]["message"]["content"]

    return characters, storyline, script

def main():
    st.title("Movie Script Generator")
    st.write("Generate movie scripts, characters, and storylines based on a single theme.")

    theme = st.text_input("Enter the movie theme", placeholder="e.g., Space Exploration, Love Story, Thriller")

    if st.button("Generate Content"):
        if theme:
            characters, storyline, script = generate_movie_content(theme)

            st.subheader("Main Characters")
            st.text(characters)

            st.subheader("Storyline")
            st.text(storyline)

            st.subheader("Movie Script")
            st.text_area("", script, height=300)
        else:
            st.warning("Please enter a theme to generate content.")

if __name__ == "__main__":
    main()
