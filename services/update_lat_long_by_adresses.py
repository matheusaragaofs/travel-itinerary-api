import asyncio
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


async def get_lat_long_by_address(address, retries=3, delay=2):
    loc = Nominatim(user_agent="Geopy Library", timeout=10)

    def geocode_address(address):
        for _ in range(retries):
            try:
                return loc.geocode(address)
            except GeocoderTimedOut:
                time.sleep(delay)
        return None

    getLoc = await asyncio.to_thread(geocode_address, address)

    if getLoc:
        print(f"Geocoded address: {getLoc.address}")
        return [getLoc.latitude, getLoc.longitude]
    else:
        print(f"Could not geocode address: {address}")
        return None


async def update_itinerary_lat_long(itinerary):
    for _, details in itinerary.items():
        for _, activity_details in details.items():
            if isinstance(activity_details, dict) and "address" in activity_details:
                address = activity_details["address"]
                new_lat_long = await get_lat_long_by_address(address)
                if new_lat_long:
                    activity_details["latitude"], activity_details["longitude"] = map(
                        str, new_lat_long
                    )
                else:
                    activity_details["latitude"], activity_details["longitude"] = (
                        None,
                        None,
                    )
    return itinerary


async def update_activities_restaurants_and_accomodations_lat_long(activities):
    for activity in activities:
        if "address" in activity:
            address = activity["address"]
            new_lat_long = await get_lat_long_by_address(address)
            if new_lat_long:
                activity["latitude"], activity["longitude"] = map(str, new_lat_long)
            else:
                activity["latitude"], activity["longitude"] = None, None
    return activities


async def update_lat_long_for_all(mocked_response):
    itinerary = mocked_response.get("itinerary", {})
    recommended_accommodations = mocked_response.get("recommended_accommodations", [])
    recommended_restaurants = mocked_response.get("recommended_restaurants", [])
    extra_activities = mocked_response.get(
        "extra_activities_based_on_preferred_travel_styles", []
    )

    updated_itinerary = await update_itinerary_lat_long(itinerary)
    updated_accommodations = (
        await update_activities_restaurants_and_accomodations_lat_long(
            recommended_accommodations
        )
    )
    updated_restaurants = (
        await update_activities_restaurants_and_accomodations_lat_long(
            recommended_restaurants
        )
    )
    updated_extra_activities = (
        await update_activities_restaurants_and_accomodations_lat_long(extra_activities)
    )

    return {
        "itinerary": updated_itinerary,
        "recommended_accommodations": updated_accommodations,
        "recommended_restaurants": updated_restaurants,
        "extra_activities_based_on_preferred_travel_styles": updated_extra_activities,
    }


def update_lat_long_by_addresses(itineraray):
    return asyncio.run(update_lat_long_for_all(itineraray))
