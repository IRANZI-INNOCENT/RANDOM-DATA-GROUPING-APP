import os
import pandas as pd
import streamlit as st
import base64

def read_file(uploaded_file):
    file_extension = os.path.splitext(uploaded_file.name)[-1]
    if file_extension == ".csv":
        return pd.read_csv(uploaded_file)
    elif file_extension == ".xlsx":
        return pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None

def group_people(people_df, num_groups, group_names, people_per_group):
    # Shuffle the order of people
    people_df = people_df.sample(frac=1).reset_index(drop=True)

    # Initialize empty groups/create empty groups
    groups = [[] for _ in range(num_groups)]

    # Assign people to groups cyclically
    group_counter = 0
    for i, people in people_df.iterrows():
        if len(groups[group_counter]) < people_per_group:
            groups[group_counter].append(people.tolist())  # Append entire row of people data as list
        else:
            group_counter += 1
            if group_counter >= num_groups:
                group_counter = 0
            groups[group_counter].append(people.tolist())

    # Save each group to a separate CSV file with specified names
    file_links = []
    for i, group in enumerate(groups):
        group_df = pd.DataFrame(group, columns=people_df.columns)  # Use column names from original DataFrame
        csv = group_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Base64 encoding
        href = f'<a href="data:file/csv;base64,{b64}" download="{group_names[i]}.csv">Download {group_names[i]}</a>'
        file_links.append(href)
    
    return file_links

def main():
    st.title("RANDOM GROUPING APP")

    # File upload
    uploaded_file = st.file_uploader("Upload file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        people_df = read_file(uploaded_file)
        
        if people_df is not None:
            # Remove any rows with missing values
            people_df.dropna(inplace=True)
            
            # Number of groups input
            num_groups = st.number_input("Enter the number of groups", min_value=1, step=1)

            # Group names input
            group_names = []
            for i in range(num_groups):
                group_name = st.text_input(f"Enter name for Group {i+1}")
                group_names.append(group_name)

            # Students per group input
            people_per_group = st.number_input("Enter the number per group", min_value=1, step=1)
            
            # Grouping button
            if st.button("GROUP YOUR WORK") and len(group_names) == num_groups:
                file_links = group_people(people_df, num_groups, group_names, people_per_group)
                for link in file_links:
                    st.markdown(link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
