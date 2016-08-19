from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS
import terragon

sc = SparkContext()

r1 = (1, 1, 1.0)
r2 = (1, 2, 2.0)
r3 = (2, 1, 2.0)
ratings = sc.parallelize([r1, r2, r3])
model = ALS.trainImplicit(ratings, 1, seed=10)
model.predict(2, 2)


stringified_spark_model = terragon.dumps_spark_to_base64(sc, model)

with open("/tmp/test.sparkle", "wb") as f:
    f.write(stringified_spark_model)
