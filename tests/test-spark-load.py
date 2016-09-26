from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS
import terragon

sc = SparkContext()

stringified_spark_model = open("/tmp/test.sparkle", "rb").read()
model = terragon.loads_spark_from_base64(sc, stringified_spark_model)

print(model)
print(model.predict(2, 2))
