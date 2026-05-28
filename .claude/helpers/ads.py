"""Helper Google Ads per a sessions clawdocs.

Llegeix credencials de variables d'entorn (configurades al Cloud env):
- GOOGLE_ADS_DEVELOPER_TOKEN
- GOOGLE_ADS_CLIENT_ID
- GOOGLE_ADS_CLIENT_SECRET
- GOOGLE_ADS_REFRESH_TOKEN
- GOOGLE_ADS_LOGIN_CUSTOMER_ID (MCC sense guions)

Ús bàsic:

    from ads import get_client, pull_campaigns
    client = get_client()
    rows = pull_campaigns(client, "3823744676", "2026-05-15", "2026-05-22")
    for r in rows:
        print(r)
"""
import os
import re

os.environ.setdefault(
    "GRPC_DEFAULT_SSL_ROOTS_FILE_PATH", "/etc/ssl/certs/ca-certificates.crt"
)

from google.ads.googleads.client import GoogleAdsClient


def _clean(name):
    return os.environ[name].strip().strip("<>").strip()


def _config():
    required = [
        "GOOGLE_ADS_DEVELOPER_TOKEN",
        "GOOGLE_ADS_CLIENT_ID",
        "GOOGLE_ADS_CLIENT_SECRET",
        "GOOGLE_ADS_REFRESH_TOKEN",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID",
    ]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise RuntimeError(f"Falten env vars: {missing}")
    return {
        "developer_token": _clean("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "client_id": _clean("GOOGLE_ADS_CLIENT_ID"),
        "client_secret": _clean("GOOGLE_ADS_CLIENT_SECRET"),
        "refresh_token": _clean("GOOGLE_ADS_REFRESH_TOKEN"),
        "login_customer_id": re.sub(r"\D", "", _clean("GOOGLE_ADS_LOGIN_CUSTOMER_ID")),
        "use_proto_plus": True,
    }


def get_client():
    return GoogleAdsClient.load_from_dict(_config())


def _norm_cid(customer_id):
    return str(customer_id).replace("-", "").strip()


def pull_campaigns(client, customer_id, start_date, end_date):
    """Retorna llista de dicts amb performance per campanya en el rang donat."""
    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          campaign.advertising_channel_type,
          metrics.cost_micros,
          metrics.conversions,
          metrics.conversions_value,
          metrics.impressions,
          metrics.clicks
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY metrics.cost_micros DESC
    """
    results = []
    stream = ga_service.search_stream(customer_id=_norm_cid(customer_id), query=query)
    for batch in stream:
        for row in batch.results:
            cost = row.metrics.cost_micros / 1_000_000
            value = row.metrics.conversions_value
            results.append({
                "campaign_id": row.campaign.id,
                "name": row.campaign.name,
                "status": row.campaign.status.name,
                "type": row.campaign.advertising_channel_type.name,
                "cost_eur": round(cost, 2),
                "value_eur": round(value, 2),
                "conversions": round(row.metrics.conversions, 2),
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "roas": round(value / cost, 2) if cost > 0 else 0,
            })
    return results


def pull_conversion_actions(client, customer_id):
    """Retorna llista de conversion actions configurades al compte."""
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
          conversion_action.id,
          conversion_action.name,
          conversion_action.category,
          conversion_action.status,
          conversion_action.primary_for_goal,
          conversion_action.include_in_conversions_metric,
          conversion_action.type
        FROM conversion_action
    """
    results = []
    stream = ga_service.search_stream(customer_id=_norm_cid(customer_id), query=query)
    for batch in stream:
        for row in batch.results:
            ca = row.conversion_action
            results.append({
                "id": ca.id,
                "name": ca.name,
                "category": ca.category.name,
                "status": ca.status.name,
                "primary_for_goal": ca.primary_for_goal,
                "included_in_conversions": ca.include_in_conversions_metric,
                "type": ca.type_.name,
            })
    return results


def list_accessible_customers(client):
    """Retorna llista de Customer IDs accessibles per l'MCC."""
    svc = client.get_service("CustomerService")
    accessible = svc.list_accessible_customers()
    return [name.split("/")[-1] for name in accessible.resource_names]


if __name__ == "__main__":
    import sys
    c = get_client()
    if len(sys.argv) == 1:
        print("Comptes accessibles via MCC:")
        for cid in list_accessible_customers(c):
            print(f"  {cid}")
    elif len(sys.argv) == 4:
        _, cid, start, end = sys.argv
        rows = pull_campaigns(c, cid, start, end)
        for r in rows:
            print(r)
    else:
        print("Ús: python ads.py [<customer_id> <start_date> <end_date>]")
