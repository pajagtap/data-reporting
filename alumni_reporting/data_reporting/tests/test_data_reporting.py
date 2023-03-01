import os,sys
import unittest
import datetime
import csv

abspath = os.path.abspath(".")
sys.path.append(abspath)

from src import data_reporting as data_rep

PARQUET_FILEPATH = "/home/parquet_data_export/alumni"
CSV_OUTPUT_PATH = "/home/output_data/"

class TestDataReporting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spark = data_rep.create_spark_session()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.spark.stop()
        except:
            None

    def test_create_spark_session(self):
        self.assertNotEqual(self.spark, None)

    def test_stop_spark_session(self):
        isSparkStopped = data_rep.stop_spark_session(self.spark)
        self.assertTrue(isSparkStopped)

    def test_read_df(self):
        df = data_rep.read_df(self.spark, PARQUET_FILEPATH)
        self.assertEqual(df.count(), 11)

    def test_load_to_csv(self):
        df = data_rep.read_df(self.spark, PARQUET_FILEPATH)
        curr_dt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = "alumni_"+curr_dt+".csv"
        output_fname = data_rep.load_df_to_csv(df, CSV_OUTPUT_PATH, filename)

        data = []
        with open(output_fname) as f:
            csvreader = csv.reader(f)
            header = next(csvreader)
            for row in csvreader:
                data.append(row)

        self.assertEqual(df.columns, header)
        self.assertEqual(df.count(), len(data))


if __name__ == "__main__":
    unittest.main()