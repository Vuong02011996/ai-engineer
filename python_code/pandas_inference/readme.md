# 10 minutes to pandas
## Object creation
+ **Series**: creating a series by passing a list of values, default index.
+ **DataFrame**: 
  + creating a data frame by passing a `numpy array`, index and labeled columns.
  + creating a data frame by passing a `dict` of objects that can be converted to series-like.
  + The columns of the resulting DataFrame have different dtypes. `df.dtypes`

## Viewing data
+ `df.head()`: View the `top` rows of the frame
+ `df.tail(2)`: View the `bottom` rows of the frame
+ `df.index`: Display the index
+ `df.columns`: Display the column
+ `df.to_numpy()`: **DataFrame.to_numpy()**
  + Numpy arrays have one dtype for the entire array, while pandas DataFrame has one dtype per column.
  + When you call df.to_numpy(), pandas will find the NumPy type that can `hold all` of the dtypes in the DataFrame.
  + This may end up being `object`, which requires casting every value to Python object.(expensive operation)
  + `df.to_numpy()` does not include the index or column labels in the output.
+ `df.describe()`: shows a quick statistic summary of your data.
+ `df.T`: Transposing your data.
+ `df.sort_index()`: sorting by an axis 
+ `df.sort_values()`: sorting by values

## Selection
While standard Python/Numpy expressions for selecting and setting are intuitive and come in handy for interactive work,
for production code, we recommended the optimized pandas **data access methods**: `.at, .iat, .loc, .iloc`. 

### Getting
+ `df.A or df["A"]`: selecting a single column (which yields a Series)
+ `[:]`: selecting slices the rows.

### Selection by label
+ `df.loc[dates[0]]`: for getting a cross-section using a label.
+ `df.loc[:, ["A", "B"]]`: selecting on a multi-axis by label.
+ `df.loc["20130102":"20130104", ["A", "B"]]`: showing label slicing, both endpoints are included.
+ `df.loc["20130102", ["A", "B"]]`: reduction in the dimensions of the returned object.
+ `df.loc[dates[0], "A"]`: for getting a scalar value.
+ `df.at[dates[0], "A"]`: for getting fast access to a scalar.

### Selection by position
+ `df.iloc[3]`: select via the position of the passed integers.
+ `df.iloc[3:5, 0:2]`: by integer slices, acting similar to Numpy/Python.
+ `df.iloc[[1, 2, 4], [0, 2]]`: by lists of integer position locations, similar to the Numpy/Python style.
+ `df.iloc[1, 1]`: for getting a value explicitly.
+ `df.iat[1, 1]`: for getting fast access to a scalar.

### Boolean indexing
+ `df[df["A"] > 0]`: Using a single column's values to select data.
+ `df[df > 0]`: Selecting values from a DataFrame where a boolean condition is met.
+ Using the `isin()` method for filtering:
  + `df2["E"] = ["one", "one", "two", "three", "four", "three"]`
  + `df2[df2["E"].isin(["two", "four"])]`

### Setting
+ Setting a new column automatically aligns the data by the indexes
  + `s1 = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range("20130102", periods=6))`
  + `df["F"] = s1`
+ `df.at[dates[0], "A"] = 0`: setting a values by label
+ `df.iat[0, 1] = 0`: setting a values by position.
+ `df.loc[:, "D"] = np.array([5] * len(df))`: setting by passing with a Numpy array.
+ A where operation with setting.
  + `df2 = df.copy()`
  + `df2[df2 > 0] = -df2`

# Ref
+ https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html