# visilogix

## Network Flow

Network flow optimization using gurobi for supply chain domain - factories(f), lines(l), depots(d) and products(p).

<pre>
Given,
  factory_fixed_cost(f) 		# Cost in Rs per year
  factory_max_line(f)			# Max number of Lines to be active

  factory_lines(f, l)			# New/Existing. Mapping factory(f) to line(l)
  line_capex(f, l)			# Cost in Rs per year
  line_shifts(f, l)			# Maximum number of shifts per year

  freight(f, d)				# Cost in Rs per Truck from factory(f) to depot(d)

  product_lodability(p)			# Number of Tons which can be loaded per truck
  product_manufacturing_cost(f, l, p)	# Cost in Rs per Ton of product(p) on a line(l)
  depot_benefit(f, d, p)		# Saving in Rs per Ton of product(p) from factory(f) to depot(d)

  demand(d, p)				# Minimum Number of Tons of product(p) to be delivered to depot(d)

optimizer.py finds the network flow(f, l, d, p) with Optimal cost.
  network flow(f, l, d, p)           # Number of Tons of product(p) to be manufactured
                                     # in factory(f), line(l) and delivered to depot(d)
</pre>

### Pylint

sh pylint.sh

### Data Generation

x={name};python3 data_generator.py -c datagen_config/$x.py -o data/$x.xlsx

### Optimization

x={name};m=gurobi;d=opt_runs/$x/$m;
python3 optimizer.py -c opt_config/$x.py -i data/$x.xlsx -o $d > opt.log; mv opt.log $d

solution file is $d/solution.xlsx
