import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Theatre Lesson Plan Generator", page_icon="🎭", layout="wide")

st.title("🎭 Theatre Lesson Plan Generator")
st.markdown("Aap apni Theme, Theatre Style, Grade aur Sessions ki sankhya yahan dalein, aur app aapke template ke anusar poora lesson plan taiyar kar dega[cite: 1]!")

# Sidebar for Inputs
st.sidebar.header("📝 Input Parameters")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")
theme = st.sidebar.text_input("Theme Name", "The Living World")
theatre_style = st.sidebar.selectbox("Theatre Style", ["Mime", "Clowning", "Object Theatre", "Puppetry", "Nukkad Natak", "Physical Theatre"])
grade = st.sidebar.selectbox("Grade", ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8"])
num_sessions = st.sidebar.slider("Number of Sessions", min_value=2, max_value=20, value=16, step=2)

if st.sidebar.button("Generate Lesson Plan"):
    if not api_key:
        st.error("Kripya apni Gemini API Key darj karein!")
    else:
        genai.configure(api_key=api_key)
        # Using Gemini 2.5 Flash or Pro
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"""
        You are an expert Theatre Curriculum Designer and Educator. Create a comprehensive, professional theatre lesson plan based on the following details and template structure:
        
        - Theme: {theme}
        - Theatre Style: {theatre_style}
        - Grade: {grade}
        - Total Number of Sessions: {num_sessions}
        
        Follow this strict template format for all sessions:
        1. LEARNING GOAL: One-line learning objective for {grade} students working on role, voice, body language, expression, and theme "{theme}"[cite: 1].
        2. WORKING GOALS: Must start with "To..." focusing on the entire session skills[cite: 1].
        3. SESSION-WISE BREAKDOWN (Day, Content, Session Goal, Skills using Bloom's Taxonomy level-based words like Identify, Apply, Create, Location, Time, Grade, Teacher)[cite: 1]:
           - Hook (5-7 mins): Teacher-led, video/demonstration, includes a Thinking Routine with steps for children[cite: 1].
           - Core (~20 mins): Student-led skill building, starting with "In the continuation of the session the students will...", step-by-step instructions, group/pair/individual activity, and one reflective question[cite: 1].
           - Closure & AFL: Starting with "To reflect on their learning students will...", naming the AFL tool used[cite: 1].
           - Stickability: One focused keyword[cite: 1].
           
        Generate all {num_sessions} sessions in a clean, tabular or structured format matching the school template.
        """
        
        with st.spinner("Generating your structured theatre lesson plan..."):
            try:
                response = model.generate_content(prompt)
                st.success("Lesson Plan Successfully Generated!")
                st.markdown(response.text)
                
                # Download option
                st.download_button(
                    label="Download Lesson Plan as Text",
                    data=response.text,
                    file_name=f"Theatre_Lesson_Plan_{theme.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error aagaya: {e}")
