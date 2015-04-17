import os
from sklearn.externals import joblib


class MachineLoader():

    @classmethod
    def load(cls, pkg):
        machine = None
        machine_path = os.path.dirname(pkg.__file__)
        machine_file = os.path.join(machine_path, "machine.pkl")

        if os.path.isfile(machine_file):
            machine = joblib.load(machine_file)
        else:
            raise Exception("machine.pkl is not created yet in {0}".format(machine_path))

        return machine
