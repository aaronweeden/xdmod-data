import plotly.graph_objects as go
import plotly.io as pio

pio.templates["timeseries"] = go.layout.Template(
    layout={
        'hoverlabel': {
            'bgcolor': 'white'
        },
        'plot_bgcolor': 'white',
        'colorway': ["#1199FF",
                     "#DB4230",
                     "#4E665D",
                     "#F4A221",
                     "#66FF00",
                     "#33ABAB",
                     "#A88D95",
                     "#789ABC",
                     "#FF99CC",
                     "#00CCFF",
                     "#FFBC71",
                     "#A57E81",
                     "#8D4DFF",
                     "#FF6666",
                     "#CC99FF",
                     "#2F7ED8",
                     "#0D233A",
                     "#8BBC21",
                     "#910000",
                     "#1AADCE",
                     "#492970",
                     "#F28F43",
                     "#77A1E5",
                     "#3366FF",
                     "#FF6600",
                     "#808000",
                     "#CC99FF",
                     "#008080",
                     "#CC6600",
                     "#9999FF",
                     "#99FF99",
                     "#969696",
                     "#FF00FF",
                     "#FFCC00",
                     "#666699",
                     "#00FFFF",
                     "#00CCFF",
                     "#993366",
                     "#3AAAAA",
                     "#C0C0C0",
                     "#FF99CC",
                     "#FFCC99",
                     "#CCFFCC",
                     "#CCFFFF",
                     "#99CCFF",
                     "#339966",
                     "#FF9966",
                     "#69BBED",
                     "#33FF33",
                     "#6666FF",
                     "#FF66FF",
                     "#99ABAB",
                     "#AB8722",
                     "#AB6565",
                     "#990099",
                     "#999900",
                     "#CC3300",
                     "#669999",
                     "#993333",
                     "#339966",
                     "#C42525",
                     "#A6C96A",
                     "#111111"],
        'xaxis': {
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': '#5078a0'
            },
            'color': '#606060',
            'ticks': 'outside',
            'ticklen': 10,
            'tickcolor': '#c0cfe0',
            'gridcolor': '#bfc0c0',
            'linecolor': '#c0cfe0',
            'showgrid': False,
            'zerolinecolor': '#c0cfe1',
            'showline': True,
            'zerolinewidth': 4,
            'tickformat': "%Y-%m-%d"
        },
        'yaxis': {
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': '#1199FF'
            },
            'color': '#606060',
            'gridcolor': '#bfc0c0',
            'linecolor': '#c0cfe0',
            'zerolinecolor': '#c0cfe1',
            'showline': True,
            'zerolinewidth': 4
        },
        'title': {
            'font': {
                'color': '#444b6e',
                'size': 16
            }
        },
        'hovermode': 'closest',
        'showlegend': True,
        'legend': {
            'orientation': 'h',
            'y': -0.2
        },
        'margin': {
            't': 50
        }
    }
)
