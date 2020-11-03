import re
from random import uniform
import pandas as pd

def position(df):
    kx = 20
    ky = 10

    # PERFORMANCE DISCUSSION OF PANDAS
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/enhancingperf.html
    # df.eval('xpos=(top_in+bot_in-(top_out+bot_out))/(top_in+bot_in+top_out+bot_out)*'+str(kx), inplace=True)
    # df.eval('ypos=(top_in+top_out-(bot_in+bot_out))/(top_in+bot_in+top_out+bot_out)*'+str(ky), inplace=True)
    df['xpos'] = df['top_in'].apply(lambda x: uniform(-1, 1))
    df['ypos'] = df['top_in'].apply(lambda x: uniform(-1, 1))

    # print(df)

    return df


def detloc_detid_mapping(df):
    det_lines = []
    mapping_file_name = ('/nfs/cesr/online/instr/CBPM/config/BPM_DET_params.cfg')
    with open(mapping_file_name, 'r') as mapping_file:
        for line in mapping_file:
            if re.match('.DETECTOR_LOCATION', line) or re.match('.DETEC_ID_ELE ', line):
                det_lines.append(line.split()[1])

    it = iter(det_lines)
    det_dict = dict(zip(it, it))

    df['instr_idx'] = df['instr'].map(det_dict).astype(
        'int64')  # need to int conversion, otherwise string and therefore do not bod well with sorting

    # print(df.dtypes)

    df.sort_values(by='instr_idx', ascending=True, inplace=True)

    print(df.head())

    return df


def decimate(df):
    # df.set_index('timestamp')
    resample_logic = {'instr': 'last',
                      'top_in': 'mean',
                      'top_out': 'mean',
                      'bot_in': 'mean',
                      'bot_out': 'mean',
                      'xpos': 'mean',
                      'ypos': 'mean'}

    df_final =pd.DataFrame()

    # df.set_index('timestamp', inplace=True)

    df['timestamp'] = df['timestamp'].astype('datetime64')
    # df['timestamp'] = pd.to_datetime(df['timestamp'])
    print(df.dtypes)

    for instr in df['instr'].unique():
        df_tmp = df[df['instr'] == instr]
        # print(df_tmp.head())
        df_tmp = df_tmp.resample('1Min', on='timestamp').apply(resample_logic)
        # print(df_tmp.head())
        df_final = pd.concat([df_final, df_tmp])
        # break

    df_final.reset_index(inplace=True)

    return df_final
