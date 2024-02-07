from __future__ import print_function
from DIRAC.Core.Base.Script import parseCommandLine
from LHCbDIRAC.ProductionManagementSystem.Client.ProductionRequestClient import ProductionRequestClient
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

import argparse


def get_prodID(requestID):
    '''returns a list of productionIDs for requestID
    '''
    parseCommandLine()
    pc = ProductionRequestClient()
    tc = TransformationClient()
    prods = pc.getProductionList(requestID)['Value']
    simprods = filter(lambda prod: 'Simulation' in tc.getTransformation(prod)['Value']['Type'], prods)
    return list(simprods)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='list of requestIDs')
    parser.add_argument('requestIDs', type=int, nargs='+', help='')

    args = parser.parse_args()

    prodIDs = []
    for requestID in args.requestIDs:
        prodIDs.extend(get_prodID(requestID))

    output = ''
    for prodID in prodIDs:
        output += f',{prodID}'

    print(output[1:])
