# script codecarbone.py
# decorateur pour lancer une fonction et mesurer la consommation de codecarbone
from codecarbon import OfflineEmissionsTracker
from functools import wraps



def codecarbone_fr(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracker = OfflineEmissionsTracker(
                project_name="LivrIA",
                country_iso_code="FRA"
        )
        tracker.start()    

        result = func(*args, **kwargs)

        tracker.stop()
        print(f"La fonction {func.__name__} a émis :\n\t- {tracker.final_emissions_data.emissions} kgCO2e,\n\t- CPU : {tracker.final_emissions_data.cpu_energy} Wh\n\t- GPU : {tracker.final_emissions_data.gpu_energy} Wh")

        return result
    return wrapper


# Exemple d'utilisation
if __name__ == "__main__":
    @codecarbone_fr
    def test():
        print("Hello world")



    test()

