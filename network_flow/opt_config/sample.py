{
    'model': {
        'gurobi': {
            'params': {
                'LogFile': '{output_dirname}/gurobi.log',
                'OutputFlag': True,
            },
        },
    },
    'output': {
        'obj_factor': 1,
        'flow_factor': 1,
    },
    'data': {
        'factory_fixed_cost': { # cost per year
            'sheet': 'Fixed Cost',
            'key': 1,
            'value': 2,
        },
        'factory_max_line': {
            'sheet': 'Max Line',
            'start_row': 3,
            'key': 1,
            'value': 4,
        },
        'factory_lines': {
            'sheet': 'Factory Line',
            'key': (1, 2),
            'value': 3,
        },
        'line_capex': { # cost per year
            'sheet': 'Capital Cost',
            'key': (1, 2),
            'value': 3,
        },
        'line_shifts': { # shifts per line per year
            'sheet': 'Shift Master',
            'start_row': 2,
            'key': (1, 2),
            'value': 3,
            'hours': 8,
        },
        'freight': { # cost per truck
            'sheet': 'Freight',
            'key': (1, 2),
            'value': 3,
        },
        'product_lodability': { # ton per truck
            'sheet': 'LTCP Product',
            'start_row': 2,
            'key': 2,
            'value': 3,
        },
        'product_capacity': { # ton per shift
            'sheet': 'Capacity',
            'key': (1, 2, 3),
            'value': 4,
        },
        'product_manufacturing_cost': { # cost per ton
            'sheet': 'LPF',
            'start_row': 2,
            'key': (1, 2, 3),
            'value': {
                'labour': 4,
                'power' : 6,
                'fuel'  : 5,
            },
        },
        'depot_benefit': { # cost per ton
            'sheet': 'Fiscal',
            'key': (2, 3, 1),
            'value': 4,
        },
        'depot_demand': { # ton per year
            'sheet': 'Demand',
            'key': (1, 2),
            'value': 3,
        },
    },
}
