# -*- coding: utf-8 -*-
"""
Created on Mon Mar 2023

@author: patri
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel("dist.xlsx")

data.rename(columns={"Unnamed: 0": "Cities"}, inplace=True)
data = data.set_index("Cities")

def array_values_route(array):
    """
    
    """
    array_values = []
    for i in range(len(array) - 1):
        first_selector = array[i]
        second_selector = array[i + 1]
        array_values.append(data[first_selector][second_selector])
    array_values.append(data[array[0]][array[-1]]) 
    
    return array_values


def exchange_positions(array):
        position1 = np.random.randint(0,len(array))
        position2 = np.random.randint(0,len(array))
        new_route = array.copy()
        new_route[position1], new_route[position2] = new_route[position2], new_route[position1]
        return new_route

#############################################################################################

#########################   Algoritmo Simulated Annealing    ################################

#############################################################################################

dist, config = [],[]

for _ in range(30):

    actual_config_labels = np.random.permutation(data.columns)
    actual_energy = sum(array_values_route(actual_config_labels))

    t = 0
    T = 1000
    vector = []

    while T > 5:
        for i in range(100):
            prime_config_labels = exchange_positions(actual_config_labels)
            prime_config_values = array_values_route(prime_config_labels)
            prime_config_energy = sum(prime_config_values)

            delta_e = prime_config_energy - actual_energy
            x = -(delta_e)/T
            q = np.exp(x)
            p = np.random.uniform(0,1)
            if p < q:
                actual_config_labels = prime_config_labels.copy()
                actual_energy = prime_config_energy
                vector.append(actual_energy)

        t +=1
        T = 1000/(1+(t/5))
    
    dist.append(actual_energy)
    config.append(actual_config_labels)

print("Optimal route: ", actual_config_labels, "final energy: ", actual_energy)

#############################################################################################
# Graph of the energy

y = np.array(dist)
plt.plot(y)