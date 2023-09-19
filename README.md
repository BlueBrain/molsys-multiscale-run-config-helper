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
prompt%> ./generate.py -c ./tests/data/ngv_config.json -o Test_output --neuron_population_name All
```
