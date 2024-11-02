import streamlit as st
import plotly.express as px
import pandas as pd

# Sample Data
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 11, 12, 13, 14]
})

st.title("Interactive Scatter Plot with Questionnaire")

# Scatter plot
fig = px.scatter(df, x='x', y='y')
scatter_plot = st.plotly_chart(fig)

# Questionnaire visibility toggle
if st.session_state.get("show_questionnaire", False):
    st.write("### Questionnaire")
    st.text_input("Question 1", "Your answer here")
    st.button("Submit", on_click=lambda: st.session_state.update(show_questionnaire=False))
else:
    if st.button("Show Questionnaire"):
        st.session_state.show_questionnaire = True

