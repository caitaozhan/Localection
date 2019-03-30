'''
Some useful utilities
'''
import json
import numpy as np
import random

def read_config(filename):
    '''Read json file into json object
    '''
    with open(filename, 'r') as handle:
        dictdump = json.loads(handle.read(), encoding='utf-8')
    return dictdump


def ordered_insert(sensor_index, index):
    '''Insert index into sensor_index and guarantee sensor_index is sorted from small to large.
    Attributes:
        sensor_index (list)
        index (int)
    '''
    size = len(sensor_index)
    for i in range(size):
        if index < sensor_index[i]:
            sensor_index.insert(i, index)
            break
    else:
        sensor_index.insert(size, index)


def print_results(results):
    '''print the results array copied from device
    '''
    for i in range(results.shape[0]):
        for j in range(results[i].shape[0]):
            print(results[i, j], end=' ')
        print()

from numpy import inf
def amplitude_2_db(abso):
    '''Transform the decibal signal strength into absolute value of iq samples
       y = 20*log10(x)
       where y is power in dB and x is the absolute value of iq samples
    '''
    try:
        val = 20*np.log10(abso)
    except:
        pass
    try:
        val[np.isnan(val)] = -80
        val[val < -80] = -80
    except:
        if val < -80 or val is np.nan:
            val = -80
    return val


def db_2_amplitude(db):
    '''Transform the decibal signal strength into absolute value of iq samples
       x = 10^(y/20)
       where y is power in dB and x is the absolute value of iq samples
    '''
    try:
        if db <= -80:
            return 0
    except:
        pass
    val = np.power(10, np.array(db)/20)
    try:
        val[val <= 0.0001] = 0
    except:
        if val <= 0.0001:  # noise floor
            val = 0
    return val


def find_elbow(inertias, num_intruder):
    '''Find the elbow point of kmeans clustering, to determine the K
    Args:
        inertias (list): a list of float
    Return:
        (int): the K
    '''
    #deltas = []
    #for i in range(len(inertias)-1):
    #    deltas.append(inertias[i] - inertias[i+1])
    #if not deltas:  # there is only one inertia
    #    return 1

    #print('ratio1 = ', deltas[9]/inertias[0])
    #print('ratio2 = ', inertias[9]/inertias[0])

    param ={1:0.5,
            2:0.5,
            4:0.15,
            8:0.08,
            16:0.02,
            24:0.006,
            30:0.003
        }

    i = 0
    while i < len(inertias):
        if inertias[i] < param[num_intruder]*inertias[0] or inertias[i] < 5: # after elbow point: slope is small
            break      # 0.5 for {1, 2}
        i += 1         # 0.15 for {}
    return i+1# 0.0176 for 10~20


def random_secondary():
    '''Generate some random secondary from a pool
    Return:
        (list): a subset from a pool total_secondary
    '''
    total_secondary = [149, 456, 590, 789, 889, 999, 1248, 1500]
    num = random.randint(1, 4)
    secondary = random.sample(total_secondary, num)
    secondary = [149, 1248]
    print('The secondary are: ', secondary)
    return secondary


def random_intruder(grid_len):
    '''Generate some random intruder
    Return:
        (list): a list of integers (transmitter index)
    '''
    intruders = list(range(grid_len*grid_len))
    num = random.randint(3, 4)
    intruder = random.sample(intruders, num)
    print('The new intruder are: ', intruder)
    return intruder


if __name__ == '__main__':
    dic = read_config('config.json')
    print(dic)
    sensor_list = [2, 4, 6, 8]
    ordered_insert(sensor_list, 11)
    print(sensor_list)
    sensor_list.remove(11)
    print(sensor_list)
