
# ============================================================
# Import libraries
# ============================================================

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# ============================================================
# Load cleaned dataset
# ============================================================

df = pd.read_csv("e_commerce_cleaned_data.csv")

# ============================================================
# Initialize Dash app
# ============================================================

app = Dash(__name__)

app.title = "E-Commerce Performance Dashboard"


# ============================================================
# Filter values
# ============================================================

companies = sorted(df["Company"].dropna().unique())
years = sorted(df["Year"].dropna().unique())
regions = sorted(df["Region_with_Highest_Sales"].dropna().unique())


# ============================================================
# Reusable styles
# ============================================================

CARD = {
    "padding": "14px 18px",
    "border": "1px solid #dedede",
    "borderRadius": "10px",
    "minWidth": "180px",
    "backgroundColor": "white",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
}


GRAPH_CARD = {
    "backgroundColor": "white",
    "padding": "12px",
    "border": "1px solid #eeeeee",
    "borderRadius": "12px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.04)",
}


# ============================================================
# Dashboard layout
# ============================================================

app.layout = html.Div(
    [
        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        html.H1(
            "E-Commerce Performance Analytics Dashboard",
            style={
                "marginBottom": "4px"
            }
        ),

        html.P(
            "Compare sales, market position, customer scale, "
            "sales per active user, profitability indicators, "
            "regional patterns, and mobile transaction activity "
            "across Amazon, Alibaba, and eBay.",
            style={
                "color": "#555",
                "marginTop": "0"
            },
        ),


        # ----------------------------------------------------
        # Filters
        # ----------------------------------------------------

        html.Div(
            [
                # Company filter

                html.Div(
                    [
                        html.Label("Company"),

                        dcc.Dropdown(
                            id="company-filter",

                            options=[
                                {
                                    "label": company,
                                    "value": company
                                }
                                for company in companies
                            ],

                            value=companies,
                            multi=True,
                        ),
                    ],

                    style={
                        "flex": "1",
                        "minWidth": "220px"
                    }
                ),


                # Year filter

                html.Div(
                    [
                        html.Label("Year"),

                        dcc.Dropdown(
                            id="year-filter",

                            options=[
                                {
                                    "label": str(year),
                                    "value": year
                                }
                                for year in years
                            ],

                            value=years,
                            multi=True,
                        ),
                    ],

                    style={
                        "flex": "1",
                        "minWidth": "220px"
                    }
                ),


                # Region filter

                html.Div(
                    [
                        html.Label("Highest-sales region"),

                        dcc.Dropdown(
                            id="region-filter",

                            options=[
                                {
                                    "label": region,
                                    "value": region
                                }
                                for region in regions
                            ],

                            value=regions,
                            multi=True,
                        ),
                    ],

                    style={
                        "flex": "1",
                        "minWidth": "220px"
                    }
                ),
            ],

            style={
                "display": "flex",
                "gap": "16px",
                "marginBottom": "20px",
                "flexWrap": "wrap",
                "backgroundColor": "white",
                "padding": "16px",
                "borderRadius": "12px",
                "border": "1px solid #eeeeee"
            },
        ),


        # ----------------------------------------------------
        # KPI cards
        # ----------------------------------------------------

        html.Div(
            [
                html.Div(
                    [
                        html.Small("Observations"),
                        html.H3(id="kpi-rows")
                    ],
                    style=CARD
                ),

                html.Div(
                    [
                        html.Small("Average Sales (USD Bn)"),
                        html.H3(id="kpi-sales")
                    ],
                    style=CARD
                ),

                html.Div(
                    [
                        html.Small("Average Active Users (M)"),
                        html.H3(id="kpi-users")
                    ],
                    style=CARD
                ),

                html.Div(
                    [
                        html.Small("Average Market Share (%)"),
                        html.H3(id="kpi-share")
                    ],
                    style=CARD
                ),

                html.Div(
                    [
                        html.Small("Average Operating Income (%)"),
                        html.H3(id="kpi-op")
                    ],
                    style=CARD
                ),
            ],

            style={
                "display": "flex",
                "gap": "12px",
                "flexWrap": "wrap",
                "marginBottom": "20px"
            },
        ),


        # ----------------------------------------------------
        # Row 1
        # Sales per active user trend + annual sales trend
        # ----------------------------------------------------

        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id="sales-user-trend"
                    ),

                    style={
                        **GRAPH_CARD,
                        "flex": "1",
                        "minWidth": "420px"
                    }
                ),

                html.Div(
                    dcc.Graph(
                        id="sales-trend"
                    ),

                    style={
                        **GRAPH_CARD,
                        "flex": "1",
                        "minWidth": "420px"
                    }
                ),
            ],

            style={
                "display": "flex",
                "gap": "16px",
                "flexWrap": "wrap",
                "marginBottom": "16px"
            },
        ),


        # ----------------------------------------------------
        # Row 2
        # Region + sales distribution
        # ----------------------------------------------------

        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id="region-chart"
                    ),

                    style={
                        **GRAPH_CARD,
                        "flex": "1",
                        "minWidth": "420px"
                    }
                ),

                html.Div(
                    dcc.Graph(
                        id="sales-box"
                    ),

                    style={
                        **GRAPH_CARD,
                        "flex": "1",
                        "minWidth": "420px"
                    }
                ),
            ],

            style={
                "display": "flex",
                "gap": "16px",
                "flexWrap": "wrap",
                "marginBottom": "16px"
            },
        ),


        # ----------------------------------------------------
        # Row 3
        # Deviation from overall average
        # ----------------------------------------------------

        html.Div(
            [
                dcc.Graph(
                    id="company-deviation"
                )
            ],

            style=GRAPH_CARD,
        ),
    ],

    style={
        "maxWidth": "1400px",
        "margin": "0 auto",
        "padding": "24px",
        "fontFamily": "Arial",
        "backgroundColor": "#f7f8fa"
    },
)


