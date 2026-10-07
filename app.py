import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Autonomous Theatre Curriculum Search Engine", page_icon="🎭", layout="wide")

st.title("🎭 Autonomous Theatre Curriculum & Lesson Plan Search Engine")
st.markdown("Sirf apni **Theme** aur **Theatre Style** daliye. Yeh smart search engine bachchon ke liye sabse creative aur structured session-wise workpath taiyar karegi!")

# Comprehensive Theatre Forms Database with Core Skill Sets
THEATRE_FORMS = {
    "Mime": "Non-verbal performance focusing on gestures, facial expressions, body isolation, spatial awareness, and precision.",
    "Clowning": "Physical comedy, slapstick, emotional vulnerability, comic timing, spontaneity, and direct audience connection.",
    "Object Theatre": "Animating everyday props, metaphorical thinking, object manipulation, and spatial economy.",
    "Puppetry (Sock / Shadow / Hand)": "Fine motor coordination, voice disassociation, rhythm, sync, and visual storytelling.",
    "Nukkad Natak (Street Play)": "High-energy public theatre, vocal projection, ensemble coordination, rhythmic chanting, and social critique.",
    "Physical Theatre": "Storytelling through movement, choreography, core strength, ensemble trust, and kinesthetic awareness.",
    "Improvisation (Improv)": "Unscripted spontaneous performance, active listening, 'Yes-And' mindset, and quick adaptability.",
    "Custom / Experimental Form": "User-defined dynamic performance style combining multi-disciplinary arts and expression."
}

# Sidebar Input Panel (Clean & Search-Engine Style)
st.sidebar.header("🔍 Search & Curriculum Parameters")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")

theme = st.sidebar.text_input("Enter Theme Name", "The Living World")
theme_description = st.sidebar.text_area("Describe the Theme / Context", 
    "Focusing on animal habitats, ecosystems, interdependence of nature, and empathy towards wildlife.")

theatre_style_selection = st.sidebar.selectbox("Select Theatre Style / Form", list(THEATRE_FORMS.keys()))

if theatre_style_selection == "Custom / Experimental Form":
    custom_style = st.sidebar.text_input("Specify Custom Theatre Style", "Mask Theatre & Movement")
    theatre_style = custom_style
else:
    theatre_style = theatre_style_selection

grade = st.sidebar.selectbox("Select Target Grade", ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10"])
num_sessions = st.sidebar.slider("Number of Sessions required", min_value=4, max_value=24, value=8, step=2)

if st.sidebar.button("Search & Generate Creative Workpath"):
    if not api_key:
        st.error("Kripya apni Gemini API Key darj karein!")
    else:
        genai.configure(api_key=api_key)
        
        # Using standard gemini-flash model
        model = genai.GenerativeModel("gemini-flash")
        
        prompt = f"""
        You are an elite Autonomous Theatre Curriculum Search Engine and Master Playwright Educator. 
        Your task is to design a highly creative, resource-rich, and structured theatre workpath based on the user's input.
        
        Input Parameters:
        - Theme: {theme}
        - Theme Context / Description: {theme_description}
        - Theatre Style / Form: {theatre_style}
        - Base Form Description: {THEATRE_FORMS.get(theatre_style_selection, 'Dynamic theatre pedagogy')}
        - Grade Level: {grade}
        - Total Number of Sessions: {num_sessions}
        
        Please structure your response into the following clear sections:
        
        1. 🌐 THEME INTELLIGENCE & SUB-TOPICS:
           Analyze the theme and list 4-5 creative sub-topics, conceptual prompts, and learning angles that will help {grade} students connect deeply with the theme through theatre.
           
        2. 🎯 OVERALL LEARNING & WORKING GOALS:
           - LEARNING GOAL: A precise one-line learning objective for {grade} students integrating role, voice, body language, expression, and the theme.
           - WORKING GOALS: Must start with "To..." outlining core theatrical competencies across the sessions.
           
        3. 🎒 BASIC RESOURCES & PROPS:
           List essential low-cost props, spatial requirements, and audio soundscape tools needed.
           
        4. 📅 SESSION-WISE WORKPATH (Sessions 1 to {num_sessions}):
           For each session, provide:
           - Session # & Content Focus
           - Session Goal & Bloom's Taxonomy Skill Level (e.g., Identify, Apply, Create)
           - Hook (5-7 mins): Teacher-led spark/mini-inquiry, featuring a clear Thinking Routine with step-by-step instructions for students.
           - Core (~20 mins): Student-led skill building beginning with "In the continuation of the session the students will...", structured step-by-step group/pair/individual activities, specific character voice/audio modulation suggestions, and one reflective question.
           - Closure & AFL: Starting with "To reflect on their learning students will...", naming the Assessment for Learning (AFL) tool used.
           - Stickability: One core focused keyword.
           
        5. 🎭 CONCLUDING STAGEWORK & SMALL SCRIPTS:
           For the final sessions, provide tailored small devised theatre scripts, dialogue pieces, and group task guidelines based on '{theme}' and '{theatre_style}' for students to perform as a climax.
        """
        
        with st.spinner("Crafting your creative theatre workpath..."):
            try:
                response = model.generate_content(prompt)
                st.success("Creative Theatre Workpath Successfully Generated!")
                st.markdown(response.text)
                
                # Download option
                st.download_button(
                    label="Download Complete Workpath as Text",
                    data=response.text,
                    file_name=f"Theatre_Workpath_{theme.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error aagaya: {e}")
