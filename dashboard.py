import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

# --- Load Data ---
CSV_FILE_PATH = "results/evaluation_scores.csv"

def load_data():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except FileNotFoundError:
        print(f"Warning: {CSV_FILE_PATH} not found. Creating empty DataFrame.")
        df = pd.DataFrame(columns=[
            'faithfulness', 'answer_relevancy', 'context_recall', 'context_precision',
            'question', 'answer', 'contexts', 'ground_truth'
        ])
    return df

df = load_data()

# --- Initialize the Dash App ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "RAG Evaluation Dashboard"

# --- Helper Function to Create Metric Cards ---
def create_metric_card(title, value):
    
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title"),
            html.H2(f"{value:.2f}", className="card-text"),
        ]),
        color="dark",
        inverse=True, 
        className="text-center m-2"
    )

# --- Calculate Average Scores ---
avg_faithfulness = df['faithfulness'].mean()
avg_answer_relevancy = df['answer_relevancy'].mean()
avg_context_recall = df['context_recall'].mean()
avg_context_precision = df['context_precision'].mean()

# --- Dark Mode Table Style ---

table_dark_style = {
    'style_data': {
        'backgroundColor': '#343a40', 
        'color': 'white',
        'whiteSpace': 'normal',
        'height': 'auto',
    },
    'style_header': {
        'backgroundColor': '#222',
        'color': 'white',
        'fontWeight': 'bold',
    },
    'style_cell': {
        'textAlign': 'left',
        'padding': '10px',
    },
    'style_filter': {
        'backgroundColor': '#555',
        'color': 'white',
    },
}

app.layout = dbc.Container([
    # 1. Header
    html.H1("⚖️ RAG Application Evaluation Dashboard", className="my-4 text-center"),
    html.Hr(),

    # 2. Average Score Cards
    html.H2("📊 Average Performance Metrics", className="mt-4"),
    dbc.Row([
        dbc.Col(create_metric_card("Faithfulness", avg_faithfulness), width=3),
        dbc.Col(create_metric_card("Answer Relevancy", avg_answer_relevancy), width=3),
        dbc.Col(create_metric_card("Context Recall", avg_context_recall), width=3),
        dbc.Col(create_metric_card("Context Precision", avg_context_precision), width=3),
    ]),
    html.Hr(),

    # 3. Failed Questions Analysis (Interactive)
    html.H2("⚠️ Failed Question Analysis", className="mt-4"),
    html.P("Use the dropdown and slider to filter for low-scoring questions."),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Select Metric:"),
                    dcc.Dropdown(
                        id='metric-filter-dropdown',
                        options=[
                            {'label': 'Faithfulness', 'value': 'faithfulness'},
                            {'label': 'Answer Relevancy', 'value': 'answer_relevancy'},
                            {'label': 'Context Recall', 'value': 'context_recall'},
                            {'label': 'Context Precision', 'value': 'context_precision'}
                        ],
                        value='faithfulness'
                    )
                ], width=6),
                dbc.Col([
                    dbc.Label("Score Threshold:"),
                    dcc.Slider(
                        id='threshold-slider',
                        min=0, max=1, step=0.1, value=0.7,
                        marks={i/10: str(i/10) for i in range(0, 11)}
                    )
                ], width=6)
            ]),
            html.H4("Filtered Results:", className="mt-4"),
            html.Div(id='filtered-results-table'),
        ]),
        color="dark",
        inverse=True,
        className="mt-3"
    ),
    
    html.Hr(),

    # 4. Detailed Full Results Table
    html.H2("🔬 Detailed Full Results", className="mt-4"),
    dash_table.DataTable(
        id='full-data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        sort_action="native",
        filter_action="native",
        **table_dark_style # UPDATED: Applying the dark style
    )
], fluid=True)

# --- Define Callbacks (Interactivity) ---
@app.callback(
    Output('filtered-results-table', 'children'),
    [Input('metric-filter-dropdown', 'value'),
     Input('threshold-slider', 'value')]
)
def update_filtered_table(metric_to_filter, threshold):
    # Reload the data in case it changed
    df_filtered = load_data()
    
    if df_filtered.empty:
        return dbc.Alert("No data found. Please run evaluate.py first.", color="info")
        
    df_filtered = df_filtered[df_filtered[metric_to_filter] <= threshold]

    if df_filtered.empty:
        return dbc.Alert("No questions found below this threshold. Good job!", color="success")

    # Return a new DataTable
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_filtered.columns],
        data=df_filtered.to_dict('records'),
        **table_dark_style 
    )

# --- Run the App ---
if __name__ == '__main__':
    print("Dash server starting... Go to http://127.0.0.1:8050/")
    
    app.run(debug=True)