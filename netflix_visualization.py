"""
🎬 Netflix Content Analysis & Interactive Visualization Project

This script performs data loading, cleaning, and visualization on the Netflix Titles
dataset using pandas and Altair.

Main questions explored:
1. How has Netflix’s catalog grown over time?
2. Which genres dominate the platform?
3. How do content ratings differ across genres?
4. Which countries produce the most Netflix titles?
5. How long does it take for titles to be added to Netflix after release?
"""

import pandas as pd
import altair as alt

# Global chart sizing for consistency across visualizations
CHART_WIDTH = 750
CHART_HEIGHT = 350

alt.themes.enable("default")
alt.data_transformers.disable_max_rows()  # allow > 5k rows if needed


# -----------------------------------------------------------------------------
# 1. Load the Dataset
# -----------------------------------------------------------------------------
# The original dataset contains 8,807 rows and is sampled down to 3,000 rows
# to keep Altair visualizations performant.

df_full = pd.read_csv("data/netflix_titles.csv")
print("Full dataset shape:", df_full.shape)

# Quick data overview
df_full.info()
print("\nMissing values per column:\n", df_full.isna().sum())


# -----------------------------------------------------------------------------
# 2. Create 3,000-Row Subset
# -----------------------------------------------------------------------------
# Altair performs best with datasets under ~5,000 rows.
# We generate a random sample of 3,000 rows using a fixed random seed
# for reproducibility and save it into the data folder.

df_subset = df_full.sample(n=3000, random_state=42)
df_subset.to_csv("data/netflix_titles_subset_3000.csv", index=False)
print("\nSubset shape:", df_subset.shape)


# -----------------------------------------------------------------------------
# 3. Data Cleaning
# -----------------------------------------------------------------------------
# Steps:
# - Remove whitespace from string fields
# - Convert date_added to datetime and extract year_added
# - Split duration into numeric value and type
# - Extract primary country
# - Extract main (first-listed) genre

df = df_subset.copy()

# 3.1 Strip whitespace from all object (string) columns
str_cols = df.select_dtypes(include="object").columns
for col in str_cols:
    df[col] = df[col].str.strip()

# 3.2 Parse date_added and extract year_added
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
df["year_added"] = df["date_added"].dt.year.astype("Int64")

# 3.3 Split duration into numeric and type columns
duration_split = df["duration"].str.split(" ", n=1, expand=True)
df["duration_int"] = pd.to_numeric(duration_split[0], errors="coerce")
df["duration_type"] = duration_split[1]

# 3.4 Extract primary country
def get_first_country(x: str | None) -> str | None:
    if pd.isna(x):
        return None
    return x.split(",")[0].strip()

df["country_primary"] = df["country"].apply(get_first_country)

# 3.5 Extract main genre (first listed)
def get_main_genre(x: str | None) -> str | None:
    if pd.isna(x):
        return None
    return x.split(",")[0].strip()

df["main_genre"] = df["listed_in"].apply(get_main_genre)

print("\nCleaned dataframe preview:")
print(df.head())


# -----------------------------------------------------------------------------
# 4. Visualizations (Altair)
# -----------------------------------------------------------------------------
# These visualizations are designed to be viewed in a Jupyter Notebook or
# interactive environment. When run there, each chart variable will display
# the corresponding plot.


# 4.1 Titles by Release Year (Movies vs TV Shows) with interactive slider
df_modern = df[df["release_year"] >= 2004]

year_slider = alt.binding_range(
    min=2004,
    max=int(df_modern["release_year"].max()),
    step=1,
)
year_param = alt.param(
    "Year",
    value=int(df_modern["release_year"].max()),
    bind=year_slider,
)

chart_year_slider = (
    alt.Chart(df_modern)
    .mark_line(point=True)
    .encode(
        x=alt.X(
            "release_year:O",
            axis=alt.Axis(title="Release Year", labelAngle=45),
        ),
        y=alt.Y(
            "count():Q",
            title="Number of Titles",
        ),
        color=alt.Color(
            "type:N",
            title="Content Type",
            scale=alt.Scale(
                # Netflix-inspired colors
                domain=["Movie", "TV Show"],
                range=["#E50914", "#221F1F"],
            ),
        ),
        tooltip=["type", "release_year", "count()"],
    )
    .add_params(year_param)
    .transform_filter("datum.release_year <= Year")
    .properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        title="Netflix Titles by Release Year (2004–Present) – Interactive",
    )
)

# 4.2 Top 10 Netflix Genres (bar chart)
genre_counts = df["main_genre"].value_counts().nlargest(10).reset_index()
genre_counts.columns = ["genre", "count"]

chart_genre_counts = (
    alt.Chart(genre_counts)
    .mark_bar(color="#E50914")  # Netflix red
    .encode(
        x=alt.X("count:Q", title="Number of Titles"),
        y=alt.Y("genre:N", sort="-x", title="Main Genre"),
        tooltip=["genre", "count"],
    )
    .properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        title="Top 10 Netflix Genres",
    )
)


