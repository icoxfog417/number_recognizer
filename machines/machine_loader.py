import os
from sklearn.externals import joblib


class MachineLoader():
    MACHINE_FILE = "machine.pkl"
    DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../data/")
    FEEDBACK_FILE_FORMAT = "{0}_feedback.txt"

    @classmethod
    def load(cls, pkg, file_name=""):
        machine = None
        machine_file = cls.get_pkg_path(pkg, file_name if file_name else cls.MACHINE_FILE)

        if os.path.isfile(machine_file):
            machine = joblib.load(machine_file)
        else:
            raise Exception("{0} doesn't exist.".format(machine_file))

        return machine

    @classmethod
    def feedback(cls, pkg, feedback, separator="\t", encoding="utf-8"):
        feedback_file = os.path.join(cls.DATA_FOLDER, cls.FEEDBACK_FILE_FORMAT.format("_".join(pkg.__name__.split("."))))
        with open(feedback_file, "ab+") as outfile:
            line = separator.join([str(e) for e in feedback])
            outfile.write((line + os.linesep).encode(encoding))

        return feedback_file

    @classmethod
    def save(cls, pkg, machine, file_name=""):
        machine_file = cls.get_pkg_path(pkg, file_name if file_name else cls.MACHINE_FILE)
        joblib.dump(machine, machine_file)

    @classmethod
    def get_pkg_path(cls, pkg, file_name=""):
        pkg_path = os.path.dirname(pkg.__file__)
        if file_name:
            pkg_path = os.path.join(pkg_path, file_name)
        return pkg_path
