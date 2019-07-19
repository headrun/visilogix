#!/bin/sh

set +x

pylint -E *.py --generated-members=factory_fixed_cost,factory_lines,line_capex,product_manufacturing_cost,product_lodability,freight,product_capacity,line_shifts,factory_max_line,line_shifts,depot_benefit,depot_demand
