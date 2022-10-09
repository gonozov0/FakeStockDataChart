import dash
import plotly
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output

from repository import SessionLocal, get_ticker_with_values, get_tickers, schemas

app = dash.Dash(__name__)


def setup_app(tickers: list[schemas.Ticker], default_ticker: schemas.Ticker):
    app.layout = html.Div(
        [
            html.Div(
                [
                    dcc.Dropdown(
                        options=[
                            {"label": ticker.name, "value": ticker.id}
                            for ticker in tickers
                        ],
                        value=default_ticker.id,
                        id="ticker-names-dropdown",
                    )
                ]
            ),
            html.Div(
                [
                    dcc.Graph(id="live-chart", animate=True),
                    dcc.Interval(
                        id="chart-update",
                        interval=1000,
                    ),
                ]
            ),
        ]
    )


@app.callback(
    Output("live-chart", "figure"),
    [
        Input("ticker-names-dropdown", "value"),
        Input("chart-update", "n_intervals"),
    ],
)
def update_graph_scatter(ticker_id, *_):
    if not ticker_id:
        global default_ticker
        ticker_id = default_ticker.id
    global session

    ticker = get_ticker_with_values(session=session, ticker_id=ticker_id)
    y = ticker.values
    x = [i for i in range(len(y))]

    data = plotly.graph_objs.Scatter(x=x, y=y, name="Scatter", mode="lines+markers")
    return {
        "data": [data],
        "layout": go.Layout(
            xaxis=dict(range=[min(x) - 1, max(x) + 1]),
            yaxis=dict(range=[min(y) - 1, max(y) + 1]),
        ),
    }


if __name__ == "__main__":
    session = SessionLocal()
    try:
        tickers = get_tickers(session=session)
        default_ticker = tickers[0]
        setup_app(tickers=tickers, default_ticker=default_ticker)
        app.run_server(host="0.0.0.0")
    finally:
        session.close()
