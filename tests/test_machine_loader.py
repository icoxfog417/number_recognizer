import unittest
from sklearn import datasets
from machines.machine_loader import MachineLoader
import machines.number_recognizer


class TestMachineLoader(unittest.TestCase):

    def test_load(self):
        machine = MachineLoader.load(machines.number_recognizer)
        self.assertTrue(machine)

    def test_predict(self):
        digits = datasets.load_digits()

        from sklearn import svm
        from sklearn import cross_validation

        clf = svm.SVC(gamma=0.001, C=100)
        clf = clf.fit(digits.data, digits.target)
        cross_validation.cross_val_score(clf, digits.data[:-1], digits.target[:-1], cv=5)
        print(digits.target)

        sample = [0, 0, 0, 0, 229, 0, 0, 0, 0, 254, 255, 0, 0, 78, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                  0, 255, 0, 0, 0, 0, 0, 255, 255, 0, 0, 0, 0, 68, 255, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255,
                  255, 0, 0, 0, 0, 0, 0, 0, 6, 255, 255, 0]

        predicted = clf.predict(sample)
        print(predicted)

        print(digits.data[-1])
        predicted = clf.predict(digits.data[-1])
        print(predicted)


