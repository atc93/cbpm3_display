import csv
import datetime
import io
import time

import pandas as pd
import psycopg2


def initialize():
    conn = psycopg2.connect(host="cesrpg.classe.cornell.edu",
                            port=5432,
                            database="actest",
                            user="atc93",
                            password="u8Lp0d")
    return conn


def get_online_data_from_db(conn):
    # ADD CHECK/ALARM IF DATA OLDER THAN X MINUTES FROM CURRENT TIME
    # MAKE SURE CBPMS IN SAME TRIGGER
    curr = conn.cursor()

    f = io.StringIO()
    curr.copy_expert("COPY (SELECT timestamp FROM cbpm3 ORDER BY timestamp DESC LIMIT 1) TO STDOUT WITH (FORMAT CSV)",
                     f)
    f.seek(0)
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        timestamp_last = row[0]
        # if int(row[1]) == 119:
        #     output_file.write(row[0] + ',' + row[2] + ',' + str(time.time()) + '\n')
        #     break
    # print(timestamp_last)

    f = io.StringIO()
    curr.copy_expert("COPY (SELECT * FROM cbpm3 WHERE timestamp ='" + str(timestamp_last) +
                     "') TO STDOUT WITH (FORMAT CSV, HEADER)",
                     f)
    f.seek(0)
    # reader = csv.reader(f, delimiter=',')
    # for row in reader:
    #     print(row[0])
        # if int(row[1]) == 119:
        #     output_file.write(row[0] + ',' + row[2] + ',' + str(time.time()) + '\n')
        #     break

    df = pd.read_csv(f)

    # print(df)

    return df

def get_offline_data_from_db(conn, date_start, date_end, time_start, time_end):
    # print(date_start, date_end, time_start, time_end)
    # timestamp_start = datetime.datetime.timestamp(
    #     datetime.datetime.strptime(date_start + ' ' + time_start, '%Y-%m-%d %H:%M'))
    # timestamp_end = datetime.datetime.timestamp(datetime.datetime.strptime(date_end + ' ' + time_end, '%Y-%m-%d %H:%M'))
    # print(datetime.datetime.strptime(date_start + ' ' + time_start, '%Y-%m-%d %H:%M'),
    #       timestamp_start,
    #       datetime.datetime.strptime(date_end + ' ' + time_end, '%Y-%m-%d %H:%M'),
    #       timestamp_end)

    timestamp_start = datetime.datetime.strptime(date_start + ' ' + time_start, '%Y-%m-%d %H:%M')
    timestamp_end = datetime.datetime.strptime(date_end + ' ' + time_end, '%Y-%m-%d %H:%M')

    df = pd.DataFrame()

    datetime_range = pd.date_range(start=timestamp_start, end=timestamp_end, freq='30Min')
    datetime_start = datetime_range[0:len(datetime_range)-1]
    datetime_end = datetime_range[1:len(datetime_range)]

    print(datetime_start, datetime_end)

    timestamp = timestamp_start

    for start, end in zip(datetime_start, datetime_end):
        print(start, end)
        # print(timestamp_end-timestamp_end)
        t1 = time.perf_counter()
        cur = conn.cursor()

        # https://towardsdatascience.com/optimizing-pandas-read-sql-for-postgres-f31cd7f707ab
        # https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
        f = io.StringIO()
        cur.copy_expert("COPY (SELECT * FROM cbpm3 WHERE timestamp<'" + str(end) + "' AND timestamp>='" + str(
            start) +
                        "' ORDER by timestamp) TO STDOUT WITH (FORMAT CSV, HEADER)", f)
        f.seek(0)
        df = pd.concat([df, pd.read_csv(f)])
        print(f'{1000 * (time.perf_counter() - t1):.2f} ms')
    # print(df.head())
    cur.close()

    # for i in range(120):
    #     df.loc[
    #         (
    #          (df['timestamp'] - df['timestamp'].shift(i) < 0.05)
    #          ),
    #         'timestamp'] = df['timestamp'].shift(i)
    #
    # df.to_csv('test.csv')
    #
    # df = df[:10000]

    # keep it here: multi-indexing
    # https: // www.somebits.com / ~nelson / pandas - multiindex - slice - demo.html
    # df = df.set_index(['timestamp', 'instr'])
    # print(df.head())

    return df

# https://strftime.org/
