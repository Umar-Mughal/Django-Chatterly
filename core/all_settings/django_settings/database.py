import os


def get_database_settings():
    print("db name =====", os.getenv("DB_NAME"))
    return {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
        }
    }
