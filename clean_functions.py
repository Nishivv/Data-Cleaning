import numpy as np
import pandas as pd




def missing(df):
  null_per = np.round(df.isnull().mean() * 100, 2)
  null_no = df.isnull().sum()
  result_df = pd.DataFrame({
      "col_name" : null_per.index,
      "%_missing_value": null_per.values,
      "num_missing_value": null_no.values
  })

  mask = result_df["num_missing_value"] > 0
  result_df = result_df[mask]
  result_df = result_df.sort_values(by = "num_missing_value",
                        ascending = False).reset_index(drop = True)
  return result_df



def out_info(df, threshold = 0.25):
  '''
  It provides outliers information for a dataframe.
  Input - DataFrame, threshold
  Output - it prints number of outliers in each column,
  with there percent and upper limit and lower limit values
  '''
  # identify numerical cols
  num_col = [col for col in df.columns if df[col].dtype != "object"]
  result_df = pd.DataFrame({
              "col_name": [],
              "skewness": [],
              "method":[],
              "num_out": [],
              "out_%": [],
              "uw": [],
              "lw": []
          })

  for col in num_col:
    if abs(df[col].skew()) > threshold:

      q1 = df[col].quantile(0.25)
      q3 = df[col].quantile(0.75)
      iqr = q3 - q1
      uw = q3 + 1.5 * iqr
      lw = q1 - 1.5 * iqr
      mask = (df[col] > uw) | (df[col] < lw)
      num_out = mask.sum()
      per_out = mask.mean()* 100

      temp_df = pd.DataFrame({
          "col_name": [col],
          "skewness": [round(df[col].skew(),2)],
          "method":["iqr"],
          "num_out": [num_out],
          "out_%": [per_out],
          "uw": [uw],
          "lw": [lw]
          })

      result_df = pd.concat([result_df, temp_df], ignore_index = False)

    else:
      x_bar = df[col].mean()
      x_std = df[col].std()
      uw = x_bar + 3 * x_std
      lw = x_bar - 3 * x_std

      mask = (df[col] > uw) | (df[col] < lw)
      num_out = mask.sum()
      per_out = mask.mean()* 100

      temp_df = pd.DataFrame({
          "col_name": [col],
          "skewness": [round(df[col].skew(),2)],
          "method":["z_score"],
          "num_out": [num_out],
          "out_%": [per_out],
          "uw": [uw],
          "lw": [lw]
          })

      result_df = pd.concat([result_df, temp_df], ignore_index = False)

  result_df = result_df.sort_values(by = "num_out", ascending = False).reset_index(drop = True)
  return result_df



def rem_out(df, col_list, method = "zscore"):
  df_new = df.copy()
  if method == "zscore":
    print("through zscore")
    for col in col_list:
      x_bar = df_new[col].mean()
      x_std = df_new[col].std()
      ub = x_bar + 3*x_std
      lb = x_bar - 3*x_std
      mask = (df_new[col] > ub) | (df_new[col] < lb)
      drop_index = df_new[mask].index
      df_new.drop(index = drop_index, inplace = True)
      print(f"for col {col} num outliers remove - {len(drop_index)}")
  elif method == "iqr":
    print("through iqr")
    for col in col_list:
      q1 = df[col].quantile(0.25)
      q3 = df[col].quantile(0.75)
      iqr = q3 - q1
      ub = q3 + 1.5 * iqr
      lb = q1 - 1.5 * iqr
      mask = (df_new[col] > ub) | (df_new[col] < lb)
      drop_index = df_new[mask].index
      df_new.drop(index = drop_index, inplace = True)
      print(f"for col {col} num outliers remove - {len(drop_index)}")

  else:
    print("enter valid method: zscore, iqr")

  return df_new