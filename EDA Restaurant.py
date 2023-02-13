import pandas as pd
from Restaurants import results_df
from textwrap import wrap
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


###SCORE
fig, ax = plt.subplots()
sns.kdeplot(results_df["score"], shade=True, ax=ax)
ax.legend()
fig.suptitle("Health Inspection Violations Density")
plt.show()
###CUISINE
pd.set_option('display.max_columns', None)
#

# #

cuisine_map = {
    'Middle Eastern': 'Mediterranean',
    'Moroccan': 'Mediterranean',
    'Tapas': 'Mediterranean',
    'Spanish': 'Mediterranean',
    'Greek': 'Mediterranean',
    'Armenian': 'Mediterranean',
    'Basque': 'Mediterranean',
    'Afghan': 'Mediterranean',
    'Iranian': 'Mediterranean',
    'Turkish': 'Mediterranean',
    'Scandinavian': 'European',
    'Czech': 'European',
    'English': 'European',
    'German': 'European',
    'Portuguese': 'European',
    'Russian': 'European',
    'Polish': 'European',
    'Continental': 'European',
    'Irish': 'European',
    'French': 'European',
    'Eastern European': 'European',
    'Pizza/Italian': 'Pizza',
    'Chinese': 'Asian',
    'Japanese': 'Asian',
    'Chinese/Japanese': 'Asian',
    'Filipino': 'Asian',
    'Indian': 'Asian',
    'Indonesian': 'Asian',
    'Bangladeshi': 'Asian',
    'Thai': 'Asian',
    'Korean': 'Asian',
    'Chinese/Cuban': 'Asian',
    'Vietnamese/Cambodian/Malaysia': 'Asian',
    'Bottled beverages, including water, sodas, juices, etc.': 'Beverages',
    'Café/Coffee/Tea': 'Beverages',
    'Bagels/Pretzels': 'Baked Goods',
    'Donuts': 'Baked Goods',
    'Chilean': 'Latin/Caribbean',
    'Peruvian': 'Latin/Caribbean',
    'Caribbean': 'Latin/Caribbean',
    'Brazilian': 'Latin/Caribbean',
    'Latin (Cuban, Dominican, Puerto Rican, South & Central American)': 'Latin/Caribbean',
    'Ice Cream, Gelato, Yogurt, Ices': 'Specialty',
    'Seafood': 'Specialty',
    'Chicken': 'Specialty',
    'Nuts/Confectionary': 'Specialty',
    'Hotdogs/Pretzels': 'Specialty',
    'Hotdogs': 'Specialty',
    'Fruits/Vegetables': 'Specialty',
    'Vegetarian': 'Specialty',
    'Salads': 'Specialty',
    'Steak': 'Specialty',
    'Juice, Smoothies, Fruit Salads': 'Specialty',
    'Pancakes/Waffles': 'Specialty',
    'Vegan': 'Specialty',
    'Jewish/Kosher': 'Specialty',
    'Sandwiches': 'Soups & Sandwiches',
    'Soups': 'Soups & Sandwiches',
    'Soup/Sandwiches': 'Soups & Sandwiches',
    'Delicatessen': 'Deli/Buffett',
    'Sandwiches/Salads/Mixed Buffet': 'Deli/Buffett',
    'Soul Food': 'American',
    'Californian': 'American',
    'Creole/Cajun': 'American',
    'Cajun': 'American',
    'Creole': 'American',
    'Barbecue': 'American',
    'Tex-Mex': 'American',
    'Southwestern': 'American',
    'Hamburgers': 'American',
    'Hawaiian': 'American'
}

