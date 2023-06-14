/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
     
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
