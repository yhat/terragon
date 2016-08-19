from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS
import sparkle

sc = SparkContext()

stringified_spark_model = open("/tmp/test.sparkle", "rb").read()
model = sparkle.load_spark_model(sc, stringified_spark_model)

print model
print model.predict(2, 2)
