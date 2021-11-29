# class to create new metrics
class Metric:
    # constructor
    def __init__(self, metric_name, metric_type, comment, value, params):
        # if some key values are missing return error
        if metric_name is None or metric_type is None or value is None:
            raise ValueError

        # safe values in new entity
        self.metric_name = metric_name
        self.metric_type = metric_type
        self.comment = comment
        self.value = value
        self.params = params

    # return entity values as formatted string for prometheus to parse
    def to_string(self):
        # "# HELP metrics_name comment"
        help_string = f'# HELP {self.metric_name} {self.comment}'

        # "# TYPE metrics_name metric_type"
        type_string = f'# TYPE {self.metric_name} {self.metric_type}'

        output = ""

        # only add a pure comment line if there is a comment
        if self.comment is not None:
            output += help_string + "\n"
        output += type_string + "\n" + f'{self.metric_name}{self.__params_to_string()} {self.value}'

        return output

    # format params to string
    def __params_to_string(self):

        if self.params is None:
            return ""

        output = "{"

        for k, v in self.params.items():
            output += f'{k}="{v}" ,'

        return output[0:-2] + "}"
