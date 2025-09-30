# app.py — Advanced Retail Dashboard (Dash v3 + Plotly, polished)
# Run:
#   pip install dash pandas numpy plotly
#   (optional for trendline) pip install statsmodels
#   python app.py
# Open: http://127.0.0.1:8050

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# ========= CONFIG =========
DATA_PATH = "cleaned_retail.csv"   # change if needed
DEFAULT_TEMPLATE = "plotly_white"
COLOR_ACCENT = "#6C5CE7"
TOP_N_DEFAULT = 10
COLOR_SEQ = px.colors.qualitative.Vivid
# ==========================

# ---- make trendline optional (no crash if statsmodels missing)
try:
    import statsmodels.api as sm  # noqa: F401
    HAS_STATSMODELS = True
except Exception:
    HAS_STATSMODELS = False

# ---------- Data Load ----------
def load_data(path: str) -> pd.DataFrame:
    f = Path(path)
    if not f.exists():
        raise FileNotFoundError(f"File not found: {f.resolve()}")
    if f.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(f)
    elif f.suffix.lower() == ".csv":
        try:
            df = pd.read_csv(f, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(f, encoding="latin1")
    else:
        raise ValueError("Use .xlsx or .csv")
    return df

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().replace(" ", "").replace("-", "").replace("/", "") for c in df.columns]
    alias = {
        "CustomerID": ["Customer Id", "Customer_ID", "Customer Id "],
        "InvoiceDate": ["Invoice Date", "Date"],
        "UnitPrice": ["Unit Price", "Price"],
        "InvoiceNo": ["Invoice No", "Invoice", "Invoice_Number"],
    }
    for tgt, alts in alias.items():
        if tgt not in df.columns:
            for a in alts:
                if a in df.columns:
                    df.rename(columns={a: tgt}, inplace=True)
                    break

    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    df = df.drop_duplicates()

    mask = pd.Series(True, index=df.index)
    if "Quantity" in df.columns:
        mask &= df["Quantity"] > 0
    if "UnitPrice" in df.columns:
        mask &= df["UnitPrice"] > 0
    df = df.loc[mask].copy()

    if {"Quantity", "UnitPrice"}.issubset(df.columns):
        df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    if "InvoiceDate" in df.columns:
        df["InvoiceYear"]  = df["InvoiceDate"].dt.year
        df["InvoiceMonth"] = df["InvoiceDate"].dt.month
        df["InvoiceHour"]  = df["InvoiceDate"].dt.hour
        df["Weekday"]      = df["InvoiceDate"].dt.day_name()
        df["DateOnly"]     = df["InvoiceDate"].dt.date
    return df

df_raw = load_data(DATA_PATH)
df = clean(df_raw)

HAS = {
    "country":   "Country"    in df.columns,
    "desc":      "Description" in df.columns,
    "total":     "TotalPrice"  in df.columns,
    "date":      "InvoiceDate" in df.columns,
}

min_date = df["InvoiceDate"].min() if HAS["date"] else None
max_date = df["InvoiceDate"].max() if HAS["date"] else None

# ---------- App ----------
app = Dash(__name__)
app.title = "Retail Sales Dashboard"

# ---- UI helpers
def card(children, **style):
    base = {
        "background": "#fff",
        "borderRadius": "16px",
        "padding": "16px",
        "boxShadow": "0 8px 20px rgba(17, 17, 26, 0.05)",
    }
    base.update(style or {})
    return html.Div(children, style=base)

def style_fig(fig, title=None):
    fig.update_layout(
        template=DEFAULT_TEMPLATE,
        title=title if title else fig.layout.title.text,
        title_font=dict(size=18, color="#2C3E50"),
        font=dict(family="Inter, Segoe UI, Roboto, Arial", size=12, color="#2C3E50"),
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor="#eee"),
        yaxis=dict(showgrid=True, gridcolor="#eee"),
        colorway=COLOR_SEQ,
    )
    return fig

HSTACK = {"display": "flex", "gap": "12px", "alignItems": "center", "flexWrap": "wrap"}
GRID_3 = {"display": "grid", "gridTemplateColumns": "repeat(3, minmax(220px, 1fr))", "gap": "16px"}

