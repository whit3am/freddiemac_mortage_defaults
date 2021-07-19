if __name__ == '__main__':
    from utils.datapipe import DataPipeXY

    """
    Requires some human directory management.
    """
    data_pipe = DataPipeXY()
    data_pipe.build_x('../data')
    data_pipe.build_y('../data/')
    data_pipe.build_xy()
    data_pipe.export_csv(data_pipe.Xy, '../data/df_freddie_mac.csv')

    data_pipe_2005 = DataPipeXY()
    data_pipe_2005.build_x('../data/2005')
    data_pipe_2005.build_y('../data/2005')
    data_pipe_2005.build_xy()
    data_pipe_2005.export_csv(data_pipe_2005.Xy, '../data/df_freddie_mac_2005.csv')

