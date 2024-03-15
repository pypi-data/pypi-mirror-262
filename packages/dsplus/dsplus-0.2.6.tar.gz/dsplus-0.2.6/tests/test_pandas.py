#region Library

#%%
import pandas as pd
import numpy as np
import dsplus as ds

#%%
import importlib
importlib.reload(ds)

#endregion -----------------------------------------------------------------------------------------
#region Set Operations

#%%
def test_set_union_1():
    v1 = [0,1,2]
    v2 = [1,2,3]

    v = ds.set_union(v1, v2).to_list()

    assert v == [0,1,2,3]

def test_set_union_2():
    v1 = [0,1,2]
    v2 = [3,4]

    v = ds.set_union(v1, v2).to_list()

    assert v == [0,1,2,3,4]

def test_set_intersection_1():
    v1 = [0,1,2]
    v2 = [1,2,3]

    v = ds.set_intersection(v1, v2).to_list()

    assert v == [1,2]

def test_set_intersection_2():
    v1 = [0,1,2]
    v2 = [3,4]

    v = ds.set_intersection(v1, v2).to_list()

    assert v == []

def test_set_diff_1():
    v1 = [0,1,2]
    v2 = [1,2,3]

    v = ds.set_diff(v1, v2).to_list()

    assert v == [0]

def test_set_diff_2():
    v1 = [0,1,2]
    v2 = [3,4]

    v = ds.set_diff(v1, v2).to_list()

    assert v == [0,1,2]

#endregion -----------------------------------------------------------------------------------------
#region Slice

#%%
def test_pd_select():
    df = pd.DataFrame(columns = ['v'+str(_) for _ in range(21)])

    df_select = df.pipe(ds.pd_select, 'str.startswith("v2"), *, -str.startswith("v1"), -v8')

    assert df_select.columns.tolist() == ['v2', 'v20', 'v0', 'v3', 'v4', 'v5', 'v6', 'v7', 'v9']

#%%
def test_pd_select_drop():
    df = pd.DataFrame(columns = ['v'+str(_) for _ in range(21)])

    df_select = df.pipe(ds.pd_select, '-:v5, -v8:')

    assert df_select.columns.tolist() == ['v6', 'v7']

#endregion -----------------------------------------------------------------------------------------
#region Others

#%%
def test_pd_definition():
    df_ds = ds.pd_dataframe(x = [1,2,3],
                            y = 4)
    df_pd = pd.DataFrame(dict(x = [1,2,3],
                              y = 4))
    
    assert df_pd.equals(df_ds)

#%%
def test_pd_set_colnames_1():
    df = pd.DataFrame(columns = ['c1', 'c2', 'c3'])

    df = ds.pd_set_colnames(df, ['v1', 'v2', 'v3'])

    assert df.columns.tolist() == ['v1', 'v2', 'v3']

def test_pd_set_colnames_2():
    df = pd.DataFrame(columns = ['c1', 'c2', 'c3'])

    df = ds.pd_set_colnames(df, ['v1', 'v2', 'v3', 'v4'])

    assert df.columns.tolist() == ['v1', 'v2', 'v3']

def test_pd_set_colnames_3():
    df = pd.DataFrame(columns = ['c1', 'c2', 'c3'])

    df = ds.pd_set_colnames(df, col_names=['v1', 'v2'])

    assert df.columns.tolist() == ['v1', 'v2', '_2']

def test_pd_split_column_1():
    df = ds.pd_dataframe(sn = [1,2,3],
                         c = ['a_b', 'mm_nnn', 'x_y'])
    
    df_split = ds.pd_split_column(df, '_', column_original='c', columns_new=['c1', 'c2'])

    df_split_check = pd.concat([df,
                                df['c'].str.split('_', expand=True).set_axis(['c1', 'c2'], axis=1)],
                                axis=1)
    
    assert df_split.equals(df_split_check)

#endregion -----------------------------------------------------------------------------------------
