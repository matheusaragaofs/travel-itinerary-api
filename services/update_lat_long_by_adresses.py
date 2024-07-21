import asyncio
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


itinerary = {
    "friday": {
        "afternoon": {
            "activity": "Praia de Porto de Galinhas (day trip continued)",
            "address": "Porto de Galinhas, Ipojuca - PE",
            "average_cost": "R$ 0",
            "latitude": "-8.502654",
            "longitude": "-35.005511",
            "time": "12:00 - 18:00",
        },
        "date_day": "2024-07-26",
        "morning": {
            "activity": "Praia de Porto de Galinhas (day trip)",
            "address": "Porto de Galinhas, Ipojuca - PE",
            "average_cost": "R$ 100 (transport)",
            "latitude": "-8.502654",
            "longitude": "-35.005511",
            "time": "08:00 - 12:00",
        },
        "night": {
            "activity": "Casa da Moeda",
            "address": "Rua da Moeda, 150, Recife Antigo, Recife - PE",
            "average_cost": "R$ 50",
            "latitude": "-8.061998",
            "longitude": "-34.870486",
            "time": "21:00 - 00:00",
        },
    },
    "monday": {
        "afternoon": {
            "activity": "Mercado de São José",
            "address": "Praça Dom Vital, s/n, São José, Recife - PE",
            "average_cost": "R$ 20",
            "latitude": "-8.069504",
            "longitude": "-34.877071",
            "time": "13:00 - 16:00",
        },
        "date_day": "2024-07-22",
        "morning": {
            "activity": "Instituto Ricardo Brennand",
            "address": "Alameda Antônio Brennand, s/n, Várzea, Recife - PE",
            "average_cost": "R$ 30",
            "latitude": "-8.043132",
            "longitude": "-34.978831",
            "time": "09:00 - 12:00",
        },
        "night": {
            "activity": "Clube Metrópole",
            "address": "Rua das Ninfas, 125, Boa Vista, Recife - PE",
            "average_cost": "R$ 40",
            "latitude": "-8.061615",
            "longitude": "-34.889041",
            "time": "22:00 - 03:00",
        },
    },
    "saturday": {
        "afternoon": {
            "activity": "Recife Antigo Walking Tour",
            "address": "Praça do Arsenal, s/n, Recife Antigo, Recife - PE",
            "average_cost": "R$ 30",
            "latitude": "-8.062031",
            "longitude": "-34.871888",
            "time": "14:00 - 17:00",
        },
        "date_day": "2024-07-27",
        "morning": {
            "activity": "Mercado da Encruzilhada",
            "address": "Avenida Beberibe, s/n, Encruzilhada, Recife - PE",
            "average_cost": "R$ 10",
            "latitude": "-8.026243",
            "longitude": "-34.884237",
            "time": "09:00 - 12:00",
        },
        "night": {
            "activity": "Cachaçaria Carvalheira",
            "address": "Avenida Sul, 2840, Imbiribeira, Recife - PE",
            "average_cost": "R$ 80",
            "latitude": "-8.097741",
            "longitude": "-34.899146",
            "time": "20:00 - 23:00",
        },
    },
    "sunday": {
        "afternoon": {
            "activity": "Parque Dona Lindu",
            "address": "Avenida Boa Viagem, s/n, Boa Viagem, Recife - PE",
            "average_cost": "R$ 0",
            "latitude": "-8.127576",
            "longitude": "-34.902074",
            "time": "13:00 - 17:00",
        },
        "date_day": "2024-07-21",
        "morning": {
            "activity": "Praia de Boa Viagem",
            "address": "Avenida Boa Viagem, Boa Viagem, Recife - PE",
            "average_cost": "R$ 0",
            "latitude": "-8.115304",
            "longitude": "-34.904586",
            "time": "08:00 - 12:00",
        },
        "night": {
            "activity": "Bar Burburinho",
            "address": "Rua Tomazina, 106, Recife Antigo, Recife - PE",
            "average_cost": "R$ 50",
            "latitude": "-8.063717",
            "longitude": "-34.871110",
            "time": "20:00 - 23:00",
        },
    },
    "thursday": {
        "afternoon": {
            "activity": "Paço do Frevo",
            "address": "Praça do Arsenal, s/n, Recife Antigo, Recife - PE",
            "average_cost": "R$ 10",
            "latitude": "-8.062031",
            "longitude": "-34.871888",
            "time": "13:00 - 16:00",
        },
        "date_day": "2024-07-25",
        "morning": {
            "activity": "Museu Cais do Sertão",
            "address": "Avenida Alfredo Lisboa, s/n, Recife Antigo, Recife - PE",
            "average_cost": "R$ 10",
            "latitude": "-8.063188",
            "longitude": "-34.870751",
            "time": "09:00 - 12:00",
        },
        "night": {
            "activity": "Bodega do Véio",
            "address": "Rua do Amparo, 212, Olinda - PE",
            "average_cost": "R$ 30",
            "latitude": "-8.008635",
            "longitude": "-34.854123",
            "time": "19:00 - 22:00",
        },
    },
    "tuesday": {
        "afternoon": {
            "activity": "Marco Zero",
            "address": "Avenida Alfredo Lisboa, s/n, Recife Antigo, Recife - PE",
            "average_cost": "R$ 0",
            "latitude": "-8.063184",
            "longitude": "-34.871022",
            "time": "14:00 - 17:00",
        },
        "date_day": "2024-07-23",
        "morning": {
            "activity": "Praia do Pina",
            "address": "Avenida Boa Viagem, Pina, Recife - PE",
            "average_cost": "R$ 0",
            "latitude": "-8.091327",
            "longitude": "-34.880707",
            "time": "08:00 - 12:00",
        },
        "night": {
            "activity": "Manhattan Café Theatro",
            "address": "Rua Francisco da Cunha, 881, Boa Viagem, Recife - PE",
            "average_cost": "R$ 60",
            "latitude": "-8.114209",
            "longitude": "-34.897890",
            "time": "20:00 - 23:00",
        },
    },
    "wednesday": {
        "afternoon": {
            "activity": "Parque da Jaqueira",
            "address": "Rua do Futuro, s/n, Graças, Recife - PE",
            "average_cost": "R$ 0",
            "latitude": "-8.041712",
            "longitude": "-34.895157",
            "time": "14:00 - 17:00",
        },
        "date_day": "2024-07-24",
        "morning": {
            "activity": "Jardim Botânico do Recife",
            "address": "Rua Benfica, s/n, Curado, Recife - PE",
            "average_cost": "R$ 5",
            "latitude": "-8.077292",
            "longitude": "-34.938835",
            "time": "09:00 - 12:00",
        },
        "night": {
            "activity": "Roof Tebas",
            "address": "Rua do Bom Jesus, 183, Recife Antigo, Recife - PE",
            "average_cost": "R$ 70",
            "latitude": "-8.062419",
            "longitude": "-34.868196",
            "time": "21:00 - 00:00",
        },
    },
}
extra_activities_based_on_preferred_travel_styles = [
    {
        "activity": "Festa Junina",
        "address": "Praça do Arsenal, s/n, Recife Antigo, Recife - PE",
        "average_cost": "R$ 20",
        "latitude": "-8.062031",
        "longitude": "-34.871888",
        "time": "19:00 - 23:00",
    },
    {
        "activity": "Reserva Ecológica de Dois Irmãos",
        "address": "Rua Dois Irmãos, 153, Dois Irmãos, Recife - PE",
        "average_cost": "R$ 15",
        "latitude": "-8.000005",
        "longitude": "-34.938586",
        "time": "09:00 - 14:00",
    },
    {
        "activity": "Galo da Madrugada",
        "address": "Rua da Concórdia, s/n, São José, Recife - PE",
        "average_cost": "R$ 30",
        "latitude": "-8.074462",
        "longitude": "-34.878193",
        "time": "07:00 - 12:00",
    },
]

