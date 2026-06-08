import pandas as pd

# load csv file
df = pd.read_csv("OnlineRetail.csv", encoding = "latin1")

# convert to usable data types, handle customerless observations
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["CustomerID"] = (
   df["CustomerID"]
   .fillna("UNKNOWN")                    # handle customerless observations
   .astype(str)                          # make datatype consistent for all obs. in col.
   .str.replace(r"\.0$", "", regex=True) # remove ".0" appended to float-converted fields
)

# create a column for each order's revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# in the dataset, cancelled orders are represented by invoiceNo's starting with "C..."
sales_df   = df[~df["InvoiceNo"].str.startswith("C")] # dataframe to store all orders
returns_df = df[df["InvoiceNo"].str.startswith("C")]  # dataframe to store cancelled orders

df.info()
sales_df.info()
returns_df.info()

assert len(sales_df.index) + len(returns_df.index) == len(df.index)