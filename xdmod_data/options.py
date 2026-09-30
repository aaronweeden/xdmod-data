from contextlib import contextmanager


class __Options:
    def __init__(self):
        self.__options = {
            "warn_unknown_filter_values": {
                "value": "error",
                "possible_values": ["error", "warning", "silent"],
            },
        }

    def get_option(self, key):
        self.__validate_key(key)
        return self.__options[key]["value"]

    def set_option(self, key, value):
        self.__validate_key(key)
        self.__validate_value(key, value)
        self.__options[key]["value"] = value

    @contextmanager
    def option_context(self, *args):
        if len(args) % 2 != 0:
            raise ValueError(
                "`option_context` requires an even number of arguments: pairs of option and value."
            )
        original_options = {}
        try:
            for i in range(0, len(args), 2):
                key, value = args[i], args[i + 1]
                if key not in original_options:
                    original_options[key] = self.get_option(key)
                self.set_option(key, value)
            yield
        finally:
            for key, value in original_options.items():
                self.set_option(key, value)

    def __validate_key(self, key):
        if key not in self.__options:
            raise KeyError(
                f"No such option. Valid options are: {', '.join(list(self.__options))}"
            ) from None

    def __validate_value(self, key, value):
        if value not in self.__options[key]["possible_values"]:
            raise ValueError(
                f"No such value for '{key}' option. Valid values are: {', '.join(self.__options[key]['possible_values'])}."
            ) from None


__options = __Options()
get_option = __options.get_option
set_option = __options.set_option
option_context = __options.option_context
