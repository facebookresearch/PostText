# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import pandas as pd
import sys, getopt
from datetime import datetime
import os

def main(argv):
    filename = argv[0]
    try:
        opts, args = getopt.getopt(argv[1:],"hr:t:o:",["positions=", "timecol=", "output="])
    except getopt.GetoptError:
        print('dd_cleaner -r <column positions> -t <column name,newcol1,newcol2> -o <outputfile>')
        sys.exit(2)

    column_pos_list = []
    timecol = "" 
    df = pd.read_csv(filename)
    outputfilename = ""
    for opt, arg in opts:
        if opt == '-h':
            print()
            print('dd_cleaner <filename> -r <column positions> -t <column name> -o <outputfilename>')
            print()
            print('-r   list of positional columns to remove comman separated. e.g., "0,2"')
            print('-t   formats the column <column name> into <col1> and <col2> e.g, 2019-04-19T04:37:00 becomes 2019/04/13 and 04:37:00')
            print('-o   outputfilename')
            sys.exit()
        elif opt == '-r':
            tem = arg.split(",")
            column_pos_list = list(map(lambda x: int(x), tem))
            df=df.drop(df.columns[column_pos_list], axis=1)
        elif opt == '-t':
            temlist = arg.split(",")
            targetcol = temlist[0]
            newcol1 = temlist[1]
            newcol2 = temlist[2]
            datelist = []
            timelist = []
            for t in df[targetcol]:
                #split after YYYY-MM-DD
                l0 = t[0:10]
                l1 = t[11:]
                d_obj = datetime.strptime(l0, '%Y-%m-%d')
                datelist.append(d_obj.strftime('%Y/%m/%d'))
                timelist.append(l1.strip())
            df.drop(targetcol, axis=1)
            df[newcol1] = datelist
            df[newcol2] = timelist
        elif opt == '-o':
            outputfilename = arg

    df.to_csv(outputfilename, index=False)

if __name__ == "__main__":
    main(sys.argv[1:])
