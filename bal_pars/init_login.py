#!/usr/bin/env python3
import argparse
import sys
import requests
from bs4 import BeautifulSoup

from bal_pars.config import BASE_URL, USERNAME, PASSWORD, HEADERS, LOGIN_URL
from bal_pars.parse_prod import parse_product


def try_login():
    global session
    session = requests.Session()
    try:
        session = login(session)
        # Visit the catalog page to ensure the ASP.NET session state is fully initialized
        session.get("https://b2b.balkanicadistral.com/Catalogo.aspx", headers=HEADERS, timeout=20)
    except Exception as e:
        print(f"Login failed: {e}", file=sys.stderr)
        sys.exit(1)

def login(session):
    response = session.get(LOGIN_URL, headers=HEADERS, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    viewstate = soup.find("input", {"name": "__VIEWSTATE"})
    eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"})
    compressedviewstate = soup.find("input", {"name": "__COMPRESSEDVIEWSTATE"})

    login_data = {
        "__COMPRESSEDVIEWSTATE": compressedviewstate["value"] if compressedviewstate else "",
        "__VIEWSTATE": viewstate["value"] if viewstate else "",
        "__EVENTVALIDATION": eventvalidation["value"] if eventvalidation else "",
        "foo": "",
        "txUsuario": USERNAME,
        "txPass": PASSWORD,
        "btnEntrar": "Вход",
    }

    post_headers = HEADERS.copy()
    post_headers["Content-Type"] = "application/x-www-form-urlencoded"
    post_headers["Referer"] = LOGIN_URL
    post_headers["Origin"] = "https://b2b.balkanicadistral.com"

    response = session.post(LOGIN_URL, headers=post_headers, data=login_data,
                            timeout=20, allow_redirects=True)
    response.raise_for_status()

    if "Login.aspx" in response.url and "txUsuario" in response.text:
        raise requests.exceptions.RequestException("Login failed: Credentials might be incorrect.")

    return session


def fetch_page(product_code):
    params = {"Codigo": product_code, "IdOportunidad": "0"}
    # Many ASP.NET sites require a Referer to validate the request flow.
    request_headers = HEADERS.copy()
    request_headers["Referer"] = "https://b2b.balkanicadistral.com/Catalogo.aspx"
    
    response = session.get(BASE_URL, headers=request_headers, params=params, timeout=20)
    response.raise_for_status()

    # Detect ASP.NET server-side crashes that return 200 OK but show an error message
    if "Object reference not set to an instance of an object" in response.text:
        print(f"[!] Server error for product {product_code}. Skipping.", file=sys.stderr)
        return None

    return response.text


def start_pars(code):
    try:
        html = fetch_page(code)
        
        # Only parse if the HTML is valid and didn't hit the server error
        if html:
            parse_product(html, code)
        else:
            print(f"Skipping product {code} due to server error.", file=sys.stderr)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product page: {e}", file=sys.stderr)
