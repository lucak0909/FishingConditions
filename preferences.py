fish_preferences = {
        "Pike": {
            "temperature": (10, 20),  # °C
            "air_pressure": (1010, 1030),  # hPa
            "wind_speed": (0, 15),  # km/h
            "cloud_cover": (20, 80),  # percentage
            "precipitation": (0, 5),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Perch": {
            "temperature": (15, 25),  # °C
            "air_pressure": (1015, 1025),  # hPa
            "wind_speed": (0, 10),  # km/h
            "cloud_cover": (10, 70),  # percentage
            "precipitation": (0, 3),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Brown Trout": {
            "temperature": (8, 16),  # °C
            "air_pressure": (1010, 1025),  # hPa
            "wind_speed": (0, 12),  # km/h
            "cloud_cover": (30, 90),  # percentage
            "precipitation": (0, 8),  # mm
            "precipitation_type": ["None", "Rain", "Drizzle"]
        },
        "Atlantic Salmon": {
            "temperature": (5, 15),  # °C
            "air_pressure": (1010, 1020),  # hPa
            "wind_speed": (0, 15),  # km/h
            "cloud_cover": (30, 100),  # percentage
            "precipitation": (0, 10),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Roach": {
            "temperature": (12, 22),  # °C
            "air_pressure": (1010, 1030),  # hPa
            "wind_speed": (0, 10),  # km/h
            "cloud_cover": (10, 60),  # percentage
            "precipitation": (0, 4),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Bream": {
            "temperature": (12, 22),  # °C
            "air_pressure": (1012, 1028),  # hPa
            "wind_speed": (0, 12),  # km/h
            "cloud_cover": (20, 70),  # percentage
            "precipitation": (0, 5),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Rudd": {
            "temperature": (15, 25),  # °C
            "air_pressure": (1010, 1030),  # hPa
            "wind_speed": (0, 8),  # km/h
            "cloud_cover": (10, 50),  # percentage
            "precipitation": (0, 2),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Tench": {
            "temperature": (16, 24),  # °C
            "air_pressure": (1010, 1028),  # hPa
            "wind_speed": (0, 10),  # km/h
            "cloud_cover": (15, 60),  # percentage
            "precipitation": (0, 3),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Eel": {
            "temperature": (10, 20),  # °C
            "air_pressure": (1010, 1025),  # hPa
            "wind_speed": (0, 12),  # km/h
            "cloud_cover": (30, 80),  # percentage
            "precipitation": (0, 5),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Dace": {
            "temperature": (12, 20),  # °C
            "air_pressure": (1010, 1025),  # hPa
            "wind_speed": (0, 10),  # km/h
            "cloud_cover": (10, 60),  # percentage
            "precipitation": (0, 4),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Chub": {
            "temperature": (10, 20),  # °C
            "air_pressure": (1010, 1025),  # hPa
            "wind_speed": (0, 15),  # km/h
            "cloud_cover": (20, 80),  # percentage
            "precipitation": (0, 6),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Gudgeon": {
            "temperature": (10, 20),  # °C
            "air_pressure": (1010, 1030),  # hPa
            "wind_speed": (0, 8),  # km/h
            "cloud_cover": (20, 70),  # percentage
            "precipitation": (0, 2),  # mm
            "precipitation_type": ["None", "Rain"]
        }
    }


def get_fish_preferences():
    return fish_preferences
