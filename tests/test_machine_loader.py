import os
import unittest
from sklearn import datasets
from machines.machine_loader import MachineLoader
import machines.number_recognizer


class TestMachineLoader(unittest.TestCase):

    def test_load(self):
        machine = MachineLoader.load(machines.number_recognizer)
        self.assertTrue(machine)

    def test_feedback(self):
        test_file = "test_feedback.txt"
        feedback_file = MachineLoader.feedback(machines.number_recognizer, None, file_name=test_file)
        if os.path.isfile(feedback_file):
            os.remove(feedback_file)

        data = [0] * 64
        target = [0]
        feedback = target + data
        # create file
        MachineLoader.feedback(machines.number_recognizer, feedback, file_name=test_file)
        # append file
        MachineLoader.feedback(machines.number_recognizer, feedback, file_name=test_file)

        with open(feedback_file, mode="rb") as r:
            lines = r.readlines()
            self.assertEqual(2, len(lines))

        os.remove(feedback_file)

    def test_predict(self):
        digits = datasets.load_digits()

        from sklearn import svm
        from sklearn import cross_validation

        clf = svm.SVC(gamma=0.001, C=100)
        clf = clf.fit(digits.data, digits.target)
        cross_validation.cross_val_score(clf, digits.data[:-1], digits.target[:-1], cv=5)
        predicted = clf.predict(digits.data[-1])
        self.assertGreaterEqual(predicted, 0)