# visilogix

## Network Flow

Network flow optimization using gurobi for supply chain domain - factories, lines, depots and products.

### Pylint

sh pylint.sh

### Data Generation

x={name};python3 data_generator.py -c datagen_config/$x.py -o data/$x.xlsx

### Optimization

x={name};python3 optimizer.py -c opt_config/$x.py -i data/$x.xlsx -o opt_runs/$x > opt.log; mv opt.log opt_runs/$x

solution file is opt_runs/$x/solution.xlsx
