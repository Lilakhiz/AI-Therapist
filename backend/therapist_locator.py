import requests
import urllib.parse

from backend.config import GOOGLE_MAPS_API_KEY


def find_therapists(city: str):

    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask":
            ",".join([
                "places.displayName",
                "places.formattedAddress",
                "places.rating",
                "places.websiteUri",
                "places.nationalPhoneNumber",
                "places.regularOpeningHours",
                "places.googleMapsUri"
            ])
    }

    body = {
        "textQuery": f"licensed psychologist in {city}"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    response.raise_for_status()

    data = response.json()

    therapists = []

    for place in data.get("places", [])[:5]:

        therapists.append({

            "name":
                place["displayName"]["text"],

            "rating":
                place.get("rating", "N/A"),

            "address":
                place.get("formattedAddress", "Unavailable"),

            "phone":
                place.get("nationalPhoneNumber", "Unavailable"),

            "website":
                place.get("websiteUri", None),

            "maps":
                place.get(
                    "googleMapsUri",
                    f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(place.get('formattedAddress',''))}"
                ),

            "hours":
                place.get(
                    "regularOpeningHours",
                    {}
                ).get(
                    "openNow",
                    None
                )

        })

    return therapists