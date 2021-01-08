from viper_helpers.wrappers.frechet_distance_wrapper import \
    frechet_distance_wrapper
from viper_dynamic.Filter.filter import Filter

frechet_distance_filter = Filter(frechet_distance_wrapper, 0.5)

str_to_function = {"frechet_distance": frechet_distance_filter}
