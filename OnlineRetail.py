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

# I want to know revenue information, but the data contains P and Q values for cancelled orders.
# In the dataset, cancelled orders are represented by invoiceNo's starting with "C..."
sales_df   = df[~df["InvoiceNo"].str.startswith("C")] # dataframe to store all orders
returns_df = df[df["InvoiceNo"].str.startswith("C")]  # dataframe to store cancelled orders

# visually examine the table metadata to check everything looks okay
# df.info()
sales_df.info()
# returns_df.info()

# sanity check that the size of both subtables equals the size of the original
assert len(sales_df.index) + len(returns_df.index) == len(df.index)

# generate summary statistics for the dataframe
print(f"\n{sales_df.describe()}")
# FINDINGS:
# 1. There are negative quantities
#       Upon visual inspection in excel, the descriptions for such entries
#       show that negative quanities are literally showing quantities out, 
#       for reasons like damaged goods or correcting inventory data entry errors.
#          a. When damage:
#                Q < 0, P = 0
#          b. When cancelled order:
#                Q < 0, P > 0
# 2. There are two rows with negative prices, Q = 1
#       Bad debt adjustment
# 3. There are samples with Q = -1, StockCode = S, and "Cancelled" order status
#       Since the customer is already in the door, perhaps this is a merchandising cost?


# CALCULATIONS

# total revenue: $10 Million
rev = sales_df["Revenue"].sum(skipna=False)
print(f"\nTotal revenue is: ${rev:,.2f}")

# revenue per product: top performers only sold $1000 each, suggesting highly seasonal buying
itemSales = sales_df.groupby(["StockCode", "Description"], as_index=False)["Revenue"].sum()
itemSales["Revenue"] = itemSales["Revenue"].map("${:,.2f}".format)
# TODO: Add percentage of total revenue col
print(f"\nRevenue per Item:")
print(f"\n{itemSales.sort_values(by="Revenue")}")

# revenue per location: UK is main market
locSales = sales_df.groupby(["Country"], as_index=False)["Revenue"].sum()
locSales["Revenue"] = locSales["Revenue"].map("${:,.2f}".format)
# TODO: Add percentage of total revenue col
print(f"\nRevenue per Item:")
print(f"\n{locSales.sort_values(by="Revenue")}")

# most popular products by location
itemsByLoc = sales_df.groupby(["StockCode", "Description", "Country"], as_index=False)["Revenue"].sum()
itemsByLoc["Revenue"] = itemsByLoc["Revenue"].map("${:,.2f}".format)
print(f"\nRevenue by Item and Location:")
print(f"\n{itemsByLoc.sort_values(by="Revenue")}")

# limitation: cannot determine category...