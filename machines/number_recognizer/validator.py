

class Validator():

    def __init__(self):
        pass

    @classmethod
    def validate_data(cls, data):
        validated = []

        # check data length 8 * 8 = 64
        if len(data) == 64:
            try:
                validated = [float(v) for v in data]
            except Exception as ex:
                validated = []

        return validated

    @classmethod
    def validate_target(cls, target):
        result = -1
        try:
            target_number = int(target)
            if 0  <= target_number < 10:
                result = target_number
        except Exception as ex:
            result = -1

        return result

    @classmethod
    def validate_feedback(cls, feedback):
        validated = []
        if len(feedback) > 0:
            # validate target
            target = cls.validate_target(feedback[0])

            # validate data
            data = cls.validate_data(feedback[1:])

            if target > -1 and len(data) > 0:
                validated = [target] + data

        return validated
