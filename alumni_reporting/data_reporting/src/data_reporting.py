from pyspark.sql import SparkSession
import datetime
import os
import shutil

def create_spark_session():
    try:
        spark = SparkSession.builder.appName("sample-app").getOrCreate()
        print("Creating a spark session...")
        return spark
    except Exception as e:
        return None

def stop_spark_session(spark):
    try:
        spark.stop()
        print("Spark session has stopped !!!")
        return True
    except Exception as e:
        return False

def read_df(spark, parquet_file_path):
    try:
        print("Started reading the dataframe using parquet from ::: ", parquet_file_path)
        df = spark.read.format("parquet").option("header","true").load(parquet_file_path)
        return df
    except Exception as e:
        return None

def load_df_to_csv(df, csv_output_filepath, filename):
    try:
        temp_folder = "temp_folder"
        print("Converting the dataframe to csv file...")
        (df.coalesce(1).write
         .option("header","true")
         .mode("overwrite")
         .csv(csv_output_filepath+temp_folder))
        
        print("Loading the csv file.")
        # Create final csv file
        temp_op_files = os.listdir(csv_output_filepath+temp_folder)
        for f in temp_op_files:
            if f.endswith(".csv"):
                os.rename(csv_output_filepath+temp_folder+'/'+f, csv_output_filepath+filename)
        
        shutil.rmtree(csv_output_filepath+temp_folder)
        return csv_output_filepath+filename
    except Exception as e:
        return None
    
if __name__=='__main__':
    # Test Code execution
    spark = create_spark_session()
    print("Spark session is created !!!")
    parquet_filePath = "/home/parquet_data_export/alumni/"
    df = read_df(spark, parquet_filePath)
    print("Dataframe records count is ::: ", df.count())
    output_fpath = "/home/output_data/"
    curr_dt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = "alumni_"+curr_dt+".csv"
    output_fname = load_df_to_csv(df, output_fpath, filename)
    print("CSV file created ::: ", output_fname)
    stop_spark_session(spark)
