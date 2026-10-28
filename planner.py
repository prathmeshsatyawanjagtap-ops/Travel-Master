import json
from pathlib import Path


DATA_FILE = Path(__file__).parent / "destinations.json"


def load_destinations():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def recommend_destinations(
    budget,
    travelers,
    days,
    interest
):
    destinations = load_destinations()
    recommendations = []

    for destination in destinations:

        daily_cost = destination["daily_cost_per_person"]

        estimated_cost = daily_cost * travelers * days

        categories = destination["categories"]

        interest_match = (
            interest.lower() in categories
        )

        if (
            estimated_cost <= budget
            and destination["minimum_days"] <= days
        ):
            recommendations.append({
                "name": destination["name"],
                "state": destination["state"],
                "estimated_cost": estimated_cost,
                "interest_match": interest_match,
                "description": destination["description"]
            })

    recommendations.sort(
        key=lambda item: (
            not item["interest_match"],
            item["estimated_cost"]
        )
    )

    return recommendations


def generate_itinerary(destination, days):
    itinerary = []

    for day in range(1, days + 1):

        itinerary.append({
            "day": day,
            "morning": (
                f"Explore {destination} and its "
                "nearby attractions."
            ),
            "afternoon": (
                "Enjoy local food and visit a "
                "suitable sightseeing location."
            ),
            "evening": (
                "Enjoy local experiences and "
                "return to your accommodation."
            )
        })

    return itinerary