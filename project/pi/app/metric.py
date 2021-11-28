class Metric:
    def __init__(self, metric_name, metric_type, comment, value, params):

        if metric_name is None or metric_type is None or value is None:
            raise ValueError

        self.metric_name = metric_name
        self.metric_type = metric_type
        self.comment = comment
        self.value = value
        self.params = params

    def to_string(self):
        help_string = f'# HELP {self.metric_name} {self.comment}'
        type_string = f'# TYPE {self.metric_name} {self.metric_type}'

        output = ""

        if self.comment is not None:
            output += help_string + "\n"
        output += type_string + "\n" + f'{self.metric_name}{self.__params_to_string()} {self.value}'

        return output

    def __params_to_string(self):

        if self.params is None:
            return ""

        output = "{"

        for k, v in self.params.items():
            output += f'{k}="{v}" ,'

        return output[0:-2] + "}"
