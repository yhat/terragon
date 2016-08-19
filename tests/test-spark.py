from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS
import sparkle

sc = SparkContext()

r1 = (1, 1, 1.0)
r2 = (1, 2, 2.0)
r3 = (2, 1, 2.0)
ratings = sc.parallelize([r1, r2, r3])
model = ALS.trainImplicit(ratings, 1, seed=10)
model.predict(2, 2)



stringified_spark_model = sparkle.save_spark_model(model)
# thing = read_tarfile_string(stringified_spark_model)
# print thing
# print thing.predict(2, 2)




# "from %s import %s" % (model.__module__, model.__class__.__name__)
# from pyspark.mllib.recommendation import MatrixFactorizationModel
#
# MatrixFactorizationModel.load(sc, "tests/myModel.spkl")
# model.predict(2, 2)
