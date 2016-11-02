import pandas as pd
from createWellIndex import createWellIndex


def __build_list(frame):
    frame_coords = []
    for row in frame.itertuples():
        tup = (row[1], row[2])
        frame_coords.append(tup)
    return frame_coords


def createControls(path, standards=False):
    """Creates a list of lists of tuples of coordinates for the control wells

        Output: [hpe, zpe[, std]
    """

    indexed_df = createWellIndex(path)

    hpe_indexed_df = indexed_df[indexed_df['Type'] == 'HPE']
    zpe_indexed_df = indexed_df[indexed_df['Type'] == 'ZPE']

    hpe_row_col = pd.DataFrame({'Row': hpe_indexed_df['Row'], 'Column': hpe_indexed_df['Column']})
    zpe_row_col = pd.DataFrame({'Row': zpe_indexed_df['Row'], 'Column': zpe_indexed_df['Column']})

    hpe_coords = __build_list(hpe_row_col)
    zpe_coords = __build_list(zpe_row_col)

    if standards:
        std_indexed_df = indexed_df[indexed_df['Type'] == 'STD']
        std_row_col = pd.DataFrame({'Row': std_indexed_df['Row'], 'Column': std_indexed_df['Column']})

        std_coords = __build_list(std_row_col)

        return [hpe_coords, zpe_coords, std_coords]

    return [hpe_coords, zpe_coords]

