# App to allow user to select visualisations from summative.ipynb and understand conclusions interactively

from shiny import App, ui, render
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr

# Reach final combined_df from notebook
from to_final_df import load_and_prepare_data
combined_df = load_and_prepare_data()

# Variables for user to select
variables = [
    "Happiness Score",
    "GDP per cap",
    "Family",
    "Life Expectancy",
    "Freedom",
    "Corruption",
    "Generosity",
    "Unemployment"
]

# UI

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "x_var",
            "Select X variable:",
            choices=variables,
            selected="GDP per cap"
        ),
        ui.input_select(
            "y_var",
            "Select Y variable:",
            choices=variables,
            selected="Happiness Score"
        ),
    ),
    ui.h2("Interactive Exploration of World Happiness Data"),
    ui.output_plot("regression_plot"),
    ui.hr(),
    ui.output_text("model_stats"),
)

# Server

def server(input, output, session):

    @output
    @render.plot
    def regression_plot():
        x = input.x_var()
        y = input.y_var()

        # Prevent X = Y
        if x == y:
            return None

        df_clean = combined_df[[x, y]].dropna()

        plt.figure(figsize=(8, 5))

        sns.regplot(
            data=df_clean,
            x=x,
            y=y,
            scatter=False,  # match notebook style
            line_kws={"linewidth": 2, "color": "darkorchid"}
        )

        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f"{y} vs {x}")
        plt.tight_layout()

        return plt.gcf()

    @output
    @render.text
    def model_stats():
        x = input.x_var()
        y = input.y_var()

        if x == y:
            return "Please select two different variables."

        df_clean = combined_df[[x, y]].dropna()

        # Regression for R²
        X = df_clean[[x]].values
        Y = df_clean[y].values
        model = LinearRegression().fit(X, Y)
        r2 = model.score(X, Y)

        # Pearson correlation
        r, p = pearsonr(df_clean[x], df_clean[y])

        return (
            f"Pearson r: {r:.3f}\n"
            f"p-value: {p:.3f}\n"
            f"R-squared: {r2:.3f}"
        )
    
# App
app = App(app_ui, server)