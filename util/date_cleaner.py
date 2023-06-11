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
    df = pd.read_csv(filename)
    targetcol = argv[1]
    newcol = argv[2]
    outputfilename = argv[3]
    datelist = []
    for t in df[targetcol]:
        d_obj = datetime.strptime(t, '%m/%d/%Y')
        datelist.append(d_obj.strftime('%Y/%m/%d'))
    df.drop(targetcol, axis=1)
    df[newcol] = datelist

    df.to_csv(outputfilename, index=False)

if __name__ == "__main__":
    main(sys.argv[1:])
