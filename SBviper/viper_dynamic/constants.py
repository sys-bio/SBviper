from viper_helpers.wrappers.frechet_distance_wrapper import \
    frechet_distance_wrapper
from viper_dynamic.Filter.filter import Filter

frechet_distance_filter = Filter(frechet_distance_wrapper, 0.5)

str_to_function = {"frechet_distance": frechet_distance_filter}


def get_filter(filter_name, tolerance_value):
    if filter_name == "frechet_distance":
        print("Entered tolerance_value is " + tolerance_value)
        return Filter(frechet_distance_wrapper, tolerance_value)
