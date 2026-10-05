import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Advanced Theatre Lesson Plan Generator", page_icon="🎭", layout="wide")

st.title("🎭 Advanced Theatre Lesson Plan & Curriculum Generator")
st.markdown("Aap apni Theme, Elaboration, Theatre Form aur Sessions ki sankhya yahan dalein, aur app ek comprehensive, resource-rich aur interactive lesson plan taiyar karega!")

# Comprehensive Theatre Forms Database with Associated Skills
THEATRE_FORMS = {
    "Mime": {
        "description": "Non-verbal performance focusing on gestures, facial expressions, and body movement without words.",
        "skills": ["Spatial Awareness", "Body Isolation", "Exaggerated Expression", "Precision", "Imaginative Object Interaction"]
    },
    "Clowning": {
        "description": "Physical comedy, slapstick, and emotional vulnerability through playfulness and direct connection with the audience.",
        "skills": ["Comic Timing", "Vulnerability", "Physical Comedy", "Spontaneity", "Audience Engagement"]
    },
    "Object Theatre": {
        "description": "Animating inanimate everyday objects or props to represent characters or abstract ideas.",
        "skills": ["Metaphorical Thinking", "Object Manipulation", "Voice Projection for Objects", "Spatial Economy"]
    },
    "Puppetry (Sock / Shadow / Hand)": {
        "description": "Bringing puppets to life through synchronized hand movements, voice modulation, and light manipulation.",
        "skills": ["Fine Motor Coordination", "Voice Disassociation", "Rhythm & Sync", "Visual Storytelling"]
    },
    "Nukkad Natak (Street Play)": {
        "description": "High-energy, social-issue-based public theatre using chorus singing, clapping, formation changes, and loud projection.",
        "skills": ["Vocal Projection", "Ensemble Coordination", "Rhythmic Chanting", "Social Critique", "Physical Formations"]
    },
    "Physical Theatre": {
        "description": "Storytelling primarily through movement, choreography, acrobatics, and bodily expression rather than dialogue.",
        "skills": ["Core Strength", "Flexibility", "Ensemble Trust", "Kinesthetic Awareness", "Choreographic Memory"]
    },
    "Improvisation (Improv)": {
        "description": "Unscripted, spontaneous performance based on audience suggestions and instant creative collaboration.",
        "skills": ["Active Listening", "Spontaneous Problem Solving", "Yes-And Mindset", "Quick Adaptability"]
    }
}

# Sidebar for Inputs
st.sidebar.header("📝 Configuration Panel")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")

theme = st.sidebar.text_input("Theme Name", "The Living World")
theme_elaboration = st.sidebar.text_area("Elaborate the Theme (Context & Details)", 
    "Focusing on ecosystems, animal habitats, interdependence of nature, and empathy towards wildlife.")

theatre_style = st.sidebar.selectbox("Theatre Style / Form", list(THEATRE_FORMS.keys()))

# Display selected theatre form details & skills in sidebar
st.sidebar.markdown(f"**Form Description:** {THEATRE_FORMS[theatre_style]['description']}")
st.sidebar.markdown(f"**Key Skills Targeted:** {', '.join(THEATRE_FORMS[theatre_style]['skills'])}")

grade = st.sidebar.selectbox("Grade", ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10"])
num_sessions = st.sidebar.slider("Number of Sessions", min_value=4, max_value=24, value=16, step=2)

# Optional Reference Materials
st.sidebar.header("🎬 Reference & Support (Optional)")
ref_video = st.sidebar.text_input("Reference Video Link (YouTube/Drive)", placeholder="Paste URL here")
ref_audio_notes = st.sidebar.text_input("Audio / Voice Modulation Notes", placeholder="e.g., High pitch for birds, deep bass for lion")

if st.sidebar.button("Generate Advanced Lesson Plan"):
    if not api_key:
        st.error("Kripya apni Gemini API Key darj karein!")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Selected form skills mapping
        form_skills = ", ".join(THEATRE_FORMS[theatre_style]['skills'])
        
        prompt = f"""
        You are an expert Master Theatre Curriculum Designer and Educator. Create a comprehensive, professional, and structured theatre lesson plan based on the following parameters:
        
        - Theme: {theme}
        - Theme Elaboration / Context: {theme_elaboration}
        - Theatre Style: {theatre_style}
        - Core Form Skills to Integrate: {form_skills}
        - Grade: {grade}
        - Total Number of Sessions: {num_sessions}
        - Reference Material / Videos context: {ref_video if ref_video else 'Standard educational visual references'}
        - Audio & Voice Modulation Guidance: {ref_audio_notes if ref_audio_notes else 'Incorporate character-specific voice modulation and soundscape cues.'}
        
        Follow this strict curriculum structure:
        1. LEARNING GOAL: A clear one-line learning objective for {grade} students working on role, voice, body language, expression, and the theme context.
        2. WORKING GOALS: Must start with "To..." focusing on core competencies across the sessions.
        3. BASIC RESOURCES LIST: List required props, sound tools, spatial setups, and costume elements.
        4. SESSION-WISE BREAKDOWN (From Session 1 to Session {num_sessions}):
           For each session include: Day/Session #, Content, Session Goal, Skills (using Bloom's Taxonomy words like Identify, Apply, Create), Location, Time, Grade, Teacher.
           - Hook (5-7 mins): Teacher-led demonstration/video discussion, including a Thinking Routine with clear step-by-step instructions for children.
           - Core (~20 mins): Student-led skill building starting with "In the continuation of the session the students will...", step-by-step group/pair/individual activities, and one reflective question. Include specific audio/voice modulation cues where applicable.
           - Closure & AFL: Starting with "To reflect on their learning students will...", naming the AFL tool used.
           - Stickability: One focused core keyword.
           
        5. FINAL SESSIONS (Climax / Scriptwork for last few sessions):
           Provide tailored small devised theatre scripts and group task guidelines based on the theme '{theme}' and style '{theatre_style}' for students to perform during the concluding days.
        """
        
        with st.spinner("Generating your advanced multi-feature theatre curriculum..."):
            try:
                response = model.generate_content(prompt)
                st.success("Advanced Curriculum Successfully Generated!")
                st.markdown(response.text)
                
                # Download option
                st.download_button(
                    label="Download Complete Lesson Plan as Text",
                    data=response.text,
                    file_name=f"Advanced_Theatre_Plan_{theme.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error aagaya: {e}")
