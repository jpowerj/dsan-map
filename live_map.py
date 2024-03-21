import copy
import json

import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from country_list import countries_for_language
from streamlit_gsheets import GSheetsConnection
# import pydeck as pdk
# import folium
# from streamlit_folium import st_folium

# Geocoding
geocoder = Nominatim(user_agent="dsan-live-map")

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# # Print results
# for row in df.itertuples():
#     loc_str = f"{row.city}, {row.state}, {row.country}"
#     st.write(loc_str)
#     location = geocoder.geocode(loc_str).raw
#     # Print raw data
#     st.write(location)


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
    st.subheader(f'Welcome to Georgetown, from {city}!')

# df = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

#m = folium.Map(location=CENTER_START, zoom_start=8)
#fg = folium.FeatureGroup(name="Markers")
#for marker in st.session_state["markers"]:
#    fg.add_child(marker)

#st_folium(
#    m,
#    center=st.session_state["center"],
#    zoom=st.session_state["zoom"],
#    key="new",
#    feature_group_to_add=fg,
#    height=400,
#    width=700,
#)


# _ZOOM_LEVELS = [
#     360,
#     180,
#     90,
#     45,
#     22.5,
#     11.25,
#     5.625,
#     2.813,
#     1.406,
#     0.703,
#     0.352,
#     0.176,
#     0.088,
#     0.044,
#     0.022,
#     0.011,
#     0.005,
#     0.003,
#     0.001,
#     0.0005,
#     0.00025,
# ]

# def _get_zoom_level(distance: float) -> int:
#     """Get the zoom level for a given distance in degrees.

#     See https://wiki.openstreetmap.org/wiki/Zoom_levels for reference.

#     Parameters
#     ----------
#     distance : float
#         How many degrees of longitude should fit in the map.

#     Returns
#     -------
#     int
#         The zoom level, from 0 to 20.

#     """
#     for i in range(len(_ZOOM_LEVELS) - 1):
#         if _ZOOM_LEVELS[i + 1] < distance <= _ZOOM_LEVELS[i]:
#             return i

#     # For small number of points the default zoom level will be used.
#     return 12

# def _get_viewport_details(
#     data: pd.DataFrame, lat_col_name: str, lon_col_name: str, zoom: int | None
# ) -> tuple[int, float, float]:
#     """Auto-set viewport when not fully specified by user."""
#     min_lat = data[lat_col_name].min()
#     max_lat = data[lat_col_name].max()
#     min_lon = data[lon_col_name].min()
#     max_lon = data[lon_col_name].max()
#     center_lat = (max_lat + min_lat) / 2.0
#     center_lon = (max_lon + min_lon) / 2.0
#     range_lon = abs(max_lon - min_lon)
#     range_lat = abs(max_lat - min_lat)

#     if zoom is None:
#         if range_lon > range_lat:
#             longitude_distance = range_lon
#         else:
#             longitude_distance = range_lat
#         zoom = _get_zoom_level(longitude_distance)

#     return zoom, center_lat, center_lon

# def to_deckgl_json(
#     df,
#     size: None | str | float,
#     color,
#     map_style: str | None,
#     zoom: int | None,
# ) -> str:

#     lat_col_name = 'lat'
#     lon_col_name = 'lon'
#     size_arg = size
#     color_arg = color

#     # Drop columns we're not using.
#     # (Sort for tests)
#     used_columns = sorted(
#         [
#             c
#             for c in {lat_col_name, lon_col_name}
#             if c is not None
#         ]
#     )
#     df = df[used_columns]

#     #color_arg = _convert_color_arg_or_column(df, color_arg, color_col_name)

#     zoom, center_lat, center_lon = _get_viewport_details(
#         df, lat_col_name, lon_col_name, zoom
#     )

#     default = copy.deepcopy(_DEFAULT_MAP)
#     default["initialViewState"]["latitude"] = center_lat
#     default["initialViewState"]["longitude"] = center_lon
#     default["initialViewState"]["zoom"] = zoom
#     default["layers"] = [
#         {
#             "@@type": "ScatterplotLayer",
#             "getPosition": f"@@=[{lon_col_name}, {lat_col_name}]",
#             "getRadius": size_arg,
#             "radiusMinPixels": 3,
#             "radiusUnits": "meters",
#             "getFillColor": color_arg,
#             "data": df.to_dict("records"),
#         }
#     ]

#     if map_style:
#         if not config.get_option("mapbox.token"):
#             raise StreamlitAPIException(
#                 "You need a Mapbox token in order to select a map type. "
#                 "Refer to the docs for st.map for more information."
#             )
#         default["mapStyle"] = map_style

#     return json.dumps(default)

# #map_style = None


st.map(df, size=2500, use_container_width=True, zoom=7)

# deck.setProps({
#         viewState: {zoom}
#       });
# print(type(map_obj))
# print(dir(map_obj))

# st.pydeck_chart(pdk.Deck(
#     map_style=None,
#     initial_view_state=pdk.ViewState(
#         latitude=37.76,
#         longitude=-122.4,
#         zoom=11,
#         pitch=50,
#     ),
#     layers=[
#         pdk.Layer(
#            'HexagonLayer',
#            data=chart_data,
#            get_position='[lon, lat]',
#            radius=200,
#            elevation_scale=4,
#            elevation_range=[0, 1000],
#            pickable=True,
#            extruded=True,
#         ),
#         pdk.Layer(
#             'ScatterplotLayer',
#             data=chart_data,
#             get_position='[lon, lat]',
#             get_color='[200, 30, 0, 160]',
#             get_radius=200,
#         ),
#     ],
# ))