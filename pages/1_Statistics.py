import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Statistcis", layout="wide")
st.title("Powerlifting Statistics")


df = pd.read_csv("powerlifting_cleaned.csv", low_memory=False)
df = df.melt(
    id_vars=['Name', 'Sex', 'Event', 'Equipment', 'Age', 'AgeClass',
       'BirthYearClass', 'Division', 'BodyweightKg', 'WeightClassKg',
       'Squat1Kg', 'Squat2Kg', 'Squat3Kg', 'Best3SquatKg', 'Bench1Kg',
       'Bench2Kg', 'Bench3Kg', 'Best3BenchKg', 'Deadlift1Kg', 'Deadlift2Kg',
       'Deadlift3Kg', 'Best3DeadliftKg', 'TotalKg', 'Place', 'Dots', 'Wilks',
       'Glossbrenner', 'Goodlift', 'Tested', 'Country', 'Federation',
       'ParentFederation', 'Date', 'MeetCountry', 'MeetTown', 'MeetName',
       'Sanctioned'],
    value_vars=['IPF_WeightClass', 'Traditional_WeightClass'],
    var_name='WeightClassType',
    value_name='WeightClass'
)

df = df.melt(
    id_vars=df.columns.difference(['Best3SquatKg', 'Best3BenchKg', 'Best3DeadliftKg', 'TotalKg']),
    value_vars=['Best3SquatKg', 'Best3BenchKg', 'Best3DeadliftKg', 'TotalKg'],
    var_name='Lift',
    value_name='ResultKg'
)

df['Lift'] = df['Lift'].map({
    'Best3SquatKg': 'Squat',
    'Best3BenchKg': 'Bench Press',
    'Best3DeadliftKg': 'Deadlift',
    'TotalKg': 'Total'
})

df['Sex'] = df['Sex'].map({
    'F': 'Female',
    'M': 'Male'
})

sex = st.sidebar.selectbox("Select gender:", ['Female', 'Male'], index=None, key = 'sex')
weight_class_type = st.sidebar.selectbox("Select weight and age class type:", ['IPF', 'Traditional'], index=None, key = 'weight_class_type')
if weight_class_type == 'IPF':
    age_column = 'BirthYearClass'
else:
    age_column = 'AgeClass'

available_age_classes = sorted(df[age_column].dropna().unique())
available_age_classes = [cls for cls in available_age_classes if cls != '5-12']
selected_age_class = st.sidebar.selectbox("Select age class:", available_age_classes, index=None, key='age_class')

if weight_class_type == 'IPF':
    weight_classes = ['43kg', '47kg', '52kg', '57kg', '63kg', '69kg', '76kg', '84kg', '84+kg'] if sex == 'Female' else \
                     ['53kg', '59kg', '66kg', '74kg', '83kg', '93kg', '105kg', '120kg', '120+kg']
else:
    weight_classes = ['44kg', '48kg', '52kg', '56kg', '60kg', '67.5kg', '75kg', '82.5kg', '90kg', '90+kg'] if sex == 'Female' else \
                     ['52kg', '56kg', '60kg', '67.5kg', '75kg', '82.5kg', '90kg', '100kg', '110kg', '125kg', '140kg', '140+kg']

weight_class = st.sidebar.selectbox("Select weight class", weight_classes, index=None, key='weight_class')

# Filtrowanie i wykres
if sex and weight_class_type and weight_class and selected_age_class:
    filtered_df = df[
        (df['Sex'] == sex) &
        (df['WeightClassType'] == f"{weight_class_type}_WeightClass") &
        (df['WeightClass'] == weight_class) &
        (df[age_column] == selected_age_class)
    ]
    st.write(f"{sex} lifters – {weight_class} ({weight_class_type}) in age class {selected_age_class}")
    st.write(f"Number of lifters: {len(filtered_df)}")

    if not filtered_df.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            lifts_df = filtered_df[filtered_df['Lift'] != 'Total']
            fig_lifts = px.box(
                lifts_df,
                x="Lift",
                y="ResultKg",
                points=None,
            )
            fig_lifts.update_layout(xaxis_title="", yaxis_title="Result (kg)", boxmode="group")
            st.plotly_chart(fig_lifts, use_container_width=True)
        with col2:
            total_df = filtered_df[filtered_df['Lift'] == 'Total']
            fig_total = px.box(
                total_df,
                x="Lift",
                y="ResultKg",
                points=None,
            )
            fig_total.update_layout(xaxis_title = "", yaxis_title="Result (kg)", boxmode="group")
            st.plotly_chart(fig_total, use_container_width=True)
        st.subheader("Records:")

        for lift in ["Squat", "Bench Press", "Deadlift", "Total"]:
            top_lift = filtered_df[filtered_df["Lift"] == lift]
            top_lift = top_lift[["Name", "ResultKg", "Date"]].sort_values(by="ResultKg", ascending=False).iloc[0]
            st.write(f"**{lift}** — {top_lift['Name']} : {top_lift['ResultKg']}kg ({top_lift['Date']})")
    else:
        st.warning("No data available for the selected filters.")
else:
    st.info("Please select all filters in the sidebar.")