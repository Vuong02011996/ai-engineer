# 10 minutes to pandas
## Object creation
Ref [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/dsintro.html#series)
+ **Series**: creating a series by passing a list of values, default index.
  + Series is a one-dimensional labeled array capable of holding any data type (integers, strings, floating point numbers, Python objects, etc.).
  + Syntax: `s = pd.Series(data, index=index)`
  + data can be many different things:
    + a python dict
      + `d = {"b": 1, "a": 0, "c": 2}
         pd.Series(d)`
    + an ndarray: `s = pd.Series(np.random.randn(5), index=["a", "b", "c", "d", "e"])`
    + a scalar value(like 5): `pd.Series(5.0, index=["a", "b", "c", "d", "e"])`
  + Series acts very similarly to a ndarray, and is a valid argument to most NumPy functions.
  + When working with raw NumPy arrays, **looping through value-by-value** is usually **not necessary**. The same is true when working with Series in pandas
  + 


+ **DataFrame**: 
  + DataFrame is a 2-dimensional labeled data structure with columns of potentially different types.
  You can think of it like a spreadsheet or SQL table, or a dict of Series objects.
    + creating a data frame by passing a `numpy array`, index and labeled columns.
    + creating a data frame by passing a `dict` of objects that can be converted to series-like.
    + The columns of the resulting DataFrame have different dtypes. `df.dtypes`

+ **Conclusion**: Series table one column, DataFrame table two column.


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

## Missing data
Pandas primarily uses the value `np.nan` to represent missing data. It is by default not included in computations.
+ Reindexing allows you to change/add/delete the index on a specified axis. This returns a copy of the data.
  + `df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ["E"])`
  + `df1.loc[dates[0] : dates[1], "E"] = 1`

+ `df1.dropna(how="any")`: to drop any rows that have missing data.
+ `df1.fillna(value=5)`: filling missing data
+ `pd.isna(df1)`: to get the boolean mask where values are nan.


## Operations
### Stats
Operations in general exclude missing data.
+ `df.mean()`
+ `df.mean(1)`: same operation on the other axis.
+ Operating with objects that have different dimensionality and need alignment. In addition, pandas automatically broadcasts along the specified dimension.
  + `s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)`
  + `df.sub(s, axis="index")`

### Apply
Applying functions to the data
+ `df.apply(np.cumsum)`
+ `df.apply(lambda x: x.max() - x.min())`

### Histogramming
+ Histogram
  + `s = pd.Series(np.random.randint(0, 7, size=10))`
  + `s.value_counts()`

### String Methods
+ Series is equipped with a set of string processing methods in the str attribute that make it easy to operate on each element of the array, as in the code snippet below
  + `s = pd.Series(["A", "B", "C", "Aaba", "Baca", np.nan, "CABA", "dog", "cat"])`
  + `s.str.lower()`

## Merge
### Concat
### Join

## Grouping
## Reshaping

## Time series
## Categoricals


## Plotting
## Getting data in/out


# Ref
+ https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html