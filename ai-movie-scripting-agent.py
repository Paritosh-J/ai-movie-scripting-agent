# import required libs
import os
import json
from dotenv import load_dotenv
import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
from agno.run.agent import RunOutput
from agno.team import Team
from agno.tools.serpapi import SerpApiTools
from textwrap import dedent

# set up streamlit app
st.title("🤖 AI Movie Scripting Agent 🎬✨")
st.caption("Punch in your plot idea, I'll generate full movie script for you...🔥")

# set up API keys
load_dotenv()
anthropic_api_key = os.getenv("GOOGLE_API_KEY")
serp_api_key = os.getenv("SERP_API_KEY")

if anthropic_api_key and serp_api_key:
    script_writer = Agent(
        name="ScriptWriter",
        model=Gemini(id="gemini-2.5-flash", api_key=anthropic_api_key),
        description=dedent(
            """\
        You are an expert screenplay writer. Given a movie idea and genre, 
        develop a compelling script outline with character descriptions and key plot points.
        """
        ),
        instructions=[
            "Write a script outline with 3-5 main characters and key plot points.",
            "Outline the three-act structure and suggest 2-3 twists.",
            "Ensure the script aligns with the specified genre and target audience.",
        ]
    )

    casting_director = Agent(
        name="CastingDirector",
        model=Gemini(id="gemini-2.5-flash", api_key=anthropic_api_key),
        description=dedent(
            """\
        You are a talented casting director. Given a script outline and character descriptions,
        suggest suitable actors for the main roles, considering their past performances and current availability.
        """
        ),
        instructions=[
            "Suggest 2-3 actors for each main role.",
            "Check actors' current status using `search_google`.",
            "Provide a brief explanation for each casting suggestion.",
            "Consider diversity and representation in your casting choices.",
        ],
        tools=[SerpApiTools(api_key=serp_api_key)]
    )

    movie_producers = Team(
        name="MovieProducers",
        model=Gemini(id="gemini-2.5-flash", api_key=anthropic_api_key),
        members=[script_writer, casting_director],
        description="Experienced movie producer overseeing script and casting.",
        instructions=[
            "Ask ScriptWriter for a script outline based on the movie idea.",
            "Pass the outline to CastingDirector for casting suggestions.",
            "Summarize the script outline and casting suggestions.",
            "Provide a concise movie concept overview.",
        ],
        markdown=True,
    )

    # input fields
    movie_idea = st.text_area("Describe what's cooking in your mind...💡 Few sentences will do!")
    genre = st.selectbox(
        "Choose the movie genre🎭",
        ["Action", "Comedy", "Horror", "Romance", "Sci-Fi", "Thriller", "Drama"]
    )
    target_audience = st.selectbox(
        "Whose watching?👀",
        ["General", "Children", "Teens", "Adults", "Mature"]
    )
    movie_runtime = st.slider("How long's the runtime (in minutes)?⌛", 60, 180, 120)

    # agent starts to work
    if st.button("Generate Script📝"):
        with st.spinner("Scripting your cool idea...✍️"):
            try:
                input_text = (
                    f"Movie idea: {movie_idea}\n"
                    f"Genre: {genre}\n"
                    f"Target audience: {target_audience}\n"
                    f"Movie runtime: {movie_runtime} mins\n"
                )
                # get response from agent
                response: RunOutput = movie_producers.run(input_text, stream=False)

                # Normalize content
                content = getattr(response, "content", "")
                parsed = None
                try:
                    parsed = json.loads(content) if isinstance(content, str) else None
                except Exception:
                    parsed = None

                # If the agent returned a JSON with an "error" key, hide it by default
                if isinstance(parsed, dict) and "error" in parsed:
                    st.error(
                        "🥵 Looks like I'm overloaded — please try again later. 🥲")
                    # Show details only if developer mode enabled or user explicitly asks
                    dev_mode = os.getenv("DEV_MODE", "false").lower() == "true"
                    if dev_mode:
                        with st.expander("🔧 Technical details (DEV MODE)"):
                            st.code(json.dumps(parsed, indent=2), language="json")
                    else:
                        if st.checkbox("Show technical details"):
                            st.code(json.dumps(parsed, indent=2), language="json")
                else:
                    # Safe to show normal content
                    st.write(content)

            except Exception as e:
                # Best-effort: try to parse exception text as JSON (some libs return JSON text in the exception)
                raw_error = str(e)
                pretty = raw_error
                try:
                    parsed_exc = json.loads(raw_error)
                    pretty = json.dumps(parsed_exc, indent=2)
                except Exception:
                    parsed_exc = None

                # If it's a Gemini-style JSON error, don't dump it on UI by default
                if isinstance(parsed_exc, dict) and "error" in parsed_exc:
                    st.error(
                        "🥵 Looks like I'm overloaded — please try again later. 🥲")
                    dev_mode = os.getenv("DEV_MODE", "false").lower() == "true"
                    if dev_mode:
                        with st.expander("🔧 Technical details (DEV MODE)"):
                            st.code(pretty, language="json")
                    else:
                        if st.checkbox("Show technical details (error encountered)"):
                            st.code(pretty, language="json")
                else:
                    st.error("😵 An unexpected error occurred.")
                    with st.expander("Technical details"):
                        st.code(pretty)

    st.info(
        "⚠️ Usage limits for this app ⚠️  \n"
        "Requests Per Minute : 10 requests  \n"
        "Requests Per Day : 250 requests"
    )
