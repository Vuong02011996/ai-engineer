import polars as pl

def data_ecg():
    pl.Config.set_tbl_cols(100) # extract ... in column
    pl.Config.set_tbl_rows(100) # extract ... in row
    all_data = pl.read_parquet(
        "/home/server2/Desktop/Vuong/Project/octomed-octodx-ai-ai-holter_library/study-377082-1.parquet")

    print(all_data.columns) # print all column    # ("['EPOCH', 'CHANNEL', 'BEAT', 'BEAT_TYPE', 'EVENT', 'QT', 'QTC', 'ST_LEVEL', 'ST_SLOPE', 'P_ONSET', 'P_PEAK', "
    #  "'P_OFFSET', 'P_AMPLITUDE', 'T_ONSET', 'T_PEAK', 'T_OFFSET', 'T_AMPLITUDE', 'QRS_ONSET', 'QRS_OFFSET', 'FILE_INDEX',"
    #  " 'RR_HEATMAP', 'RR_HEATMAP_REVIEWED', 'PVC_TEMPLATE', 'PVC_TEMPLATE_REVIEWED']")

    # Select column want to see
    data_selected_columns = all_data.select(['BEAT', 'BEAT_TYPE', 'EVENT', 'QT', 'QTC', 'ST_LEVEL', 'ST_SLOPE', 'P_ONSET', 'P_PEAK'])

    # Select columns from the 10th to the 100th (Polars uses zero-based indexing)
    data_selected_columns = data_selected_columns[9:100, :]  # Select columns from index 9 to 99

    with pl.Config(fmt_str_lengths=1000, tbl_width_chars=1000): # extend column width
        print(data_selected_columns)

if __name__ == '__main__':
    data_ecg()