results_df['cuisine_description'] = results_df['cuisine_description'].map(cuisine_map)
def get_cuisine_grade_distribution(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    """
    Get the distribution of restaurant grades (A, B, C) by cuisine type.

    Args:
        df: The DataFrame containing restaurant data.
        top_n: The number of top cuisines to include in the output.

    Returns:
        A DataFrame with the grade distribution for the top n cuisine types.
    """
    # Get the top n cuisine types by count of restaurants
    cuisines = df['cuisine_description'].value_counts().head(top_n).index.tolist()
    
    # Filter the DataFrame to include only the top n cuisine types and the relevant columns
    cuisinegrade = df[['cuisine_description', 'c', 'score']]
    cuisinegrade = cuisinegrade[cuisinegrade['cuisine_description'].isin(cuisines)]
    cuisinegrade = cuisinegrade[cuisinegrade.c.isin(['A_rep', 'B_rep', 'C_rep'])]
    cuisinegrade = cuisinegrade.reset_index().drop('index', axis=1)
    
    # Calculate the percentage of restaurants with each grade for each cuisine type
    cg = pd.crosstab(cuisinegrade['cuisine_description'], cuisinegrade.c)
    cgdensity = cg.apply(lambda r: r/r.sum(), axis=1)
    cgdensity = cgdensity.sort_values(by='A_rep')
    
    # Format the cuisine names for better readability in the plot
    cglabels = list(cgdensity.index)
    cglabels = ['\n'.join(wrap(l, 20)) for l in cglabels]
    
    return cgdensity, cglabels

def plot_grade_distribution(cgdensity: pd.DataFrame, cglabels: list) -> None:
    """
    Plot the grade distribution for each cuisine type.

    Args:
        cgdensity: The DataFrame with the grade distribution for each cuisine type.
        cglabels: The formatted cuisine names for the plot.
    """
    # Set the plot parameters
    plt.figure(figsize=(10, 8))
    plt.xlim(0, 1.15)
    plt.xlabel('Percentage of restaurants')
    plt.ylabel('')
    plt.title('Grade Distribution by Cuisine Type')
    plt.set_cmap('Set2')
    
    # Plot the horizontal stacked bar chart
    cgdensity.plot(kind='barh', stacked=True, mark_right=True)
    
    # Add the formatted cuisine names as y-axis labels
    plt.yticks(range(len(cglabels)), cglabels)
    plt.tight_layout()
    
    # Save the plot to a file
    plt.savefig('gradebycuisine.png')

def get_cuisine_score_distribution(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Get the score distribution for each cuisine type.

    Args:
        df: The DataFrame containing restaurant data.
        top_n: The number of top cuisines to include in the output.

    Returns:
        A DataFrame with the mean and median scores for the top n cuisine types.
    """
    # Get the top n cuisine types by count of restaurants
    cuisines = df['cuisine_description'].value_counts().head(top_n).index.tolist()
    
    # Filter the DataFrame to include only the top n cuisine types and the relevant columns
    cuisinegrade = df[['cuisine_description', 'score']]
    cuisinegrade = cuisinegrade[cuisinegrade['cuisine_description'].isin(cuisines)]
    
    # Calculate the mean and median scores for each cuisine type
    rows = []
    for cuisine in cuisines:
        score = cuisinegrade.loc[cuisinegrade['cuisine_description'] == cuisine, 'score']
        mean_score = round(np.mean(score), 1)
        median_score = round(np.median(score), 1)
        name = cuisine[:15]
        rows.append([name, mean_score, median_score])
        
        # Plot the score distribution for each cuisine type
        plt.hist(score, label=name, bins=int(np.max(score.values)/2))
        plt.title(f'Score Distribution for {name} Restaurants')
        plt.axvline(x=median_score, color='r', label=f'Median = {median_score}')
        plt.axvline(x=mean_score, color='g', label=f'Mean = {mean_score}')
        plt.legend()
        plt.savefig(f'{name}_score_distribution.png')
        plt.clf()
    
    # Create a DataFrame with the mean and median scores for each cuisine type
    df = pd.DataFrame(rows, columns=["Name", "Mean", "Median"])
    
    return df

def plot_score_density(df: pd.DataFrame) -> None:
    """
    Plot the density of health inspection violation scores.

    Args:
        df: The DataFrame containing restaurant data.
    """
    # Set the plot parameters
    plt.figure(figsize=(8, 6))
    plt.title('Health Inspection Violations Density')
    
    # Plot the score density using the seaborn library
    sns.kdeplot(df['score'], shade=True)
    
    # Save the plot to a file
    plt.savefig('health_inspection_violations_density.png')

# Call the functions to generate and plot the cuisine score distribution data
cuisine_scores = get_cuisine_score_distribution(results_df)
plot_score_density(results_df)

# Call the functions to generate and plot the grade distribution data
cgdensity, cglabels = get_cuisine_grade_distribution(results_df)
plot_grade_distribution(cgdensity, cglabels)

