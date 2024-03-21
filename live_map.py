import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from country_list import countries_for_language

st.markdown(
        """
       <style>
       [data-testid="stSidebar"][aria-expanded="true"]{
           width: 400px;
       }
       """,
        unsafe_allow_html=True,
    )   

country_tuples = countries_for_language('en')
country_names_noUS = sorted([country_tuple[1] for country_tuple in country_tuples if country_tuple[1] != "United States"])
country_names = ['United States'] + country_names_noUS

# From https://gist.github.com/JeffPaine/3083347
state_abbr_to_name = {
    # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#States.
    "AK": "Alaska",
    "AL": "Alabama",
    "AR": "Arkansas",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MO": "Missouri",
    "MS": "Mississippi",
    "MT": "Montana",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NE": "Nebraska",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VA": "Virginia",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming",
    # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Federal_district.
    "DC": "District of Columbia",
    # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Inhabited_territories.
    "AS": "American Samoa",
    "GU": "Guam GU",
    "MP": "Northern Mariana Islands",
    "PR": "Puerto Rico PR",
    "VI": "U.S. Virgin Islands",
}
state_names = sorted(state_abbr_to_name.values())

st.subheader('DSAN Admitted Students')

st.sidebar.title("Welcome! Where are you from?")
with st.sidebar.form(key ='LocationForm'):
    country_placeholder = st.empty()
    state_placeholder = st.empty()
    city = st.text_input("City", "")
    #province = st.text_input("Province", "Ontario")
    #country = st.text_input("Country", "United States")
    loc_submit = st.form_submit_button(label = 'Add to map &rarr;')

with country_placeholder:
    country = st.selectbox('Country', country_names)

with state_placeholder:
    if country == "United States":
        state = st.selectbox("State", state_names)

if loc_submit:
    st.subheader(f'Welcome to Washington, DC, from {city}!')

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(df)
