## 📺 Netflix Visualization Project
## Final Project – Data Visualization Course

🌟 Overview
This repository contains my final visualization project analyzing patterns in Netflix’s global catalog of movies and TV shows. Using a curated subset of the popular Kaggle Netflix Movies and TV Shows dataset, this project explores:

-How Netflix content has evolved over time
-Which genres and ratings dominate the platform
-Which countries contribute the most titles
-Relationships between release year, content type, country, and genre

The project includes data cleaning, exploratory analysis, visualization prototyping, user evaluation, and a final interactive visualization.

## 📂 Repository Structure
netflix-visualization-project/
│
├── data/
│   ├── netflix_titles.csv
│   └── netflix_titles_subset_3000.csv
│
├── notebooks/
│   └── netflix_visualization.ipynb
│
├── src/
│   ├── load_data.py
│   ├── preprocessing.py
│   └── charts.py
│
├── sketches/
│   └── (low-fidelity prototypes here)
│
└── README.md

## 📊 Data Description

This project uses the public Netflix Movies and TV Shows dataset from Kaggle (8,807 records). Each record contains metadata describing a title available on Netflix, including:

-type (Movie or TV Show)
-title
-director/cast
-country
-date_added
-release_year
-rating
-duration
-listed_in (genres)
-description

# To ensure smooth performance with Altair visualizations, a 3,000-row subset of the dataset was sampled using:
df_subset = df_full.sample(n=3000, random_state=42)

## 🧭 Part 1 – Goals, Tasks, and Initial Critique
# 🎯 Goals
1-Understand how Netflix content changes over time
2-Identify dominant genres and ratings
3-Explore geographic patterns in content production

# 📝 Tasks
-Compare counts of Movies vs TV Shows over release years
-Identify top genres based on frequency
-Compare countries by number of titles produced

# 🔍 Critique of Existing Visualizations

Existing Netflix charts often suffer from:
-Overly long category lists (genres, countries)
-Random color palettes
-Lack of interactivity
-Overplotting in map visualizations

This project addresses these limitations through filtering, simplified groupings, consistent color design, and interactive Altair components.

## Part 2 – Task Decomposition & Prototypes

# Task 1 – Explore Time Trends
-Why: Understand how Netflix content grows
-How: Time-series chart
-Target Data: release_year, type

# Task 2 – Explore Genre Distribution
-Why: Identify dominant genres
-How: Bar chart with interactive filtering
-Target Data: listed_in (first genre)

# Task 3 – Explore Country Contributions
-Why: Understand geographic differences
-How: Bar chart (or choropleth)
-Target Data: country

# 📸 Low-Fidelity Prototypes
Sketches for these visualizations are included in the /sketches/ directory.

## 🔍 Part 3 – Evaluation Plan

# ❓ Evaluation Question
Can users accurately understand Netflix’s content trends through this visualization?

# 👥 Participants

Three non-expert users:
-A classmate
-A colleague
-A family member

# 📏 Measures
- Accuracy (Are their answers correct?)
- Insight depth (Can they identify meaningful trends?)
- Efficiency (How quickly can they use filters?)
- Usability rating (1–5 scale)

# 🧪 Method: Think-Aloud Protocol

Participants:
1- View the visualization
2-Answer a set of questions aloud
3-Provide usability feedback afterward

# ✔ Success Criteria

* ≥ 80% correct answers
* ≥ 2 meaningful insights identified
* Usability ≥ 4/5

##  📊 Final Visualization

* The final interactive visualization includes:
* Time-series chart of content by release year
* Genre distribution bar chart (Top 10 genres)
* Country comparison chart
* Hover tooltips and dropdown filters
* Consistent red/blue Netflix-inspired color palette


