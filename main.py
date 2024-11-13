import streamlit as st

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = 1
    st.session_state['results'] = {}

# Function to navigate to the next page
def next_page():
    st.session_state['page'] += 1

# Function to store results
def store_results(test_name, result):
    st.session_state['results'][test_name] = result
    next_page()

# Feedback logic for each test
def get_feedback(test_name, score):
    if test_name == "PHQ-9":
        if score <= 4:
            return "Minimal or no depressive symptoms. Maintain healthy habits and monitor any future changes. **Seeking support is a sign of strength, not weakness.**"
        elif score <= 9:
            return "Mild depressive symptoms. Reflect on stressors and explore strategies like mindfulness or exercise. **Seeking support is a sign of strength, not weakness.**"
        elif score <= 14:
            return "Moderate depressive symptoms. Consider seeking counseling or talking to someone you trust. **Seeking support is a sign of strength, not weakness.**"
        elif score <= 19:
            return "Moderately severe depression. Discuss symptoms with a healthcare provider. **Seeking support is a sign of strength, not weakness.**"
        else:
            return "Severe depression, including possible suicidal thoughts. Seek immediate professional support. **Seeking support is a sign of strength, not weakness.**"

    elif test_name == "Rosenberg":
        if score <= 10:
            return "Low self-esteem. Reflect on areas where you feel unsupported or undervalued. **Seeking support is a sign of strength, not weakness.**"
        elif score <= 20:
            return "Moderate self-esteem. Recognize strengths and explore growth areas. **Seeking support is a sign of strength, not weakness.**"
        else:
            return "High self-esteem. Maintain confidence and positive self-view. **Seeking support is a sign of strength, not weakness.**"

    elif test_name == "STAI-5":
        if score <= 9:
            return "Low anxiety. You likely feel calm and secure in most situations. **Seeking support is a sign of strength, not weakness.**"
        elif score <= 14:
            return "Moderate anxiety. Consider relaxation techniques or talking to someone if it persists. **Seeking support is a sign of strength, not weakness.**"
        else:
            return "High anxiety. This may be significantly impacting your daily life. Seek professional help. **Seeking support is a sign of strength, not weakness.**"

def get_cssrs_feedback(responses):
    if responses["Q6"] == "Yes":
        return """**High Risk (Behavior)**: Your responses show recent actions or preparations toward ending your life. 
        This places you at immediate risk. It’s crucial to speak with a mental health professional as soon as possible. 
        **Seeking support is a sign of strength, not weakness.**"""
    
    if responses.get("Q3") == "Yes" or responses.get("Q4") == "Yes" or responses.get("Q5") == "Yes":
        return """**High Risk (Ideation)**: Your responses indicate serious concerns, including thoughts of suicide with a potential plan or intent. 
        This is a sign that you’re struggling with significant emotional pain. Please reach out to a mental health professional or trusted individual immediately. 
        **Seeking support is a sign of strength, not weakness.**"""
    
    if responses["Q1"] == "Yes" or responses["Q2"] == "Yes":
        return """**Moderate Risk**: Your responses suggest some distress or emotional pain, which may include thoughts about death or general hopelessness. 
        While these feelings don’t necessarily indicate immediate danger, it’s important to talk to someone you trust or reach out to a counselor. 
        **Seeking support is a sign of strength, not weakness.**"""
    
    return """**Low Risk**: Your responses indicate no current signs of suicidal thoughts or behaviors. It’s important to continue prioritizing your mental well-being. 
    If you ever feel overwhelmed, don’t hesitate to seek support from friends, family, or a mental health professional. 
    **Seeking support is a sign of strength, not weakness.**"""