header = html.Div([
    html.Div("Retail Sales Dashboard", style={"fontSize": 28, "fontWeight": 800}),
    html.Div("Interactive insights from the Online Retail dataset",
             style={"color": "#666", "marginTop": 4})
], style={"display": "flex", "flexDirection": "column"})

# ---------- Layout ----------
app.layout = html.Div(style={
    "fontFamily": "Inter, system-ui, Segoe UI, Roboto, Arial",
    "background": "#F6F7FB",
    "minHeight": "100vh",
    "padding": "20px"
}, children=[
    html.Div([header], style={"marginBottom": "14px"}),

    html.Div(style={"display": "grid",
                    "gridTemplateColumns": "320px 1fr",
                    "gap": "16px"}, children=[

        # Sidebar
        card([
            html.Div("Filters", style={"fontWeight": 700, "marginBottom": 8, "fontSize": 16}),
            html.Label("Country", style={"fontWeight": 600}),
            dcc.Dropdown(
                id="country",
                options=([{"label": c, "value": c} for c in sorted(df["Country"].dropna().unique())] if HAS["country"] else []),
                value=[], multi=True, placeholder="All countries",
                style={"marginBottom": 12}
            ),
            html.Label("Date Range", style={"fontWeight": 600}),
            dcc.DatePickerRange(
                id="dates",
                min_date_allowed=min_date.date() if min_date is not None else None,
                max_date_allowed=max_date.date() if max_date is not None else None,
                start_date=min_date.date() if min_date is not None else None,
                end_date=max_date.date() if max_date is not None else None,
                display_format="DD/MM/YYYY"
            ),
            html.Hr(style={"margin": "12px 0"}),
            html.Label("Top-N products", style={"fontWeight": 600}),
            dcc.Slider(id="topn", min=5, max=25, step=1, value=TOP_N_DEFAULT,
                       tooltip={"placement": "bottom", "always_visible": True},
                       marks={5:"5",10:"10",15:"15",20:"20",25:"25"}),
            html.Label("Search product (contains)", style={"fontWeight": 600, "marginTop": 12}),
            dcc.Input(id="search", type="text", placeholder="e.g., MUG / POSTAGE", style={"width": "100%"}),
        ], style={"alignSelf": "start"}),

        # Content
        html.Div(children=[
            html.Div(id="kpis", style=GRID_3),
            card([
                dcc.Tabs(id="tabs", value="tab-overview", children=[
                    dcc.Tab(label="Overview", value="tab-overview",
                            selected_style={"background": "#F1F2FE", "color": "#111", "fontWeight": 700}),
                    dcc.Tab(label="Products", value="tab-products",
                            selected_style={"background": "#F1F2FE", "color": "#111", "fontWeight": 700}),
                    dcc.Tab(label="Customers & Time", value="tab-time",
                            selected_style={"background": "#F1F2FE", "color": "#111", "fontWeight": 700}),
                ])
            ], style={"padding": 0}),
            html.Div(id="tab-content", style={"marginTop": 16, "display": "grid", "gap": "16px"})
        ])
    ]),

    html.Div("Built with Dash + Plotly • Internship Task 2",
             style={"textAlign": "center", "marginTop": 18, "color": "#888"})
])

# ---------- Helpers ----------
def apply_filters(_df, countries, start_date, end_date, search_text):
    out = _df.copy()
    if HAS["country"] and countries:
        out = out[out["Country"].isin(countries)]
    if HAS["date"] and start_date and end_date:
        sd = pd.to_datetime(start_date)
        ed = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        out = out[(out["InvoiceDate"] >= sd) & (out["InvoiceDate"] <= ed)]
    if HAS["desc"] and search_text:
        st = str(search_text).strip().lower()
        if st:
            out = out[out["Description"].str.lower().str.contains(st, na=False)]
    return out

def kpi_card(title, value, sub=None, color=COLOR_ACCENT):
    return card([
        html.Div(title, style={"fontSize": 13, "color": "#666"}),
        html.Div(value, style={"fontSize": 26, "fontWeight": 800, "color": color}),
        html.Div(sub or "", style={"fontSize": 12, "color": "#999", "marginTop": 4})
    ])

