import pandas as pd

# load csv file
df = pd.read_csv("OnlineRetail.csv", encoding = "latin1")
df.info()

# convert to usable data types, handle customerless observations
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["CustomerID"] = (
   df["CustomerID"]
   .fillna("UNKNOWN")                    # handle customerless observations
   .astype(str)                          # make datatype consistent for all obs. in col.
   .str.replace(r"\.0$", "", regex=True) # remove ".0" appended to float-converted fields
)

df.info()

# while addressing the missing customerIDs, I got an error while trying to convert them to integers
# saying that one of the customers is called "C...". this should not be the case

# get an array of indexes where customerID starts with C
cIndexes = df['CustomerID'].str.startswith('C', na=False)
print(df[cIndexes].head()) # print rows where customerID starts with C

# there is no customerIDs that start with C...
# assuming i made a typo in the code that initially generated the error