# Test pages with forms to submit
def phq9_page():
    st.title("PHQ-9: Depression Assessment")
    with st.form("PHQ-9"):
        scores = []
        questions = [
            "Little interest or pleasure in doing things.",
            "Feeling down, depressed, or hopeless.",
            "Trouble falling or staying asleep, or sleeping too much.",
            "Feeling tired or having little energy.",
            "Poor appetite or overeating.",
            "Feeling bad about yourself — or that you are a failure or have let yourself or your family down.",
            "Trouble concentrating on things, such as reading or watching television.",
            "Moving or speaking slowly, or being fidgety or restless.",
            "Thoughts of being better off dead or self-harm."
        ]

        for question in questions:
            scores.append(st.radio(question, ["Not at all", "Several days", "More than half the days", "Nearly every day"], index=0))

        submitted = st.form_submit_button("Next")
        if submitted:
            numeric_scores = [scores.index(choice) for choice in scores]
            store_results("PHQ-9", sum(numeric_scores))

def rosenberg_page():
    st.title("Rosenberg Self-Esteem Scale")
    with st.form("Rosenberg"):
        scores = []
        questions = [
            "I am satisfied with myself.",
            "At times, I think I am no good at all.",
            "I have a number of good qualities.",
            "I can do things as well as most people.",
            "I feel I do not have much to be proud of.",
            "I feel useless at times.",
            "I feel that I’m a person of worth.",
            "I wish I could have more respect for myself.",
            "I feel like a failure.",
            "I take a positive attitude toward myself."
        ]

        for question in questions:
            scores.append(st.radio(question, ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], index=0))

        submitted = st.form_submit_button("Next")
        if submitted:
            numeric_scores = [(1 if i in [1, 4, 5, 7, 8] else 0) + scores.index(choice) for i, choice in enumerate(scores)]
            store_results("Rosenberg", sum(numeric_scores))

def stai5_page():
    st.title("STAI-5: Anxiety Assessment")
    with st.form("STAI-5"):
        scores = []
        questions = [
            "I feel calm.",
            "I feel secure.",
            "I feel tense.",
            "I feel upset.",
            "I feel worried."
        ]

        for question in questions:
            scores.append(st.radio(question, ["Almost Never", "Sometimes", "Often", "Almost Always"], index=0))

        submitted = st.form_submit_button("Next")
        if submitted:
            numeric_scores = [4 - scores.index(choice) if i in [0, 1] else scores.index(choice) + 1 for i, choice in enumerate(scores)]
            store_results("STAI-5", sum(numeric_scores))

def cssrs_page():
    st.title("C-SSRS: Columbia Suicide Severity Rating Scale")
    with st.form("C-SSRS"):
        responses = {}
        responses["Q1"] = st.radio("Have you wished you were dead or wished you could go to sleep and not wake up?", ["No", "Yes"], index=0)
        responses["Q2"] = st.radio("Have you actually had any thoughts about killing yourself?", ["No", "Yes"], index=0)
        if responses["Q2"] == "Yes":
            responses["Q3"] = st.radio("Have you been thinking about how you might do this?", ["No", "Yes"], index=0)
            responses["Q4"] = st.radio("Have you had these thoughts and had some intention of acting on them?", ["No", "Yes"], index=0)
            responses["Q5"] = st.radio("Have you started to work out or worked out the details of how to kill yourself? Did you intend to carry out this plan?", ["No", "Yes"], index=0)
        responses["Q6"] = st.radio("Have you done anything, started to do anything, or prepared to do anything to end your life?", ["No", "Yes"], index=0)
        if responses["Q6"] == "Yes":
            responses["Q6_recent"] = st.radio("If yes, was this within the past 3 months?", ["No", "Yes"], index=0)

        submitted = st.form_submit_button("Next")
        if submitted:
            store_results("C-SSRS", get_cssrs_feedback(responses))

def feedback_page():
    st.title("Feedback and Interpretation")
    results = st.session_state['results']
    for test_name, feedback in results.items():
        st.subheader(f"{test_name} Results")
        st.write(feedback)
        st.write("---")

# Page navigation logic
if st.session_state.page == 1:
    phq9_page()
elif st.session_state.page == 2:
    rosenberg_page()
elif st.session_state.page == 3:
