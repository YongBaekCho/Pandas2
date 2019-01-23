from hw3 import *
import unittest, numpy as np, pandas as pd, json, sqlite3 
from compare_pandas import *

''' 
Auxiliary files needed:
    classes_redacted.db
    compare_pandas.py
    sun_frame.pkl, daylength_series.pkl, results_frame.pkl
This one is needed by hw1.py and is therefore required:
    sunrise_sunset.csv
'''

class TestFns(unittest.TestCase):
    def test_student_report(self):
        entries = {'13101061': 'Xowarej, Lauren, 13101061\n\
-------------------------\nISTA 131 F17: F\nISTA 350 S17: R\n',
'13100530': 'Puvejob, Eden, 13100530\n\
-----------------------\nISTA 130 S14: R\nISTA 131 F17: R\n',
'13100352': 'Tonayax, Natalie, 13100352\n\
--------------------------\nISTA 130 F16: R\nISTA 131 F17: A\nISTA 350 S18: U\n',
'14121342':''}
        for key, val in entries.items():
            self.assertEqual(val, student_report('classes_redacted.db', key))
        
    def test_A_students(self):
        conn = sqlite3.connect('classes_redacted.db')
        tests = [['Drakahey, Shannon', 'Foxobuc, Trevor', #conn
                'Mijasaz, Brandon', 'Popocoj, Kathryn',
                'Poxozih, Tzuhsien', 'Qutabec, Jeremy',
                'Saxigot, Sergio', 'Sitafov, Ryan',
                'Strocitit, William', 'Strolicih, Jared'],
                ['Beseboc, Chris', 'Bifedok, Alyssa', 'Burapev, Brian', #ista_130_f17
                'Darefir, Parker', 'Dotasak, Zach', 'Drebegan, Scott',
                'Drimaliz, Dingbo', 'Fipugax, Anmol', 'Gahejov, Vamsee',
                'Gufunoz, Bri'],
                ['Baqarer, Philipp', 'Hetewoh, Nicholas', 'Lanotey, Munir', #ista_350_s15, senior
                'Momevec, Yung-Shun', 'Padefak, Bonnie', 'Risazif, Jack',
                'Stinomel, Brandon'],
                ['Druwifex, Erik', 'Javevuc, Matthew'], #ista_350_s15, junior, 2
                []] #ista_350_s15, prof
        
        self.assertEqual(tests[0], A_students(conn))
        self.assertEqual(tests[1], A_students(conn, 'ista_130_f17'))
        self.assertEqual(tests[2], A_students(conn, 'ista_350_s15', 'senior'))
        self.assertEqual(tests[3], A_students(conn, 'ista_350_s15', 'Junior', 2))
        self.assertEqual(tests[4], A_students(conn, 'ista_350_s15', 'Prof'))
    
    def test_class_performance(self):
        conn = sqlite3.connect('classes_redacted.db')
        entries = [{'A': 29.3, 'B': 8.6, 'F': 17.2, 'R': 20.7, 'U': 24.1},  #conn
                   {'A': 22.9, 'B': 16.7, 'F': 22.9, 'R': 22.9, 'U': 14.6}, #350_s15
                   {'A': 17.0, 'B': 25.2, 'F': 16.3, 'R': 19.3, 'U': 22.2}, #130_s15
                   {'A': 27.7, 'B': 17.0, 'F': 21.3, 'R': 23.4, 'U': 10.6}, #120_f16
                   {'A': 26.1, 'B': 13.0, 'F': 23.9, 'R': 19.6, 'U': 17.4}] #350_s18
    
        self.assertEqual(entries[0], class_performance(conn))
        self.assertEqual(entries[1], class_performance(conn, 'ista_350_s15'))
        self.assertEqual(entries[2], class_performance(conn, 'ista_130_s15'))
        self.assertEqual(entries[3], class_performance(conn, 'ista_120_f16'))
        self.assertEqual(entries[4], class_performance(conn, 'ista_350_s18'))
    
    def test_read_frame(self):
        correct = pd.read_pickle('sun_frame.pkl')
        sf = read_frame()
        self.assertTrue(compare_frames_str(correct, sf))
        
    def test_get_series(self):
        rise_correct = pd.read_pickle('sunrise.pkl')
        set_correct = pd.read_pickle('sunset.pkl')
        sun_frame = pd.read_pickle('sun_frame.pkl')
        rise, set = get_series(sun_frame)
        self.assertTrue(compare_series_str(rise_correct, rise))
        self.assertTrue(compare_series_str(set_correct, set))
   
    def test_longest_day(self):
        rise_correct = pd.read_pickle('sunrise.pkl')
        set_correct = pd.read_pickle('sunset.pkl')
        self.assertEqual((pd.Timestamp('2018-06-18 00:00:00', freq='D'), '1416'), longest_day(rise_correct, set_correct))

    def test_sunrise_dif(self):
        rise = pd.read_pickle('sunrise.pkl')
        entries = {'2018-06-18 00:00:00': 19,
                   '2018-05-18 00:00:00': 75,
                   '2018-05-27 00:00:00': 59,
                   '2018-4-1 00:00:00': 125,
                   '2018-4-17 00:00:00': 116}
        for key, val in entries.items():
            self.assertEqual(val, sunrise_dif(rise, pd.Timestamp(key, freq = 'D'))) 
    
def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + ' / 100')
    
if __name__ == "__main__":
    main()