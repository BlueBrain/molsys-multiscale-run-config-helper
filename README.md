The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board of the Swiss Federal Institutes of Technology.

Copyright (c) 2024 Blue Brain Project/EPFL

# Introduction
This simple script allows to generate the following multiscale_run configuration files:
* mrci_gids.txt    
* mrci_exc_gids.txt
* mrci_inh_gids.txt 
* mrci_L1_gids.txt  
* mrci_L2_gids.txt  
* mrci_L3_gids.txt 
* mrci_L4_gids.txt  
* mrci_L5_gids.txt 
* mrci_L6_gids.txt    
* node_sets.json


# Usage
```bash
prompt%> generate.py -c <circuit_file> -o <output_path> -f <filter_neuron> -n <neuron_population_name>
```


