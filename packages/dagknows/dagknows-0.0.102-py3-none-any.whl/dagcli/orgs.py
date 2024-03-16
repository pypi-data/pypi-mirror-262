import subprocess
from base64 import b64decode
import typer
from typing_extensions import Annotated
from typing import Optional
from pathlib import Path
import os, sys
from typing import List
import requests

from pkg_resources import resource_string
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

app = typer.Typer()

@app.command()
def find(ctx: typer.Context):
    sesscli = ctx.obj.client
    from dagcli.client import make_url
    dagknows_url = sesscli.host
    url = make_url(sesscli.host, "/getUnusedOrgs")
    resp = requests.post(url, headers=ctx.obj.headers, verify=False)
    if resp.status_code == 200:
        print("Output: ", resp.json())
    else:
        print("Failed: ", resp.content)

@app.command()
def delete(ctx: typer.Context,
           orgname: str = typer.Argument(..., help="Name of the org to delete")):
    sesscli = ctx.obj.client
    from dagcli.client import make_url
    dagknows_url = sesscli.host
    url = make_url(sesscli.host, "/deleteOrg")
    payload = { "orgname": orgname.strip().lower() }
    resp = requests.post(url, json=payload, headers=ctx.obj.headers, verify=False)
    if resp.status_code == 200:
        for k,v in resp.json().get("_source", {}).get("proxy_table", {}).items():
            print(k, v)
            print("")
    else:
        print("Failed: ", resp.content)

@app.command()
def ensure(ctx: typer.Context,
           orgname: str = typer.Argument(..., help="Name of the org to ensure")):
    sesscli = ctx.obj.client
    from dagcli.client import make_url
    dagknows_url = sesscli.host
    url = make_url(sesscli.host, "/ensureOrg")
    payload = { "orgname": orgname.strip().lower() }
    resp = requests.post(url, json=payload, headers=ctx.obj.headers, verify=False)
    if resp.status_code == 200:
        for k,v in resp.json().get("_source", {}).get("proxy_table", {}).items():
            print(k, v)
            print("")
    else:
        print("Failed: ", resp.content)
