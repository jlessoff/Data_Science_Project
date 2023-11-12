# Data_Science_Project
Currently exploring yelp data and NYC restaurant / rodent data 
report and methodology: https://jlessoff.github.io/PDFs/NYC_RESTO.pdf
**Readme updated with help of chatbot 🫡** 
**Stay tuned for improved code organization and documentation 🥲😅** 
**In meantime, please reach out with questions** 


**Restaurant.py:**
Creates interactive maps using Folium to visualize restaurant locations in NYC, color-coded by inspection grade.
Generates heat maps for restaurants with specific grades (A, B, C).

Categorize scores into 'A_rep', 'B_rep', or 'C_rep' based on the value of a_. This is a proxy for health inspection grades.

Data Reading and Preparation:
Reads a CSV file containing New York City zip codes into a pandas DataFrame named neighborhood.
Connects to a public data API (specifically, NYC Open Data) and retrieves restaurant inspection data. The query is limited to 400,000 records.
Converts the API results into a pandas DataFrame and performs various data cleaning steps, such as formatting dates and zip codes, and merging with the neighborhood DataFrame.
Data Transformation and Analysis:

The scores are converted to grades using the previously mentioned function.
Cuisine descriptions are categorized into broader groups like 'Mediterranean', 'European', 'Asian', etc.
Data is filtered to only include inspections from 2019 to 2021.

Data Visualization:
Generates a kernel density plot of inspection scores.
Creates bar charts showing the distribution of grades across different cuisine types.
Generates histograms for score distributions within the top 15 cuisine types.


**EDA Restaurant.py:**
Focusing on inspection scores and their distribution across different types of cuisine.
Score Visualization:

Creates a kernel density plot of health inspection scores using seaborn. This plot gives an idea of the distribution of inspection scores across all restaurants.
Cuisine Categorization:

Defines a dictionary cuisine_map that maps various specific cuisine types to more general categories (e.g., 'Middle Eastern' to 'Mediterranean', 'Chinese' to 'Asian').
Applies this mapping to the cuisine_description column in results_df to categorize each restaurant.
Grade Distribution Analysis:

Implements a function get_cuisine_grade_distribution to calculate the distribution of health inspection grades (A, B, C) across different cuisine types.
The function filters the top n cuisines by their count, computes the proportion of each grade within each cuisine category, and formats the labels for visualization.
Another function plot_grade_distribution creates a horizontal bar chart to visualize this grade distribution.
Score Distribution Analysis:

The function get_cuisine_score_distribution computes the mean and median health inspection scores for the top n cuisine types.
For each of these top cuisines, it plots a histogram of the score distribution and saves these plots to files.
This allows for a detailed analysis of how scores vary across different types of cuisines.
Plotting Functions:



**Rodents.py:**
This script is a tool for visualizing the distribution and frequency of rat sightings in New York City over a specific period. By mapping these data points, it can provide insights into the areas most affected by rat activity, which could be valuable for urban planning, public health, and pest control initiatives.
Fetches data on rat sightings, specifically for the years 2019, 2020, and 2021. The query is limited to a very large number, likely intended to fetch all available data.
The retrieved data is then loaded into a pandas DataFrame named rodent.
Data Cleaning Function (clean_rat_data):

Renames columns for clarity and converts the inspection dates to datetime objects.
Extracts the year from the inspection dates and ensures ZIP codes are in integer format.
Merges the rat sightings data with a neighborhood data frame (not shown in the snippet) to associate each sighting with a specific neighborhood.
The function returns a DataFrame with selected columns including ZIP code, neighborhood, inspection date, result, and year.
Data Aggregation:

Groups the cleaned data by neighborhood to count the number of rat sightings in each neighborhood.
Map Visualization:

Creates a Folium map centered on New York City.
Adds a heatmap layer to the map, visualizing the concentration of rat sightings based on latitude and longitude. The heatmap intensity is determined by the count of sightings at each location.
The map is saved as an HTML file named 'rat_heat_map.html'.

**Rodent_Analysis.py**
Heatmap creation of rats

**CausalAnalysis.py**
Neighborhood Data Processing:

get_zip_data: Reads various CSV files related to ZIP codes, population, and neighborhood data, and merges them to calculate population density and rat sightings density (rat_dens).
merge_zip_data: Merges the restaurant data with the ZIP code data, categorizing population and rat density into quantiles and dropping some columns.
Bayesian Network Analysis:

First, the script creates a DataFrame (df1) with selected violation codes to analyze their relationships.
It then uses bnlearn to build a Directed Acyclic Graph (DAG) using the constraint-based structure learning method (cs).
After structure learning, it performs chi-square independence tests and prints the results in a tabulated format.
The script visualizes this Bayesian network using bn.plot.
The same steps are repeated for df2, which includes all variables from the merged DataFrame, providing a more comprehensive view of the network.
Data Output and Visualization




