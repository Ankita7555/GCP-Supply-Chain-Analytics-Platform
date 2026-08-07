from pyspark.sql import SparkSession

from pyspark.sql.functions import (
    col,
    to_timestamp,
    datediff,
    when
)

spark = (
    SparkSession
    .builder
    .appName("SupplyChainETL")
    .getOrCreate()
)

orders = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/raw/orders.csv")
)

shipments = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/raw/shipments.csv")
)

orders_clean = (
    orders
    .dropDuplicates(["order_id"])
    .filter(
        (col("quantity") > 0)
        & (col("unit_price") >= 0)
    )
)

shipments_enriched = (
    shipments
    .withColumn(
        "ship_ts",
        to_timestamp("ship_ts")
    )
    .withColumn(
        "delivery_ts",
        to_timestamp("delivery_ts")
    )
    .withColumn(
        "actual_delivery_days",
        datediff(
            "delivery_ts",
            "ship_ts"
        )
    )
    .withColumn(
        "delay_flag",
        when(
            col("actual_delivery_days")
            > col("planned_delivery_days"),
            1
        ).otherwise(0)
    )
)

orders_clean.write \
    .mode("overwrite") \
    .parquet(
        "data/processed/pyspark_orders"
    )

shipments_enriched.write \
    .mode("overwrite") \
    .parquet(
        "data/processed/pyspark_shipments"
    )

spark.stop()