# 4.3 Genre × Rating Category Heatmap
def simplify_rating(r: str | None) -> str:
    if r in ["TV-MA", "R", "NC-17"]:
        return "Mature"
    elif r in ["TV-14", "PG-13"]:
        return "Teen"
    else:
        return "Family/Kids"


df_genre = df[df["main_genre"].notna() & df["rating"].notna()].copy()
df_genre["rating_group"] = df_genre["rating"].apply(simplify_rating)

top_genres = genre_counts["genre"].tolist()
df_genre_top = df_genre[df_genre["main_genre"].isin(top_genres)]

heatmap_simple = (
    alt.Chart(df_genre_top)
    .mark_rect()
    .encode(
        x=alt.X("rating_group:N", title="Rating Category"),
        y=alt.Y("main_genre:N", title="Main Genre", sort=top_genres),
        color=alt.Color(
            "count():Q",
            title="Number of Titles",
            scale=alt.Scale(scheme="reds"),
        ),
        tooltip=["main_genre", "rating_group", "count()"],
    )
    .properties(
        width=CHART_WIDTH * 0.5,
        height=CHART_HEIGHT,
        title="Genre vs. Rating Category",
    )
)


# 4.4 Genre Distribution Over Time (stacked area, normalized)
genre_year = (
    df[df["release_year"] >= 2004]
    .groupby(["release_year", "main_genre"])
    .size()
    .reset_index(name="count")
)
genre_year = genre_year[genre_year["main_genre"].isin(top_genres)]

chart_genre_over_time = (
    alt.Chart(genre_year)
    .mark_area()
    .encode(
        x=alt.X("release_year:O", title="Release Year"),
        y=alt.Y("count:Q", stack="normalize", title="Share of Titles"),
        color=alt.Color("main_genre:N", title="Main Genre"),
        tooltip=["release_year", "main_genre", "count"],
    )
    .properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        title="Relative Genre Share Over Time (Top 10 Genres)",
    )
)


# 4.5 Top Countries Producing Netflix Titles (bar chart)
country_counts = df["country_primary"].value_counts().nlargest(15).reset_index()
country_counts.columns = ["country", "count"]

chart_country_counts = (
    alt.Chart(country_counts)
    .mark_bar(color="#221F1F")
    .encode(
        x=alt.X("count:Q", title="Number of Titles"),
        y=alt.Y("country:N", sort="-x", title="Country"),
        tooltip=["country", "count"],
    )
    .properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        title="Top 15 Countries Producing Netflix Titles",
    )
)


# 4.6 Alternative Country View: Interactive Highlight Bar Chart
highlight = alt.selection_point(on="mouseover", fields=["country"])

chart_country_highlight = (
    alt.Chart(country_counts)
    .mark_bar()
    .encode(
        x=alt.X("count:Q", title="Number of Titles"),
        y=alt.Y("country:N", sort="-x", title="Country"),
        color=alt.condition(
            highlight,
            alt.value("#E50914"),  # highlight in Netflix red
            alt.value("#221F1F"),  # default dark gray
        ),
        tooltip=["country", "count"],
    )
    .add_params(highlight)
    .properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        title="Interactive Country Comparison",
    )
)


# 4.7 Distribution of Lag Between Release and Being Added to Netflix
lag_df = df[df["year_added"].notna()].copy()
lag_df["lag_years"] = lag_df["year_added"] - lag_df["release_year"]

lag_hist = (
    alt.Chart(lag_df)
    .mark_bar()
    .encode(
        x=alt.X(
            "lag_years:Q",
            bin=alt.Bin(step=1),
            title="Years Between Release and Added to Netflix",
        ),
        y=alt.Y("count():Q", title="Number of Titles"),
        color=alt.Color(
            "type:N",
            title="Type",
            scale=alt.Scale(
                domain=["Movie", "TV Show"],
                range=["#E50914", "#221F1F"],
            ),
        ),
        tooltip=["lag_years", "count()"],
    )
    .properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        title="Distribution of Delay Between Release and Being Added to Netflix",
    )
)


# -----------------------------------------------------------------------------
# 5. Conclusion (as comments for reference)
# -----------------------------------------------------------------------------
# The visualizations built in this script support the following findings:
#
# - Netflix’s catalog has grown sharply since the mid-2010s.
# - Dramas, Comedies, Documentaries, and International TV Shows dominate the genre mix.
# - Grouping ratings into Family/Kids, Teen, and Mature improves readability compared
#   to using every individual rating label.
# - The United States and India are the largest content contributors, with strong
#   representation from several other countries.
# - Most titles are added to Netflix within roughly 0–10 years after their original release.
#
# To view the charts interactively, run this script in a Jupyter environment
# (or open the companion .ipynb notebook) and display the chart variables,
# e.g., chart_year_slider, chart_genre_counts, heatmap_simple, etc.

if __name__ == "__main__":
    # When run as a script, just print a brief message.
    # The charts are primarily meant to be viewed in a notebook environment.
    print("\nNetflix visualization script executed.")
    print("Use the accompanying Jupyter notebook to interactively view the charts.")
