

class Validator():

    def __init__(self):
        pass

    @classmethod
    def validate_data(cls, data):
        """
        validate the data.
        input data: 8 * 8 image
        format: 8 * 8 = 64 length array. each element is gray-scale float value.
        :param data:
        :return:
        """
        validated = []

        # check data length 8 * 8 = 64
        if len(data) == 64:
            try:
                validated = [float(v) for v in data]
            except Exception as ex:
                validated = []

        return validated

    @classmethod
    def validate_label(cls, label):
        """
        validate the label data
        input data: 1-10 number
        input format: int value, its range is 1-10.
        :param label:
        :return:
        """

        result = -1
        try:
            target_number = int(label)
            if 0 <= target_number < 10:
                result = target_number
        except Exception as ex:
            result = -1

        return result

    @classmethod
    def validate_feedback(cls, feedback):
        validated = []
        if len(feedback) > 0:
            # validate label
            label = cls.validate_label(feedback[0])

            # validate data
            data = cls.validate_data(feedback[1:])

            if len(data) > 0 and label > -1:
                validated = [label] + data

        return validated
