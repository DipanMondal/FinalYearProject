import pandas as pd


def build_yearly_average_df(
    report,
    metric_key,
    output_column
):
    seasonal_signature = report.get(
        "seasonal_signature",
        {}
    )

    metric_data = seasonal_signature.get(
        metric_key,
        {}
    )

    if not metric_data:
        return pd.DataFrame(
            columns=[
                "year",
                output_column
            ]
        )

    records = []

    for year, monthly_values in metric_data.items():

        values = pd.to_numeric(
            pd.Series(monthly_values),
            errors="coerce"
        ).dropna()

        if values.empty:
            continue

        records.append(
            {
                "year": int(year),
                output_column: float(values.mean())
            }
        )

    return (
        pd.DataFrame(records)
        .sort_values("year")
        .reset_index(drop=True)
    )