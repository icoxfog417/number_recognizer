import os
from sklearn.externals import joblib


class MachineLoader():
    MACHINE_FILE = "machine.pkl"
    FEEDBACK_FILE = "feedback.txt"

    @classmethod
    def load(cls, pkg):
        machine = None
        machine_file = cls.__get_pkg_path(pkg, cls.MACHINE_FILE)

        if os.path.isfile(machine_file):
            machine = joblib.load(machine_file)
        else:
            raise Exception("{0} doesn't exist.".format(machine_file))

        return machine

    @classmethod
    def feedback(cls, pkg, feedback, file_name="", separator="\t", encoding="utf-8"):
        feedback_file = cls.__get_pkg_path(pkg, file_name if file_name else cls.FEEDBACK_FILE)
        if feedback:
            with open(feedback_file, "ab+") as outfile:
                line = separator.join([str(e) for e in feedback])
                outfile.write((line + os.linesep).encode(encoding))

        return feedback_file

    @classmethod
    def __get_pkg_path(cls, pkg, file_name=""):
        pkg_path = os.path.dirname(pkg.__file__)
        if file_name:
            pkg_path = os.path.join(pkg_path, file_name)
        return pkg_path
