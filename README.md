# visilogix

## Network Flow

Network flow optimization using gurobi for supply chain domain - factories, lines, depots and products.

### Pylint

sh pylint.sh

### Data Generation

x={name};python3 data_generator.py -c datagen_config/$x.py -o data/$x.xlsx

### Optimization

x={name};m=gurobi;d=opt_runs/$x/$m;
python3 optimizer.py -c opt_config/$x.py -i data/$x.xlsx -o $d > opt.log; mv opt.log $d

solution file is $d/solution.xlsx
