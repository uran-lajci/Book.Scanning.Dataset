from pathlib import Path

import argparse
import pandas as pd
import plotly.express as px


def main(features_path: Path) -> None:
    if not features_path.is_file():
        raise FileNotFoundError(f'File does not exist: {features_path}')

    features_df = pd.read_csv(features_path)

    fig = px.scatter(
        features_df,
        x='PC1',
        y='PC2',
        color='source',
        hover_data=['instance_name']
    )

    # Customize hover template to show only the instance name
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><extra></extra>')

    fig.update_layout(
        title='Feature Visualization (Hover to See Instance Names)',
        xaxis_title='Principal Component 1',
        yaxis_title='Principal Component 2'
    )
    
    fig.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--features_path', type=Path, 
                        default='temp_data/reduced_features.csv')

    args = parser.parse_args()
    main(args.features_path)
