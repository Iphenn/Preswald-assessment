from preswald import text, plotly, connect, get_df, table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Display welcome messages
text("# Welcome to Preswald!")
text("This is your first app. 🎉")

# Load the CSV data
connect()  # Load in all sources, which by default is the sample_csv
df = get_df('life_expectancy_data_csv')

# Create the initial scatter plot
fig = px.scatter(
    df, 
    x='Total expenditure', 
    y='BMI', 
    text='Country',
    title='Life Expectancy vs. BMI',
    labels={
        'Total expenditure': 'Total Expenditure', 
        'BMI': 'BMI'
    },
    hover_data={
        'Country': True,  # Show country name
        'Total expenditure': True,  # Show Total expenditure
        'BMI': True,  # Show BMI
        'Life expectancy': True  # Show Life expectancy if available
    }
)

# Update the trace to adjust the marker size and color
fig.update_traces(
    mode='markers',  # Show only the points initially (no text)
    marker=dict(size=12, color='lightblue'),  # Set marker size and color
    textposition='top center'  # Position text outside the points
)

# Style the plot
fig.update_layout(template='plotly_white')

# Create frames for each year, to animate the plot over years
frames = [
    go.Frame(
        data=[
            go.Scatter(
                x=df[df['Year'] == year]['Total expenditure'],
                y=df[df['Year'] == year]['BMI'],
                mode='markers',
                text=df[df['Year'] == year]['Country'],
                marker=dict(size=12, color='lightblue')
            )
        ],
        name=str(year)  # Name of the frame corresponds to the year
    )
    for year in df['Year'].unique()
]

# Add the frames to the figure
fig.frames = frames

# Update layout to include the slider and animation controls
fig.update_layout(
    sliders=[{
        'steps': [
            {
                'args': [
                    [str(year)],  # Set frame to the selected year
                    {
                        'frame': {'duration': 300, 'redraw': True},  # Smooth transition
                        'mode': 'immediate',
                        'transition': {'duration': 300}
                    }
                ],
                'label': str(year),
                'method': 'animate'
            }
            for year in df['Year'].unique()
        ],
        'currentvalue': {
            'font': {'size': 20},
            'prefix': 'Year: ',
            'visible': True,
            'xanchor': 'center'
        }
    }],
    updatemenus=[
        {
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }
    ]
)

# Show the plot with the slider
plotly(fig)

# Show the data table
table(df)