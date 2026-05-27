"""Helper Merchant Center (Content API for Shopping v2.1) per a sessions clawdocs.

Usa el Service Account ja configurat a GOOGLE_APPLICATION_CREDENTIALS
(via el hook session-start.sh). El SA ha d'estar afegit com a usuari del MCA
Moviéndote (254198292) com a Admin per accedir a tots els subcomptes.

Ús bàsic:

    from merchant import get_service, list_subaccounts, pull_product_statuses

    svc = get_service()
    # Llistar subcomptes del MCA
    for sub in list_subaccounts(svc, "254198292"):
        print(sub["id"], sub["name"])

    # Estat de productes d'un subcompte (disapprovals, warnings...)
    issues = pull_product_statuses(svc, "159030506", only_with_issues=True)
    for p in issues[:10]:
        print(p["product_id"], p["title"], p["issues"])
"""
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_httplib2 import AuthorizedHttp
import httplib2
import os

SCOPES = ["https://www.googleapis.com/auth/content"]
DEFAULT_CA_BUNDLE = "/etc/ssl/certs/ca-certificates.crt"


def get_service():
    """Retorna un client de Content API v2.1 amb el SA carregat.

    Injecta el CA bundle del sistema al httplib2 perquè el proxy d'Anthropic
    no faci fallar el handshake SSL (signed amb CA del proxy).
    """
    sa_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not sa_path or not os.path.exists(sa_path):
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS no configurat o fitxer no existeix. "
            "Verifica el hook session-start.sh."
        )
    creds = service_account.Credentials.from_service_account_file(
        sa_path, scopes=SCOPES
    )
    ca_bundle = os.environ.get("REQUESTS_CA_BUNDLE", DEFAULT_CA_BUNDLE)
    http = httplib2.Http(ca_certs=ca_bundle if os.path.exists(ca_bundle) else None)
    authed_http = AuthorizedHttp(creds, http=http)
    return build("content", "v2.1", http=authed_http, cache_discovery=False)


def list_subaccounts(service, mca_id):
    """Llista els subcomptes d'un MCA Merchant Center.

    Només funciona si el compte és Advanced/MCA i el SA hi té accés.
    Retorna: [{id, name, website_url, adult_content}, ...]
    """
    results = []
    req = service.accounts().list(merchantId=mca_id)
    while req is not None:
        resp = req.execute()
        for acc in resp.get("resources", []):
            results.append({
                "id": acc.get("id"),
                "name": acc.get("name"),
                "website_url": acc.get("websiteUrl"),
                "adult_content": acc.get("adultContent", False),
                "seller_id": acc.get("sellerId"),
            })
        req = service.accounts().list_next(req, resp)
    return results


def pull_account_status(service, merchant_id):
    """Retorna l'estat d'un compte (issues globals, account-level)."""
    resp = service.accountstatuses().get(
        merchantId=merchant_id, accountId=merchant_id
    ).execute()
    return {
        "account_id": resp.get("accountId"),
        "website_claimed": resp.get("websiteClaimed"),
        "account_level_issues": resp.get("accountLevelIssues", []),
        "products": resp.get("products", []),
    }


def pull_product_statuses(service, merchant_id, only_with_issues=False, max_results=250):
    """Llista l'estat dels productes d'un compte.

    only_with_issues: si True, només retorna els que tenen issues.
    max_results: límit per evitar pulls massius. Posa None per tots.
    """
    results = []
    req = service.productstatuses().list(merchantId=merchant_id, maxResults=250)
    while req is not None:
        resp = req.execute()
        for p in resp.get("resources", []):
            issues = p.get("itemLevelIssues", [])
            if only_with_issues and not issues:
                continue
            results.append({
                "product_id": p.get("productId"),
                "title": p.get("title"),
                "link": p.get("link"),
                "destination_statuses": p.get("destinationStatuses", []),
                "issues": [
                    {
                        "code": i.get("code"),
                        "severity": i.get("severity"),
                        "destination": i.get("destination"),
                        "description": i.get("description"),
                        "detail": i.get("detail"),
                        "resolution": i.get("resolution"),
                        "num_items": i.get("numItems", 0),
                    }
                    for i in issues
                ],
            })
            if max_results and len(results) >= max_results:
                return results
        req = service.productstatuses().list_next(req, resp)
    return results


def pull_disapproved_products(service, merchant_id):
    """Atall: només els productes desaprovats (issues amb severity='error')."""
    all_with_issues = pull_product_statuses(service, merchant_id, only_with_issues=True, max_results=None)
    disapproved = []
    for p in all_with_issues:
        errors = [i for i in p["issues"] if i["severity"] == "error"]
        if errors:
            disapproved.append({**p, "issues": errors})
    return disapproved


def pull_products(service, merchant_id, max_results=250):
    """Llista els productes (no només estat). Útil per veure feed real.

    Atenció: pot ser molt llarg per catàlegs grans; usa max_results.
    """
    results = []
    req = service.products().list(merchantId=merchant_id, maxResults=250)
    while req is not None:
        resp = req.execute()
        for p in resp.get("resources", []):
            results.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "brand": p.get("brand"),
                "price": p.get("price", {}),
                "availability": p.get("availability"),
                "condition": p.get("condition"),
                "link": p.get("link"),
                "image_link": p.get("imageLink"),
                "google_product_category": p.get("googleProductCategory"),
            })
            if max_results and len(results) >= max_results:
                return results
        req = service.products().list_next(req, resp)
    return results


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("Ús: python merchant.py <comanda> [args...]")
        print("Comandes:")
        print("  subaccounts <mca_id>")
        print("  status <merchant_id>")
        print("  issues <merchant_id>")
        print("  disapproved <merchant_id>")
        print("  products <merchant_id> [max=50]")
        sys.exit(1)

    svc = get_service()
    cmd = sys.argv[1]

    if cmd == "subaccounts":
        out = list_subaccounts(svc, sys.argv[2])
    elif cmd == "status":
        out = pull_account_status(svc, sys.argv[2])
    elif cmd == "issues":
        out = pull_product_statuses(svc, sys.argv[2], only_with_issues=True, max_results=50)
    elif cmd == "disapproved":
        out = pull_disapproved_products(svc, sys.argv[2])
    elif cmd == "products":
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        out = pull_products(svc, sys.argv[2], max_results=n)
    else:
        print(f"Comanda desconeguda: {cmd}")
        sys.exit(1)

    print(json.dumps(out, indent=2, ensure_ascii=False))
