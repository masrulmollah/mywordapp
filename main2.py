import streamlit as st
import pandas as pd
import os

# Function to save words to a local file
def save_words(file_path, df):
    df.to_csv(file_path, index=False)

# Function to load words from the file if it exists and has data
def load_words(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=['Class', 'Word'])

# Function to delete a word from the dataframe
def delete_word(df, word_to_delete):
    return df[df['Word'] != word_to_delete]

# Main App
def main():
    st.title("My Word App")

    # File to save words
    file_path = "words.csv"

    # Load existing words from the CSV file
    if "word_data" not in st.session_state:
        st.session_state.word_data = load_words(file_path)

    # Get unique classes
    unique_classes = st.session_state.word_data['Class'].unique().tolist()

    # Tabs at the top: "View Words" and "Add Word"
    main_tab, add_tab = st.tabs(["View Words", "Add Word"])

    with main_tab:
        if unique_classes:
            # Create separate tabs for each class
            class_tabs = st.tabs(unique_classes)

            for i, class_name in enumerate(unique_classes):
                with class_tabs[i]:
                    class_data = st.session_state.word_data[st.session_state.word_data['Class'] == class_name]

                    for word in class_data['Word']:
                        col1, col2 = st.columns([4, 2])
                        col1.write(word)
                        if col2.button("Delete", key=f"delete_{word}"):
                            st.session_state.word_data = delete_word(st.session_state.word_data, word)
                            save_words(file_path, st.session_state.word_data)
                            st.experimental_rerun()  # Refresh the app to update the view

        else:
            st.write("No classes available yet. Please add words in the 'Add Word' tab.")

    with add_tab:
        #st.subheader("Add New Word")

        # Option to select an existing class or add a new one
        existing_class = st.selectbox("Select an existing class:", [""] + unique_classes)
        new_class = st.text_input("Or enter a new class:")

        # Determine the class to use
        word_class = new_class if new_class else existing_class

        # Input fields
        word = st.text_input("Enter the new word:")

        if st.button("Add Word"):
            if word and word_class:
                new_word = pd.DataFrame([[word_class, word]], columns=['Class', 'Word'])
                st.session_state.word_data = pd.concat([st.session_state.word_data, new_word], ignore_index=True)
                save_words(file_path, st.session_state.word_data)
                st.success(f"Word '{word}' added successfully!")
                st.experimental_rerun()  # Refresh the app to update the class list
            else:
                st.warning("Please enter the word and select or add a class.")

if __name__ == "__main__":
    main()
