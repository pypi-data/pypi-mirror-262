# from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import re
import json
import requests
from concurrent.futures import ThreadPoolExecutor





@pd.api.extensions.register_dataframe_accessor("ext")
class Extend:
    
    def __init__(self, pandas_obj):
        self._check(pandas_obj)
        self._obj = pandas_obj
        
    
    @staticmethod
    def _check(obj):
        if isinstance(obj, pd.core.frame.DataFrame) == False:
            raise AttributeError("caniform methods are only applied to objects of class 'pandas.core.frame.DataFrame'")
        
            
    @property
    def nrow(self):
        return self._obj.shape[0]
    
    @property
    def ncol(self):
        return self._obj.shape[1]
    
    
    def cols(self, *args):
        df = self._obj
        ret = df[[*args]]
        return ret
    
    
    def cols_like(self, *args):
        def rematch(str_list, search_for):
            ret_bool = []
            for s in str_list:
                if re.findall(search_for, s) == []:
                    ret_bool.append(False)
                else:
                    ret_bool.append(True)
            ret = np.array(str_list)[np.array(ret_bool)].tolist()
            return ret
        df = self._obj
        clist = df.columns.tolist()
        new_cols = []
        for f in [*args]:
            tmp = rematch(clist, f)
            new_cols.extend(tmp)
        ret = df[new_cols]
        return ret
    
    
    def cols_paste(self, *args, sep = "-", new_name = "auto", drop_ori = True, show_verbose = True):
        df = self._obj
        idx = df.index
        df = df.reset_index(drop = True)
        join_cols = [*args]
        if new_name == "auto":
            new_name = "_".join(join_cols)
        tmp_df = df[join_cols].applymap(str)
        new_col = []
        if show_verbose:
            print(f"Pasting columns {', '.join(join_cols)} using sep = '{sep}' into new column '{new_name}'")
        for r in range(0, tmp_df.shape[0]):
            tmp = sep.join(tmp_df.loc[r].tolist())
            new_col.append(tmp)
        ret = df.assign(auto = new_col).rename(columns = {"auto": new_name})
        if drop_ori:
            ret = ret.drop(join_cols, axis = 1)
        ret.index = idx
        return ret
    
    
    def cols_split(self, split_col, split_by = "-", new_prefix = "new_", drop_ori = True):
        df = self._obj
        idx = df.index
        df = df.reset_index(drop = True)
        tmp_df_lst = []
        for r in range(0, df.shape[0]):
            tmp_split = str(df.at[r, split_col]).split(split_by)
            tmp_df_lst.append(tmp_split)
        tmp_df = pd.DataFrame(tmp_df_lst)
        tmp_df.columns = [f"{new_prefix}{c+1}" for c in range(0, tmp_df.shape[1])]
        if drop_ori:
            ret = pd.concat([df, tmp_df], axis = 1).drop(split_col, axis = 1)
        else:
            ret = pd.concat([df, tmp_df], axis = 1)
        ret.index = idx
        return ret
    
    
    def group(self, *args, to_index = False):
        df = self._obj
        ret = df.groupby([*args], as_index = to_index)
        return ret

    
    def diff(self, *args, n_diff = 1, drop_ori = True):
        df = self._obj
        idx = df.index
        df = df.reset_index(drop = True)
        if n_diff >= df.shape[0] + 1:
            raise ValueError(f"The given 'n_diff' value of {n_diff} cannot exceed the DataFrame's number of rows ({df.shape[0]})")
        use_cols = [*args]
        ret_cols = []
        for c in use_cols:
            tmp_diff = np.diff(df[c], n_diff).tolist()
            for n in range(0, n_diff):
                tmp_diff[:0] = [np.NaN]
            ret_cols.append(pd.Series(tmp_diff))
        ret_df = pd.concat(ret_cols, axis = 1)
        ret_df.columns = use_cols
        if drop_ori:
            ret = df.drop(use_cols, axis = 1)
        else:
            ret = df
        ret = pd.concat([ret, ret_df], axis = 1)
        ret.index = idx
        return ret
    
    
    def count(self, count_column, add_prop = True, round_to = 3, is_categorical = True, n_bins = 10, low_to_high = False):
        df = self._obj
        if is_categorical:
            ret = (
                df
                .groupby(count_column, as_index = False)
                .agg(n = (count_column, "count"))
                .sort_values("n", ascending = low_to_high)
            )
            if add_prop:
                ret["prop"] = np.round(ret.n / df.shape[0], round_to)
        else:
            ret = (
                pd.DataFrame({"bin": pd.cut(df[count_column], bins = n_bins)})
                .groupby("bin", as_index = False)
                .agg(n = ("bin", "count"))
                .sort_values("n", ascending = low_to_high)
            )
            if add_prop:
                ret["prop"] = np.round(ret.n / df.shape[0], round_to)
        ret = ret.reset_index(drop = True)
        return ret
    
    
    # def lm(self, x, y, ret = "rsquared", round_to = 3, show_verbose = True):
    #     df = self._obj
    #     x_name = x
    #     y_name = y
    #     X = df[x]
    #     y = df[y]
    #     if type(X) != np.ndarray:
    #         X = np.array(X).reshape((-1, 1))
    #     if type(y) != np.ndarray:
    #         y = np.array(y).reshape((-1, 1))
    #     mod = LinearRegression().fit(X, y)
    #     ret = ret.lower()
    #     if ret not in ["rsquared", "coef", "intercept"]:
    #         raise TypeError("Arg 'ret' must be one of 'rsquared', 'coef', or 'intercept'")
    #     if ret == "rsquared":
    #         rsquared = np.round(mod.score(X, y), round_to)
    #         if show_verbose:
    #             print(f"The change in '{y_name}' is ~{np.round(rsquared*100, round_to)}% explained by a change in '{x_name}'")
    #         return rsquared
    #     elif ret == "coef":
    #         coef = np.round(mod.coef_[0][0], round_to)
    #         if show_verbose:
    #             print(f"For every incremental change in '{x_name}', '{y_name}' changes by {coef}")
    #         return coef
    #     else:
    #         intercept = np.round(mod.intercept_[0], round_to)
    #         if show_verbose:
    #             print(f"With a y-intercept of {intercept}, '{y_name}' is independent of '{x_name}' when it is {intercept}")
    #         return intercept
        
    
    def to_month(self, col, use_abbr = True):
        df = self._obj
        if use_abbr:
            month_index = {
                1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
                5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
                9: "Sep", 10:"Oct", 11:"Nov", 12:"Dec"
            }
        else:
            month_index = {
                1: "January", 2: "February", 3: "March", 4: "April",
                5: "May", 6: "June", 7: "July", 8: "August",
                9: "September", 10:"October", 11:"November", 12:"December"
            }
        ret_df = df.copy()
        ret_df[col] = ret_df[col].astype("int64", errors = "ignore")
        ret_df = ret_df.replace({col: month_index})
        return ret_df

    
    def train_valid_test(self, tvt_split = [60, 20, 20], reset_the_index = True):
        df = self._obj
        if sum(tvt_split) != 100:
            raise Exception("The sum of train/valid/test split (tvt_split) must equal 100")
        train_valid = df.sample(frac = (tvt_split[0] + tvt_split[1]) / 100)
        test = pd.concat([df, train_valid, train_valid]).drop_duplicates(keep = False)
        train = train_valid.sample(frac = tvt_split[0]/100)
        valid = pd.concat([train_valid, train, train]).drop_duplicates(keep = False)
        if reset_the_index:
            train = train.reset_index(drop = True)
            valid = valid.reset_index(drop = True)
            test = test.reset_index(drop = True)
        return train, valid, test


    def apply_except(self, *args, func, **kwargs):
        ret_df = self._obj.copy()
        col_rem_lst = [*args]
        col_keep_lst = list(set(ret_df.columns) - set(col_rem_lst))
        ret_df[col_keep_lst] = ret_df[col_keep_lst].apply(func, **kwargs)
        return ret_df


    def __make_dict_list(self, _df):
        _df = _df.reset_index(drop = True)
        return list(_df.T.to_dict().values())
    
    def __post_request(self, _payload_dict, _url, _headers):
        payload_dict = json.dumps(_payload_dict)
        return requests.post(
            url = _url, 
            headers = _headers,
            data = payload_dict
        )
    
    def post(self, endpoint, headers = None, n_max_workers = 10):
        df = self._obj
        headers = {"Accept-Charset": "UTF-8"} if headers is None else headers
        payload_dict_list = self.__make_dict_list(df)
        processes = []
        with ThreadPoolExecutor(max_workers = n_max_workers) as executor:
            for pdl in payload_dict_list:
                processes.append(executor.submit(self.__post_request, _payload_dict = pdl, _url = endpoint, _headers = headers))


    def split_row(self, split_column, split_by):
        df = self._obj
        tmp = df[df[split_column].str.contains(split_by)]
        ret = df.drop(tmp.index)
        tmp = tmp.reset_index(drop = True)
        for r in range(tmp.shape[0]):
            tmp.at[r, split_column] = tmp.at[r, split_column].split(split_by)
        tmp = tmp.explode(split_column)
        return pd.concat([ret, tmp]).reset_index(drop = True)
