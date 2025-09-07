import streamlit as st
import pandas as pd
from PIL import Image

# Page config
st.set_page_config(page_title="Company Book Explorer", page_icon="🏢", layout="wide")

# Logo and header
image_logo = Image.open('utt_logo.jpg')
col1, col2 = st.columns([9, 1])
with col1:
    st.header("Company Book Explorer")
with col2:
    st.image(image_logo, width=50)

# Load data
df = pd.read_excel("data/Company_book.xlsx")

# Preprocess LOCATION column
df["LOCATION_LIST"] = df["LOCATION"].str.split(",").apply(lambda x: [loc.strip() for loc in x])
df["PROFILS_LIST"] = df["PROFILS"].str.split(",").apply(lambda x: [loc.strip() for loc in x])
# Sidebar filters
st.sidebar.header("Filter Options")

filter_entreprise = st.sidebar.multiselect("Select Entreprise(s):", sorted(df["ENTREPRISE"].unique()))
filter_domaine = st.sidebar.multiselect("Select Domaine(s):", sorted(df["DOMAINE"].unique()))
all_profiles = sorted(set(loc for sublist in df["PROFILS_LIST"] for loc in sublist))
filter_profils = st.sidebar.multiselect("Select Profile(s):",all_profiles)
all_locations = sorted(set(loc for sublist in df["LOCATION_LIST"] for loc in sublist))
filter_location = st.sidebar.multiselect("Select Location(s):", all_locations)
filter_vie= st.sidebar.multiselect("VIE ?", sorted(df["VIE"].unique()))
filter_stage4a= st.sidebar.multiselect("STAGE 4A ?", sorted(df["STAGE4A"].unique()))
min_effectif, max_effectif = st.sidebar.slider("Select Effectif Range:",
                                               int(df["EFFECTIFS"].min()),
                                               int(df["EFFECTIFS"].max()),
                                               (int(df["EFFECTIFS"].min()), int(df["EFFECTIFS"].max())))


# Apply filters
filtered_df = df.copy()

if filter_entreprise:
    filtered_df = filtered_df[filtered_df["ENTREPRISE"].isin(filter_entreprise)]

if filter_vie:
    filtered_df = filtered_df[filtered_df["VIE"].isin(filter_vie)]

if filter_domaine:
    filtered_df = filtered_df[filtered_df["DOMAINE"].isin(filter_domaine)]

if filter_location:
    if "TBD" not in filter_location:
         filter_location.append("TBD")
    filtered_df = filtered_df[filtered_df["LOCATION_LIST"].apply(lambda locs: any(loc in locs for loc in filter_location))]

if filter_profils:
    filtered_df = filtered_df[filtered_df["PROFILS_LIST"].apply(lambda locs: any(loc in locs for loc in filter_profils))]

if filter_stage4a:
    filtered_df = filtered_df[filtered_df["STAGE4A"].apply(lambda locs: any(loc in locs for loc in filter_stage4a))]


filtered_df = filtered_df[(filtered_df["EFFECTIFS"] >= min_effectif) & (filtered_df["EFFECTIFS"] <= max_effectif)]

# Display results

page_numbers_to_extract = filtered_df['PAGE'].to_list()

if page_numbers_to_extract == []:
            st.warning('No slide meets these requirements.')
else:
            current_page = 1
            total_page = len(page_numbers_to_extract)
            for i in page_numbers_to_extract:
                i = int(i)
                st.image(f'img/Brochure_Forum_UTT_2025.1866399641_page-{i:04d}.jpg', caption=f"Slide {current_page} of {total_page}")
                current_page += 1
                st.markdown("""<hr style="height:10px;border:none;color:#002677;background-color:#002677;" /> """, unsafe_allow_html=True)
# Footer
st.markdown("""<hr style="height:10px;border:none;color:#002677;background-color:#002677;" />""", unsafe_allow_html=True)