## 📺 Netflix Visualization Project

This project explores the Netflix Titles dataset through a series of interactive and static visualizations using Python and Altair. The goal is to understand how Netflix’s catalog has evolved, how genres and ratings are distributed, which countries contribute the most content, and how long it takes for a title to be added to Netflix after its original release.

This project was completed as part of a data visualization coursework module and follows a full pipeline—from data selection and cleaning to design, evaluation, and final analysis.

---


## 📂 Repository Structure
Netflix-visualization-project/
│
├── data/
│ ├── netflix_titles.csv
│ ├── netflix_titles_subset_3000.csv
│ └── netflix_titles_clean.csv (optional, created during notebook run)
│
├── notebooks/
│ └── netflix_visualization.ipynb
│
└── README.md


---

## 📊 Dataset Overview

**Source:** Kaggle — *Netflix Movies and TV Shows*  
**Rows:** ~8,800 (subset to 3,000 for responsive visuals)  
**Format:** CSV; tabular data  
**Core Columns Used:**

- `type` — Movie or TV Show  
- `title`  
- `director`, `cast`  
- `country`  
- `date_added` (cleaned → `year_added`)  
- `release_year`  
- `rating` (grouped into rating categories)  
- `duration` (cleaned → `duration_int`, `duration_type`)  
- `listed_in` (cleaned → `main_genre`)

---

## 🧹 Data Cleaning & Feature Engineering

Several transformations were applied:

- Removed trailing whitespace from string fields  
- Converted `date_added` → `datetime` → extracted `year_added`  
- Split `duration` into `duration_int` and `duration_type`  
- Extracted first country into `country_primary`  
- Extracted first genre into `main_genre`  
- Grouped complex ratings into:
  - **Family/Kids**
  - **Teen**
  - **Mature**

These cleaned fields support clearer, more interpretable visualizations.

---

## 🎯 Project Goals & Tasks

The project focuses on three major analytical tasks:

### ✔ Task 1: Understand Netflix's growth over time  
- Why? Explore catalog expansion  
- Means: Line chart + interactive slider  
- Insight: Sharp growth after 2015

### ✔ Task 2: Analyze Netflix’s genre landscape  
- Why? Identify dominant genres  
- Means: Bar charts, heatmap, stacked area chart  
- Insight: Dramas, Comedies, Documentaries dominate

### ✔ Task 3: Examine country-level contributions  
- Why? Understand global distribution  
- Means: Top-15 bar chart & interactive highlight chart  
- Insight: US and India lead, strong diversity overall

### ✔ Task 4: Investigate lag between release & Netflix addition  
- Why? Understand acquisition/publishing behavior  
- Means: Histogram  
- Insight: Many titles added within 0–10 years

---

## 📈 Visualizations Included

### 1. **Netflix Titles Over Time (Interactive Slider)**
Shows yearly growth of Movies vs TV Shows.

### 2. **Top 10 Genres Bar Chart**
Simple, clear comparison of the most common genres.

### 3. **Genre × Rating Category Heatmap**
Grouped ratings → clearer, cleaner interpretation.

### 4. **Genre Share Over Time (Stacked Area Chart)**
Shows how relative genre presence changes since 2004.

### 5. **Top 15 Countries Bar Chart**
Highlights major contributors to Netflix content.

### 6. **Interactive Country Highlight Chart**
Hover-based comparison.

### 7. **Lag Between Release and Netflix Addition (Histogram)**
Shows how long titles take to appear on Netflix.

---

## 🧪 Evaluation Summary

A small think-aloud evaluation with non-expert participants was conducted to assess readability, insightfulness, and usability. Participants correctly interpreted most insights and preferred grouped-axis visuals over cluttered originals. High-level success criteria were met.

---

## 📝 Conclusion

The analysis reveals a rapidly expanding Netflix catalog with strong representation from Drama, Comedy, and International genres. Ratings skew heavily toward Teen and Mature content for most genres. The majority of titles originate from the US and India. Lag analysis shows Netflix increasingly acquires or produces content shortly after release.

---

## 🚀 Future Work

Potential enhancements include:

- Text analysis of movie/TV descriptions  
- Maps for country-based visualizations  
- Director/actor networks  
- Comparative analysis across streaming platforms  
- Deployment as a dashboard (Streamlit or Dash)

---

## ▶ How to Run the Notebook

1. Clone the repository  
2. Ensure the `data/` folder contains the CSV files  
3. Open the project root folder in VS Code or Jupyter  
4. Run all cells from the notebook:

```bash
Kernel → Restart & Run All


### 📘 View the Notebook (Best Rendering)

GitHub sometimes fails to render large Altair visualizations.  
For the most reliable viewing, please use NBViewer:

➡ **https://nbviewer.org/github/NaremanD/fundamentals-of-data-visualization/blob/main/netflix_visualization.ipynb**

