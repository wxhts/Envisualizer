import pandas as pd
from createWellIndex import createWellIndex


def createControls(path, standards=False):
    '''Creates a list of lists of tuples of coordination for the control wells

        Output: [hpe, zpe[, std]
    '''

    indexed_df = createWellIndex(path)

    hpe_indexed_df = indexed_df[indexed_df == 'HPE']
    zpe_indexed_df = indexed_df[indexed_df == 'ZPE']

    hpe_row_col = pd.DataFrame({'Row': hpe_indexed_df['Row'], 'Column': hpe_indexed_df['Column']})
    zpe_row_col = pd.DataFrame({'Row': zpe_indexed_df['Row'], 'Column': zpe_indexed_df['Column']})

    hpe_coords = []
    for i in hpe_row_col.itertuples():
        tup = (i[1], i[2])
        hpe_coords.append(tup)

    zpe_coords = []
    for j in zpe_row_col.itertuples():
        tup = (j[1], j[2])
        zpe_coords.append(tup)

    if standards:
        std_indexed_df = indexed_df[indexed_df == 'STD']
        std_row_col = pd.DataFrame({'Row': std_indexed_df['Row'], 'Column': std_indexed_df['Column']})

        std_coords = []
        for s in std_row_col.itertuples():
            tup = (s[1], s[2])
            std_coords.append(tup)

        return hpe_coords, zpe_coords, std_coords

    return hpe_coords, zpe_coords
