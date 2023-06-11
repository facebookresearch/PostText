# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
import csv
import pandas as pd

from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle
from langchain.docstore.document import Document
from datetime import datetime

def verbalize(episodes):
    all_text = []
    all_meta = []
    id2epi = {}
    for i, dt, desc, details, tt in zip(episodes['id'], episodes['date'], episodes['desc'], episodes['details'], episodes['time']):
        l0 = dt[0:10]
        l1 = dt[11:]
        text = 'On ' + dt + ' ' + tt
        print(text)
        metadata = {'source': i}
        all_text.append(text)
        all_meta.append(metadata)
        id2epi[i] = text

    return all_text, all_meta, id2epi

def main(argv):

    episodes = pd.read_csv(argv[0])
    textdata, metadata, id2epi = verbalize(episodes)
    embeddings = OpenAIEmbeddings()

    docsearch = FAISS.from_texts(textdata, embeddings, metadatas=metadata)

    # Save vectorstore
    with open(argv[1], "wb") as f:
        pickle.dump(docsearch, f)



if __name__ == "__main__":
    main(sys.argv[1:])
