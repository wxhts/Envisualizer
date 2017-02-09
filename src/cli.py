import argparse
import csv
import pandas as pd
from createWellIndex import createWellIndex
from envisualize import EnVisualize

parser = argparse.ArgumentParser()
parser.add_argument('matrix', help='Total amount of wells in plate')  # Option
parser.add_argument('-s', '--standards', help='If there are reference agonists/antagonists in the control region', action='store_true', required=False) # Option
parser.add_argument('-o', '--outliers', help='Whether or not to remove points flagged as outliers in the control regions. Based on mean +/- 3SD', action='store_true', required=False) # Option
parser.add_argument('-a', '--annotate', help='Whether or not to annotate data with compound information', nargs=1, required=False) # Option
parser.add_argument('calculation', help='Perform percent inhibition or percent over basal calculation') # Option
parser.add_argument('controls', help='PATH to the controls template file')
parser.add_argument('barcodes', help='PATH to the barcode file')
parser.add_argument('data', help='PATH to the envision file')
#parser.add_argument('collection', help='PATH to collection file', action='store_false') # Option (T/N)
parser.add_argument('calcoutput', help='Name of calculation output file')
parser.add_argument('statistics', help='Name of the plate statistics output file')
args = parser.parse_args()

plate_stats = open(args.statistics + '.csv', 'wb')
csvwriter = csv.writer(plate_stats)
headers = ['Barcode', 'HPE CV', 'ZPE CV', 'Z-Prime', 'S/B', 'Reference %Inh']
csvwriter.writerow(headers)

index = createWellIndex(args.data)
collection = index
log = pd.read_csv(args.barcodes)
barcodes = set(collection['Barcode'])

list_inhibitions = []
for plate1 in log.itertuples():

    assayplate = plate1[1]
    compoundplate = plate1[2]
    subset = collection[(collection['Barcode'] == assayplate)]

    if args.standards and args.outliers:
        workit = EnVisualize(subset, args.controls, control_inh=True)
        stats = [assayplate, workit.CV('hpe', outlier=True), workit.CV('zpe', outlier=True), workit.zPrime(),
                 workit.signalToBackground(), workit.inhibitorControl()]
        csvwriter.writerow(stats)

        if args.annotate:
            if args.matrix == '384' and args.calculation == 'inhibition':
                workit.percentInhibition(384)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '1536' and args.calculation == 'inhibition':
                workit.percentInhibition(1536)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '384' and args.calculation == 'basal':
                workit.percentOverBasal(384)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '1536' and args.calculation == 'basal':
                workit.percentOverBasal(1536)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

        else:
            if args.matrix == '384' and args.calculation == 'inhibition':
                list_inhibitions.append(workit.percentInhibition(384))

            elif args.matrix == '1536' and args.calculation == 'inhibition':
                list_inhibitions.append(workit.percentInhibition(1536))

            elif args.matrix == '384' and args.calculation == 'basal':
                list_inhibitions.append(workit.percentOverBasal(384))

            elif args.matrix == '1536' and args.calculation == 'basal':
                list_inhibitions.append(workit.percentOverBasal(1536))

    elif args.standards:
        workit = EnVisualize(subset, args.controls, control_inh=True)
        stats = [assayplate, workit.CV('hpe'), workit.CV('zpe'), workit.zPrime(),
                 workit.signalToBackground(), workit.inhibitorControl()]
        csvwriter.writerow(stats)

        if args.annotate:
            if args.matrix == '384' and args.calculation == 'inhibition':
                workit.percentInhibition(384)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '1536' and args.calculation == 'inhibition':
                workit.percentInhibition(1536)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '384' and args.calculation == 'basal':
                workit.percentOverBasal(384)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '1536' and args.calculation == 'basal':
                workit.percentOverBasal(1536)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

        else:
            if args.matrix == '384' and args.calculation == 'inhibition':
                list_inhibitions.append(workit.percentInhibition(384))

            elif args.matrix == '1536' and args.calculation == 'inhibition':
                list_inhibitions.append(workit.percentInhibition(1536))

            elif args.matrix == '384' and args.calculation == 'basal':
                list_inhibitions.append(workit.percentOverBasal(384))

            elif args.matrix == '1536' and args.calculation == 'basal':
                list_inhibitions.append(workit.percentOverBasal(1536))

    elif args.outliers:
        workit = EnVisualize(subset, args.controls)
        stats = [assayplate, workit.CV('hpe', outlier=True), workit.CV('zpe', outlier=True), workit.zPrime(),
                 workit.signalToBackground(), ' ']
        csvwriter.writerow(stats)

        if args.annotate:
            if args.matrix == '384' and args.calculation == 'inhibition':
                workit.percentInhibition(384)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '1536' and args.calculation == 'inhibition':
                workit.percentInhibition(1536)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '384' and args.calculation == 'basal':
                workit.percentOverBasal(384)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '1536' and args.calculation == 'basal':
                workit.percentOverBasal(1536)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

        else:
            if args.matrix == '384' and args.calculation == 'inhibition':
                list_inhibitions.append(workit.percentInhibition(384))

            elif args.matrix == '1536' and args.calculation == 'inhibition':
                list_inhibitions.append(workit.percentInhibition(1536))

            elif args.matrix == '384' and args.calculation == 'basal':
                list_inhibitions.append(workit.percentOverBasal(384))

            elif args.matrix == '1536' and args.calculation == 'basal':
                list_inhibitions.append(workit.percentOverBasal(1536))

    else:
        workit = EnVisualize(subset, args.controls)
        stats = [assayplate, workit.CV('hpe'), workit.CV('zpe'), workit.zPrime(),
                 workit.signalToBackground(), ' ']
        csvwriter.writerow(stats)

        if args.annotate:
            if args.matrix == '384' and args.calculation == 'inhibition':
                workit.percentInhibition(384)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '1536' and args.calculation == 'inhibition':
                workit.percentInhibition(1536)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '384' and args.calculation == 'basal':
                workit.percentOverBasal(384)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

            elif args.matrix == '1536' and args.calculation == 'basal':
                workit.percentOverBasal(1536)
                compound_add = workit.compoundAdder(args.annotate, compoundplate)
                list_inhibitions.append(compound_add)

        else:
            if args.matrix == '384' and args.calculation == 'inhibition':
                list_inhibitions.append(workit.percentInhibition(384))

            elif args.matrix == '1536' and args.calculation == 'inhibition':
                list_inhibitions.append(workit.percentInhibition(1536))

            elif args.matrix == '384' and args.calculation == 'basal':
                list_inhibitions.append(workit.percentOverBasal(384))

            elif args.matrix == '1536' and args.calculation == 'basal':
                list_inhibitions.append(workit.percentOverBasal(1536))

all_inhibitions = pd.concat(list_inhibitions)
all_inhibitions.to_csv(args.calcoutput + '.csv', index=False)
plate_stats.close()