# PySpark Sandbox

A local playground for learning PySpark — no cluster or cloud account needed.
Spark runs in "local mode" on your machine, using all CPU cores as workers.

## Prerequisites (one-time downloads)

1. **Python 3.10–3.12** — [python.org/downloads](https://www.python.org/downloads/).
   Check the "Add Python to PATH" box in the installer.
2. **Java (JDK) 17 or 21** — PySpark 4.x requires it (Java 8/11 no longer work).
   Recommended: [Eclipse Temurin 21 (LTS)](https://adoptium.net/temurin/releases/?version=21).
   In the MSI installer, enable **"Set JAVA_HOME variable"**.
3. That's it. PySpark itself installs via pip (below). No Hadoop or Spark
   download needed for local mode.

Verify in a new PowerShell window:

```powershell
python --version   # 3.10-3.12
java -version      # 17 or 21
```

## Setup

From the project root:

```powershell
# 1. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies (PySpark is ~450 MB, takes a few minutes)
pip install -r requirements.txt

# 3. Verify Spark works
python scripts\smoke_test.py

# 4. Generate the practice datasets (writes CSVs to data/generated/)
python scripts\generate_data.py

# 5. Launch JupyterLab and open notebooks/01_getting_started.ipynb
python -m jupyter lab
```

> If `Activate.ps1` is blocked by execution policy, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Windows note: winutils

Local-mode PySpark mostly works fine on Windows without Hadoop's `winutils`.
You may see a `HADOOP_HOME` warning at startup — it's safe to ignore. If you
later hit actual errors writing files (e.g. saving Parquet), grab a community
`hadoop-3.x/bin` folder (search "hadoop winutils"), put it at `C:\hadoop\bin`,
and set the environment variable `HADOOP_HOME=C:\hadoop`.

## Project layout

```
pyspark-sandbox/
├── data/generated/     # practice CSVs (created by generate_data.py, git-ignored)
├── notebooks/          # your playground — start at 01_getting_started.ipynb
├── scripts/
│   ├── generate_data.py   # builds sample customers/products/orders datasets
│   └── smoke_test.py      # quick "is Spark working?" check
└── requirements.txt
```

The generated data is a mini retail scenario: `customers.csv` (2k rows),
`products.csv` (10 rows), `orders.csv` (50k rows). It intentionally contains
some messy data — missing emails, inconsistent casing, orphaned orders — so
you can practice cleaning and joins realistically.

## Learning roadmap

Work through these phases in order. Each maps to concrete exercises you can
do in a notebook against the generated data.

### Phase 1 — Fundamentals (week 1)
- What Spark is: driver, executors, lazy evaluation, transformations vs actions.
- Create a `SparkSession`; read `orders.csv` with `spark.read.csv` (use
  `header=True`, `inferSchema=True`).
- Core DataFrame ops: `select`, `filter`, `withColumn`, `orderBy`, `show`,
  `printSchema`, `count`, `distinct`.
- Exercise: find all orders over $500, add a `year` column from `order_date`,
  count orders per year.

### Phase 2 — Aggregations and joins (week 2)
- `groupBy` + `agg` (`sum`, `avg`, `countDistinct`), column expressions with
  `pyspark.sql.functions` (`F.col`, `F.when`, `F.round`).
- Joins: inner/left/anti. Join orders to customers and products.
- Exercise: revenue by product category; top 10 customers by lifetime spend;
  find orders whose customer_id doesn't exist (anti join).

### Phase 3 — Data cleaning and Spark SQL (week 3)
- Handling nulls (`dropna`, `fillna`, `F.coalesce`), string functions
  (`initcap`, `trim`), casting types, deduplication.
- Register DataFrames as temp views and rewrite Phase 2 exercises in SQL
  with `spark.sql(...)`.
- Exercise: standardize the city casing in customers, replace blank emails
  with null, then produce a clean joined "order facts" table.

### Phase 4 — Window functions and file formats (week 4)
- `Window.partitionBy(...).orderBy(...)` with `row_number`, `rank`, `lag`,
  running totals.
- Write and read Parquet; compare file size and read speed vs CSV.
  Partitioned writes (`partitionBy("year")`).
- Exercise: each customer's most recent order; month-over-month revenue
  change; save the clean order-facts table as Parquet partitioned by year.

### Phase 5 — Under the hood (weeks 5-6)
- Lazy evaluation in practice: `explain()`, the Spark UI at
  http://localhost:4040 while a job runs.
- Partitions, `repartition` vs `coalesce`, caching with `cache()`/`persist()`,
  broadcast joins.
- UDFs — and why built-in functions beat them.
- Exercise: compare query plans for a filtered join before/after reordering
  operations; time a query with and without caching.

### After that
- Structured Streaming basics (you can stream from a local folder of files).
- `pyspark.pandas` if you come from pandas.
- When you're ready for real scale: a free [Databricks Community Edition](https://www.databricks.com/try-databricks)
  account is the easiest way to try a real cluster.

## Good references

- [Official PySpark "Getting Started"](https://spark.apache.org/docs/latest/api/python/getting_started/index.html)
- [Spark SQL functions reference](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
- Book: *Learning Spark, 2nd Edition* (free PDF from Databricks)