# ============================================================
# Dashboard callback
# ============================================================

@app.callback(
    Output("kpi-rows", "children"),
    Output("kpi-sales", "children"),
    Output("kpi-users", "children"),
    Output("kpi-share", "children"),
    Output("kpi-op", "children"),

    Output("sales-user-trend", "figure"),
    Output("sales-trend", "figure"),
    Output("region-chart", "figure"),
    Output("sales-box", "figure"),
    Output("company-deviation", "figure"),

    Input("company-filter", "value"),
    Input("year-filter", "value"),
    Input("region-filter", "value"),
)
def update_dashboard(
    selected_companies,
    selected_years,
    selected_regions
):

    # --------------------------------------------------------
    # Handle empty selections
    # --------------------------------------------------------

    selected_companies = selected_companies or []
    selected_years = selected_years or []
    selected_regions = selected_regions or []


    # --------------------------------------------------------
    # Filter data
    # --------------------------------------------------------

    dff = df[
        df["Company"].isin(selected_companies)
        & df["Year"].isin(selected_years)
        & df["Region_with_Highest_Sales"].isin(selected_regions)
    ].copy()


    # --------------------------------------------------------
    # Handle empty filtered dataset
    # --------------------------------------------------------

    if dff.empty:

        blank = px.scatter(
            title="No data for the selected filters"
        )

        blank.update_layout(
            xaxis={
                "visible": False
            },
            yaxis={
                "visible": False
            }
        )

        return (
            "0",
            "—",
            "—",
            "—",
            "—",
            blank,
            blank,
            blank,
            blank,
            blank,
        )


    # ========================================================
    # Figure 1
    # Sales per active user trend by year
    # ========================================================

    sales_user_trend = (
        dff
        .groupby(
            [
                "Year",
                "Company"
            ],
            as_index=False
        )["Sales_per_Active_User_USD"]
        .mean()
    )


    fig1 = px.line(
        sales_user_trend,
        x="Year",
        y="Sales_per_Active_User_USD",
        color="Company",
        markers=True,
        title="Sales per Active User Trend by Year",
        labels={
            "Sales_per_Active_User_USD":
                "Average Sales per Active User (USD)"
        },
    )


    fig1.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Sales per Active User (USD)",
        legend_title="Company",
        margin=dict(
            l=70,
            r=30,
            t=70,
            b=60
        )
    )


    fig1.update_yaxes(
        tickprefix="$",
        tickformat=",.0f"
    )


    # ========================================================
    # Figure 2
    # Average annual sales trend
    # ========================================================

    trend = (
        dff
        .groupby(
            [
                "Year",
                "Company"
            ],
            as_index=False
        )["Total_Sales (USD Billion)"]
        .mean()
    )


    fig2 = px.line(
        trend,
        x="Year",
        y="Total_Sales (USD Billion)",
        color="Company",
        markers=True,
        title="Average Annual Sales Trend",
        labels={
            "Total_Sales (USD Billion)":
                "Average Sales (USD Billion)"
        },
    )


    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Sales (USD Billion)",
        legend_title="Company",
        margin=dict(
            l=60,
            r=30,
            t=70,
            b=60
        )
    )

    fig2.update_yaxes(
        tickprefix="$",
        tickformat=",.0f"
    )

    # ========================================================
    # Figure 3
    # Highest-sales region distribution
    # ========================================================

    region = (
        dff
        .groupby(
            "Region_with_Highest_Sales",
            as_index=False
        )
        .size()
    )


    fig3 = px.pie(
        region,
        names="Region_with_Highest_Sales",
        values="size",
        title="Highest-Sales Region Distribution",
    )


    fig3.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )


    fig3.update_layout(
        legend_title="Region",
        margin=dict(
            l=40,
            r=40,
            t=70,
            b=40
        )
    )

    # ========================================================
    # Figure 4
    # Sales distribution and potential outliers
    # ========================================================

    fig4 = px.box(
        dff,
        x="Company",
        y="Total_Sales (USD Billion)",
        color="Company",
        title="Sales Distribution and Potential Outliers",
        labels={
            "Total_Sales (USD Billion)":
                "Sales (USD Billion)"
        },
    )


    fig4.update_layout(
        showlegend=False,
        xaxis_title="Company",
        yaxis_title="Sales (USD Billion)",
        margin=dict(
            l=60,
            r=30,
            t=70,
            b=60
        )
    )

    fig4.update_yaxes(
        tickprefix="$",
        tickformat=",.0f"
    )
    # ========================================================
    # Figure 5
    # Deviation from overall average
    # ========================================================

    company_profile = (
        dff
        .groupby(
            "Company",
            as_index=False
        )
        .agg({
            "Market_Share (%)": "mean",
            "Operating_Income (%)": "mean",
            "Mobile_Transactions (%)": "mean"
        })
    )


    profile_long = company_profile.melt(
        id_vars="Company",
        var_name="Metric",
        value_name="Average Value"
    )


    metric_labels = {
        "Market_Share (%)":
            "Market Share",

        "Operating_Income (%)":
            "Operating Income",

        "Mobile_Transactions (%)":
            "Mobile Transactions"
    }


    profile_long["Metric"] = (
        profile_long["Metric"]
        .map(metric_labels)
    )


    # --------------------------------------------------------
    # Calculate mean across selected companies
    # for each performance metric
    # --------------------------------------------------------

    metric_means = (
        profile_long
        .groupby("Metric")["Average Value"]
        .transform("mean")
    )


    profile_long["Difference"] = (
        profile_long["Average Value"]
        - metric_means
    )


    fig5 = px.bar(
        profile_long,
        x="Difference",
        y="Metric",
        color="Company",
        barmode="group",
        orientation="h",
        title="Company Performance Relative to Overall Average",
        labels={
            "Difference":
                "Difference from Overall Average (percentage points)",
            "Metric":
                ""
        },
        text="Difference",
        hover_data={
            "Average Value": ":.2f",
            "Difference": ":.2f"
        }
    )


    fig5.update_traces(
        texttemplate="%{text:+.2f}",
        textposition="outside"
    )


    # Vertical reference line at overall average

    fig5.add_vline(
        x=0,
        line_width=1,
        line_dash="dash"
    )


    fig5.update_layout(
        xaxis_title=(
            "Difference from Overall Average "
            "(percentage points)"
        ),
        yaxis_title="",
        legend_title="Company",
        margin=dict(
            l=130,
            r=70,
            t=70,
            b=70
        )
    )


    # ========================================================
    # Return KPIs + figures
    # ========================================================

    return (
        f"{len(dff):,}",

        f'{dff["Total_Sales (USD Billion)"].mean():,.1f}',

        f'{dff["Active_Users (Million)"].mean():,.1f}',

        f'{dff["Market_Share (%)"].mean():.1f}%',

        f'{dff["Operating_Income (%)"].mean():.1f}%',

        fig1,
        fig2,
        fig3,
        fig4,
        fig5,
    )


server = app.server

if __name__ == "__main__":
    app.run(debug=True, port=8051)