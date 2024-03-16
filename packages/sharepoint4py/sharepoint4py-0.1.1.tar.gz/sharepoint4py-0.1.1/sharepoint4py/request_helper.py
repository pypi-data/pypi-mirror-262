import requests
from .errors import sharepoint4pyRequestError


def get(session: requests.Session, url, **kwargs):
    try:
        response = session.get(url, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as err:
        raise sharepoint4pyRequestError("sharepoint4py HTTP Get Failed", err)


def post(session: requests.Session, url, **kwargs):
    try:
        response = session.post(url, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as err:
        raise sharepoint4pyRequestError("sharepoint4py HTTP Post Failed", err)



def delete(session: requests.Session, url, **kwargs):
    try:
        response = session.delete(url, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as err:
        raise sharepoint4pyRequestError("sharepoint4py HTTP Post Failed", err)
