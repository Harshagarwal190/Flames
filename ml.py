import numpy as np
import pickle
import streamlit as st

# Load the pre-trained model
try:
    loaded_model = pickle.load(open("newModel.sav", "rb"))
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'newModel.sav' is in the correct directory.")
    st.stop()

# Prediction function
def predict_compatibility(input_data):
    """
    Predicts compatibility using the loaded model.
    :param input_data: List of features for prediction
    :return: Compatibility message
    """
    np_array = np.array(input_data)
    reshaped_array = np_array.reshape(1, -1)  # Reshape to 2D array as required by the model
    try:
        prediction = loaded_model.predict(reshaped_array)
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return "Error during prediction"
    
    return "💞 Couple is compatible!" if prediction[0] == 1 else "💔 Couple is not compatible."

# Streamlit configuration
st.set_page_config(
    page_title="FLAMES Compatibility Predictor",
    page_icon="🔥",
    layout="centered",
    menu_items={
        'Report a bug': "https://github.com/Defalt-here/FLAMES-couple-predictor/issues",
        'About': "Check your compatibility with the power of ML. Training dataset from Kaggle: https://www.kaggle.com/datasets/mexwell/speed-dating/data"
    }
)

# Main app function
def main():
    # Custom Header
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #FF5733;">🔥FLAMES Compatibility Predictor</h1>
            <p style="font-size: 18px;">Discover your compatibility with the power of Machine Learning!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add an image or emoji
    #st.image("https://via.placeholder.com/600x200.png?text=FLAMES+Compatibility", use_column_width=True)

    # Formatted instructions
    st.markdown("""
        **How it works:**  
        Rate your target on the following questions (1-10).  
        For dataset details, see the "About" section above.
    """)
    
    st.markdown("---")  # Horizontal line for separation

    # Use columns for better layout
    col1, col2 = st.columns(2)

    # Input fields in columns
    with col1:
        gender_option = st.selectbox("Select your gender:", ("Male", "Female"))
        gender = 1 if gender_option == "Male" else 0

        met_option = st.selectbox("Have you met before?", ("Met before", "Not met"))
        met = 1 if met_option == "Met before" else 0

        age = st.number_input("Enter your age:", min_value=0, step=1)

    with col2:
        attraction = st.slider("How attracted are you to the person?", 0, 10, 5)
        sincerity = st.slider("How sincere is the person?", 0, 10, 5)
        intelligence = st.slider("How intelligent is the person?", 0, 10, 5)
        funny = st.slider("How funny is the person?", 0, 10, 5)
        ambition = st.slider("How ambitious is the person?", 0, 10, 5)
        interests = st.slider("How many shared interests do you have?", 0, 10, 5)
        overall = st.slider("What overall score would you give the person?", 0, 10, 5)
        reciprocate = st.slider("Do you think the person will reciprocate your emotions?", 0, 10, 5)

    # Compatibility check button with spinner
    if st.button("✨ Check Compatibility ✨"):
        with st.spinner("Calculating compatibility..."):
            compatibility_message = predict_compatibility([gender, age, attraction, sincerity, intelligence, funny, ambition, interests, overall, reciprocate, met])
        st.success(compatibility_message)

        # Visual feedback
        if "compatible" in compatibility_message.lower():
            st.balloons()
        else:
            st.markdown("💔 Better luck next time!")

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center;">
            <p>Made with ❤️ using Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