accommodations = [
    {
        "address": "Avenida Boa Viagem, 5426, Boa Viagem, Recife - PE",
        "average_cost": "R$ 250 per night",
        "latitude": "-8.133659",
        "longitude": "-34.904384",
        "name": "Hotel Atlante Plaza",
        "type": "Hotel",
    },
    {
        "address": "Rua Miguel Couto, 81, Graças, Recife - PE",
        "average_cost": "R$ 150 per night",
        "latitude": "-8.052709",
        "longitude": "-34.894976",
        "name": "Pousada Villa Boa Vista",
        "type": "Pousada",
    },
    {
        "address": "Rua Marquês de Valença, 210, Boa Viagem, Recife - PE",
        "average_cost": "R$ 70 per night",
        "latitude": "-8.120503",
        "longitude": "-34.900147",
        "name": "Hostel Piratas do Sol",
        "type": "Hostel",
    },
]

restaurants = [
    {
        "address": "Praça Joaquim Nabuco, 147, Santo Antônio, Recife - PE",
        "average_cost": "R$ 100",
        "latitude": "-8.064834",
        "longitude": "-34.880644",
        "name": "Leite",
        "type": "Fine Dining",
    },
    {
        "address": "Rua Baltazar Pereira, 32, Boa Viagem, Recife - PE",
        "average_cost": "R$ 50",
        "latitude": "-8.125102",
        "longitude": "-34.903098",
        "name": "Parraxaxá",
        "type": "Regional",
    },
    {
        "address": "Rua Petrolina, 19, Boa Viagem, Recife - PE",
        "average_cost": "R$ 60",
        "latitude": "-8.114554",
        "longitude": "-34.900967",
        "name": "Chica Pitanga",
        "type": "Brazilian",
    },
]

mocked_response = {
    "itinerary": itinerary,
    "recommended_accommodations": accommodations,
    "recommended_restaurants": restaurants,
    "extra_activities_based_on_preferred_travel_styles": extra_activities_based_on_preferred_travel_styles,
}


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
