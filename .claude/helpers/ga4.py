"""Helper GA4 (Google Analytics 4 Data API) per a sessions clawdocs.

Usa el Service Account ja configurat a GOOGLE_APPLICATION_CREDENTIALS
(via el hook session-start.sh). El SA ha d'estar afegit com a Viewer a
cada propietat GA4 que es vulgui consultar.

Ús bàsic:

    from ga4 import pull_purchases
    rows = pull_purchases("123456789", "2026-05-15", "2026-05-22")
    for r in rows:
        print(r)
"""
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, FilterExpression, Filter,
)


def get_client():
    return BetaAnalyticsDataClient()


def pull_purchases(property_id, start_date, end_date, source=None):
    """Compres GA4 (event=purchase) per data i source/medium.

    source: opcional, filtra per 'sessionSource' (p.ex. 'google').
    """
    client = get_client()
    dims = [
        Dimension(name="date"),
        Dimension(name="sessionSource"),
        Dimension(name="sessionMedium"),
        Dimension(name="sessionDefaultChannelGrouping"),
    ]
    metrics = [
        Metric(name="eventCount"),
        Metric(name="purchaseRevenue"),
        Metric(name="transactions"),
    ]
    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=dims,
        metrics=metrics,
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter=Filter.StringFilter(value="purchase"),
            )
        ),
    )
    resp = client.run_report(req)
    results = []
    for row in resp.rows:
        d = {dh.name: dv.value for dh, dv in zip(resp.dimension_headers, row.dimension_values)}
        m = {mh.name: mv.value for mh, mv in zip(resp.metric_headers, row.metric_values)}
        if source and d.get("sessionSource", "").lower() != source.lower():
            continue
        results.append({
            "date": d.get("date"),
            "source": d.get("sessionSource"),
            "medium": d.get("sessionMedium"),
            "channel": d.get("sessionDefaultChannelGrouping"),
            "purchases": int(m.get("eventCount", 0)),
            "transactions": int(m.get("transactions", 0)),
            "revenue": float(m.get("purchaseRevenue", 0)),
        })
    return results


def pull_purchases_by_ad_campaign(property_id, start_date, end_date):
    """Compres GA4 agrupades per googleAdsCampaignName.

    Útil per creuar amb el Dashboard de Google Ads i validar tracking.
    """
    client = get_client()
    dims = [Dimension(name="googleAdsCampaignName")]
    metrics = [
        Metric(name="transactions"),
        Metric(name="purchaseRevenue"),
    ]
    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=dims,
        metrics=metrics,
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    resp = client.run_report(req)
    results = []
    for row in resp.rows:
        d = {dh.name: dv.value for dh, dv in zip(resp.dimension_headers, row.dimension_values)}
        m = {mh.name: mv.value for mh, mv in zip(resp.metric_headers, row.metric_values)}
        results.append({
            "campaign": d.get("googleAdsCampaignName"),
            "transactions": int(m.get("transactions", 0)),
            "revenue": float(m.get("purchaseRevenue", 0)),
        })
    return results


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Ús: python ga4.py <property_id> <start_date> <end_date> [by_campaign]")
        sys.exit(1)
    pid, start, end = sys.argv[1], sys.argv[2], sys.argv[3]
    if len(sys.argv) > 4 and sys.argv[4] == "by_campaign":
        rows = pull_purchases_by_ad_campaign(pid, start, end)
    else:
        rows = pull_purchases(pid, start, end)
    for r in rows:
        print(r)
