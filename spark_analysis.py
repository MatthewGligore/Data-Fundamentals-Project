from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main() -> None:
    spark = (
        SparkSession.builder.appName("fema-disaster-analysis")
        .master("local[*]")
        .getOrCreate()
    )

    input_path = "fema_disasters.csv"
    output_dir = "spark_output/gulf_incident_counts"

    disasters_df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(input_path)
    )

    selected_columns = [
        "state",
        "declarationType",
        "fyDeclared",
        "incidentType",
        "designatedArea",
    ]
    selected_df = disasters_df.select(*selected_columns)

    print("=== Selected columns ===")
    print(selected_columns)
    print("\n=== DataFrame head(5) on selected columns ===")
    selected_df.show(5, truncate=False)

    # DataFrame method outcome: top states by declaration count.
    state_totals_df = (
        selected_df.groupBy("state")
        .count()
        .withColumnRenamed("count", "declaration_count")
        .orderBy(F.desc("declaration_count"))
    )
    print("\n=== Top 10 states by declarations (DataFrame API) ===")
    state_totals_df.show(10, truncate=False)

    # Spark SQL outcome: incident counts for Gulf Coast states.
    selected_df.createOrReplaceTempView("disasters")
    gulf_sql = """
        SELECT
            incidentType,
            COUNT(*) AS incident_count
        FROM disasters
        WHERE state IN ('TX', 'LA', 'MS', 'AL', 'FL')
        GROUP BY incidentType
        ORDER BY incident_count DESC
    """
    gulf_incidents_df = spark.sql(gulf_sql)
    print("\n=== Gulf Coast incident counts (Spark SQL) ===")
    gulf_incidents_df.show(10, truncate=False)

    # Write as Spark part file for assignment evidence.
    gulf_incidents_df.coalesce(1).write.mode("overwrite").option("header", True).csv(output_dir)
    print(f"\nWrote Spark output to: {output_dir}")

    spark.stop()


if __name__ == "__main__":
    main()
