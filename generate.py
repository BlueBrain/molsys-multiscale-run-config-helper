#!/usr/bin/env python
# coding: utf-8

from getopt import getopt, GetoptError

import json
import numpy as np
import os
import pandas as pd
import sys

from bluepysnap import Circuit


def generate(circuit_path:str, output_path:str, neuron_population_name:str, filter_neuron:bool):
    """
    Generate the multiscale_run node_sets.json configuration files and metabolism ones
    :param circuit_path: path to the somata circuit json file (ngv_config.json)
    :param outputpath: path to the output directory where the configuration files will be exported.
    :param neuron_population_name: the sonata neuron population name
    :param filter_neuron: If True, the neuron ids will contain only the neuron that are connected to the astrocytes,
                         otherwise, the list will contain all the neurons ids 
    :return:
    """
    c = Circuit(circuit_path)

    # Create a list of astrocyte ids, that contains all the astrocytes with endfoot
    gliovascular = c.edges["gliovascular"]
    edges_ids = np.arange(gliovascular.size, dtype=np.uint16)
    df = gliovascular.get(edges_ids, ["@target_node", "endfoot_compartment_length"])
    filtered_df = df[df.endfoot_compartment_length > 0]
    selected_astrocytes_id = filtered_df["@target_node"].unique()

    # Remove from thi list the astrocytes with at least one endfoot_compartment_length == 0.0
    filtered_df = df[df.endfoot_compartment_length == 0]
    astroytes_id_to_remove = filtered_df["@target_node"].to_numpy()
    indices_to_remove = np.where(np.in1d(selected_astrocytes_id, astroytes_id_to_remove))[0]
    selected_astrocytes_id = np.delete(selected_astrocytes_id, indices_to_remove)
    print(f'INFO: There are {selected_astrocytes_id.size} astrocytes with valid endfeet')

    if filter_neuron:
        neuroglial = c.edges["neuroglial"]
        edges_ids = np.arange(neuroglial.size, dtype=np.uint16)
        df = neuroglial.get(edges_ids, ["@source_node", "@target_node"])
        selected_neuron = df[df["@source_node"].isin(selected_astrocytes_id)][
            "@target_node"
        ].unique()
        neuro_df = c.nodes[neuron_population_name].get(selected_neuron)

    else:
        selected_neuron = np.arange(c.nodes[neuron_population_name].size, dtype=np.uint16)
        neuro_df = c.nodes[neuron_population_name].get(selected_neuron)

    print(f'INFO: There are {selected_neuron.size} selected neurons')


    neuro_df = neuro_df.rename(columns={"population": "population_name"})
    neuro_df = neuro_df.reset_index(drop=False)

    mrci_all_ids = list(neuro_df.node_ids.values)
    mrci_exc_ids = list(neuro_df.loc[neuro_df["synapse_class"] == "EXC"].node_ids.values)
    mrci_inh_ids = list(neuro_df.loc[neuro_df["synapse_class"] == "INH"].node_ids.values)

    mrci_L1_ids = list(neuro_df.loc[neuro_df["layer"] == 1].node_ids.values)
    mrci_L2_ids = list(neuro_df.loc[neuro_df["layer"] == 2].node_ids.values)
    mrci_L3_ids = list(neuro_df.loc[neuro_df["layer"] == 3].node_ids.values)
    mrci_L4_ids = list(neuro_df.loc[neuro_df["layer"] == 4].node_ids.values)
    mrci_L5_ids = list(neuro_df.loc[neuro_df["layer"] == 5].node_ids.values)
    mrci_L6_ids = list(neuro_df.loc[neuro_df["layer"] == 6].node_ids.values)


    mrci_all_f = os.path.join(output_path , "mrci_gids.txt")
    mrci_exc_f = os.path.join(output_path , "mrci_exc_gids.txt")
    mrci_inh_f = os.path.join(output_path , "mrci_inh_gids.txt")

    mrci_L1_f = os.path.join(output_path , "mrci_L1_gids.txt")
    mrci_L2_f = os.path.join(output_path , "mrci_L2_gids.txt")
    mrci_L3_f = os.path.join(output_path , "mrci_L3_gids.txt")
    mrci_L4_f = os.path.join(output_path , "mrci_L4_gids.txt")
    mrci_L5_f = os.path.join(output_path , "mrci_L5_gids.txt")
    mrci_L6_f = os.path.join(output_path , "mrci_L6_gids.txt")

    # Create the output directory is it does not exist yet.
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass


    pd.Series(mrci_all_ids).to_csv(mrci_all_f, sep="\t", index=False, header=None)

    pd.Series(mrci_exc_ids).to_csv(mrci_exc_f, sep="\t", index=False, header=None)
    pd.Series(mrci_inh_ids).to_csv(mrci_inh_f, sep="\t", index=False, header=None)

    pd.Series(mrci_L1_ids).to_csv(mrci_L1_f, sep="\t", index=False, header=None)
    pd.Series(mrci_L2_ids).to_csv(mrci_L2_f, sep="\t", index=False, header=None)
    pd.Series(mrci_L3_ids).to_csv(mrci_L3_f, sep="\t", index=False, header=None)
    pd.Series(mrci_L4_ids).to_csv(mrci_L4_f, sep="\t", index=False, header=None)
    pd.Series(mrci_L5_ids).to_csv(mrci_L5_f, sep="\t", index=False, header=None)
    pd.Series(mrci_L6_ids).to_csv(mrci_L6_f, sep="\t", index=False, header=None)


    # Generate the node_sets.json
    template = {
        "testNGVSSCX_AstroMini": ["testNGVSSCX", "Astrocytes"],
        "src_cells": {"population": "All", "node_id": None},
        "testNGVSSCX": {"population": "All", "node_id": None},
        "Astrocytes": {"population": "astrocytes", "node_id": None},
    }

    template["src_cells"]["node_id"] = selected_neuron.tolist()
    template["testNGVSSCX"]["node_id"] = selected_neuron.tolist()
    template["Astrocytes"]["node_id"] = selected_astrocytes_id.tolist()

    output_filename = os.path.join(output_path, "node_sets.json")
    with open(output_filename, "w") as fout:
        json_dumps_str = json.dumps(template, indent=4)
        print(json_dumps_str, file=fout)






    print(f'INFO: Done: configuration files was exported to {output_path}')

def exit():
    print("generate.py -c <circuit_file> -o <output_path> -f <filter_neuron> -n <neuron_population_name>")
    sys.exit()

def main(argv):
    circuit_path = None
    output_path = None
    filter_neuron = False
    neuron_population_name = 'All'
    try:
        opts, args = getopt(argv, "hc:o:fn:", ["circuit_file=", "output_path=",
                                                      "filter_neuron=", "neuron_population_name="])

        if len(opts) == 0:
            exit()
        for opt, arg in opts:
            if opt == "-h":
                exit()
            elif opt in ("-c", "--circuit_file"):
                circuit_path = arg
            elif opt in ("-o", "--output_path"):
                output_path = arg
            elif opt in ("-n", "--neuron_population_name"):
                neuron_population_name = arg
            elif opt in ("-f", "--filter_neuron"):
                filter_neuron = True
            else:
                exit()
        if circuit_path and output_path:
            print(f'INFO: generate( circuit_path:{circuit_path}, output_path:{output_path},'
                  f' neuron_population_name={neuron_population_name}, filter_neuron={filter_neuron})')
            generate(circuit_path, output_path, neuron_population_name=neuron_population_name, filter_neuron=filter_neuron)
        else:
            exit()
    except  GetoptError as e:
        print(f'ERROR: {e}')

if __name__ == "__main__":
    main(sys.argv[1:])
