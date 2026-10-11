import httpx
import json
import time
import random
from post_data import add_data, PostOffice



def main():
    url = "https://www.pochta.ru/suggestions/v2/postoffices.find-from-rectangle"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:157.0) Gecko/20100101 Firefox/157.0",
        "Accept": "application/json",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json"
    }

    offices = dict()
    post_offices = list()

    for i in range(0, 7):
        for j in range(0, 5):
    # for i in range(0, 1):
    #     for j in range(0, 1):
            print(f"Square {i}, {j}")
            time.sleep(random.randint(1, 10) / 10)
            lat = 42.0 + i
            lon = 128.0 + 3 * j
            # 49-42 128-144
            json_data = {"extFilters": ["NOT_TEMPORARY_CLOSED", "NOT_PRIVATE", "NOT_CLOSED", "ONLY_ATI"],
                         "topLeftPoint": {"latitude": str(lat + 1), "longitude": str(lon + 3)},
                         "bottomRightPoint": {"latitude": str(lat), "longitude": str(lon)},
                         "precision": 0, "onlyCoordinate": False, "offset": 0, "limit": 50000}

            with httpx.Client() as client:
                r = client.post(url, headers=headers, data=json.dumps(json_data))

            for office in r.json().get("postOffices"):
                address = office.get("address")
                guid = address.get("addressGuid")
                if guid:
                    post_mark = {
                        guid: {
                            'region': address.get("region"),
                            'district': address.get("district"),
                            # 'fullAddress': address.get("fullAddress"),
                            'settlementOrCity': address.get("settlementOrCity"),
                            'settlementTypeOrCityType': address.get("settlementTypeOrCityType"),
                            'shortAddress': address.get("shortAddress"),
                            "postalCode": office.get("postalCode"),
                            "typeCode": office.get("typeCode"),
                            "typeId": office.get("typeId"),
                            "latitude": office.get("latitude"),
                            "longitude": office.get("longitude"),
                        },
                    }
                    offices.update(post_mark)

    for key in offices.keys():
        data = offices.get(key)
        post_office = PostOffice(
            id = key,
            region = data.get("region"),
            district = data.get("district"),
            settlementOrCity = data.get("settlementOrCity"),
            settlementTypeOrCityType = data.get("settlementTypeOrCityType"),
            shortAddress = data.get("shortAddress"),
            postalCode = data.get("postalCode"),
            typeCode = data.get("typeCode"),
            typeId = data.get("typeId"),
            latitude = float(data.get("latitude")),
            longitude = float(data.get("longitude"))
        )
        post_offices.append(post_office)

        if len(post_offices) > 100:
            add_data(post_offices)
            post_offices.clear()

    add_data(post_offices)

if __name__ == "__main__":
    main()
