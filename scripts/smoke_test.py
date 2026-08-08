"""Verify PySpark works. Run: python scripts/smoke_test.py"""

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("smoke-test")
    .master("local[*]")
    .getOrCreate()
)

df = spark.createDataFrame(
    [("Alice", 34), ("Bob", 45), ("Carol", 29)],
    ["name", "age"],
)

df.show()
print(f"Spark {spark.version} is working. Row count: {df.count()}")

spark.stop()
