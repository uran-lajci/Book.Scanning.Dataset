import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv('pca_result.csv')

# Create the scatter plot
fig = px.scatter(
    df,
    x='PC1',
    y='PC2',
    color='source',
    hover_data=['instance_name']  # Include instance_name in hover data
)

# Customize hover template to show only the instance name
fig.update_traces(
    hovertemplate='<b>%{customdata[0]}</b><extra></extra>'
)

# Adjust layout for better readability
fig.update_layout(
    title='PCA Visualization (Hover to See Instance Names)',
    xaxis_title='Principal Component 1 (PC1)',
    yaxis_title='Principal Component 2 (PC2)'
)

# Display the plot
fig.show()