# ---------- Callbacks ----------
@app.callback(
    Output("kpis", "children"),
    Output("tab-content", "children"),
    Input("country", "value"),
    Input("dates", "start_date"),
    Input("dates", "end_date"),
    Input("topn", "value"),
    Input("search", "value"),
    Input("tabs", "value"),
)
def update(countries, start_date, end_date, topn, search_text, tab):
    dff = apply_filters(df, countries, start_date, end_date, search_text)

    total_rev = dff["TotalPrice"].sum() if HAS["total"] else np.nan
    orders = (dff.groupby("InvoiceNo")["TotalPrice"].sum()
              if {"InvoiceNo","TotalPrice"}.issubset(dff.columns) else pd.Series(dtype=float))
    aov = orders.mean() if len(orders) else np.nan
    top_prod = (dff.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(1)
                if HAS["desc"] and HAS["total"] else None)
    top_prod_text = top_prod.index[0] if top_prod is not None and len(top_prod) else "—"

    kpis = [
        kpi_card("Total Revenue", f"£{total_rev:,.0f}" if pd.notna(total_rev) else "—"),
        kpi_card("Average Order Value", f"£{aov:,.0f}" if pd.notna(aov) else "—"),
        kpi_card("Top Product (by revenue)", top_prod_text, sub="Filtered range"),
    ]

    charts = []

    if tab == "tab-overview":
        if HAS["date"] and HAS["total"]:
            daily = dff.set_index("InvoiceDate")["TotalPrice"].resample("D").sum()
            fig = px.line(daily, markers=True, labels={"value": "Revenue", "InvoiceDate": "Date"})
            charts.append(card(dcc.Graph(figure=style_fig(fig, "Daily Revenue"))))
        if HAS["country"] and HAS["total"]:
            ctry = dff.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(15)
            fig = px.bar(ctry, labels={"value": "Revenue", "index": "Country"})
            charts.append(card(dcc.Graph(figure=style_fig(fig, "Top Countries by Revenue"))))

    elif tab == "tab-products":
        if HAS["desc"] and HAS["total"]:
            prod = (dff.groupby("Description")["TotalPrice"]
                    .sum().sort_values(ascending=False).head(int(topn)).sort_values())
            fig = px.bar(prod, orientation="h", labels={"value": "Revenue", "index": "Product"})
            charts.append(card(dcc.Graph(figure=style_fig(fig, f"Top {topn} Products by Revenue"))))

        if HAS["desc"] and {"Quantity","TotalPrice"}.issubset(dff.columns):
            agg = (dff.groupby("Description")
                   .agg(Quantity=("Quantity","sum"), Revenue=("TotalPrice","sum"))
                   .sort_values("Revenue", ascending=False).head(int(topn)*2))
            fig = px.scatter(
                agg, x="Quantity", y="Revenue", hover_name=agg.index,
                trendline=("ols" if HAS_STATSMODELS else None)
            )
            charts.append(card(dcc.Graph(figure=style_fig(fig, "Quantity vs Revenue (Top candidates)"))))

    elif tab == "tab-time":
        if HAS["date"] and HAS["total"]:
            hr = dff.groupby(dff["InvoiceDate"].dt.hour)["TotalPrice"].sum().reindex(range(24), fill_value=0)
            fig = px.line(x=hr.index, y=hr.values, markers=True,
                          labels={"x": "Hour of Day", "y": "Revenue"})
            charts.append(card(dcc.Graph(figure=style_fig(fig, "Revenue by Hour of Day"))))
        if HAS["date"] and HAS["total"]:
            dff["_weekday"] = dff["InvoiceDate"].dt.day_name()
            dff["_hour"] = dff["InvoiceDate"].dt.hour
            pivot = dff.pivot_table(index="_weekday", columns="_hour",
                                    values="TotalPrice", aggfunc="sum").fillna(0)
            order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            pivot = pivot.reindex(order)
            fig = px.imshow(pivot, aspect="auto", color_continuous_scale="Blues",
                            labels=dict(x="Hour", y="Weekday", color="Revenue"))
            fig = style_fig(fig, "Revenue Heatmap (Weekday × Hour)")
            charts.append(card(dcc.Graph(figure=fig)))

    return kpis, charts

if __name__ == "__main__":
    print("Loaded rows:", len(df))
    if min_date is not None and max_date is not None:
        print("Date range:", min_date, "->", max_date)
    app.run(debug=True)
