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
    },
    'data': {
        'factory_fixed_cost': { # cost per year
            'sheet': 'Factory',
            'key': 1,
            'value': 2,
        },
        'factory_max_line': {
            'sheet': 'Factory',
            'key': 1,
            'value': 5,
        },
        'factory_lines': {
            'sheet': 'Factory Line',
            'key': (1, 2),
            'value': 3,
        },
        'line_capex': { # cost per year
            'sheet': 'Factory Line',
            'key': (1, 2),
            'value': 4,
        },
        'line_shifts': { # shifts per line per year
            'sheet': 'Factory Line',
            'key': (1, 2),
            'value': 5,
            'hours': 8,
        },
        'freight': { # cost per truck
            'sheet': 'Freight',
            'key': (1, 2),
            'value': 3,
        },
        'product_lodability': { # ton per truck
            'sheet': 'Product',
            'key': 1,
            'value': 2,
        },
        'product_capacity': { # ton per shift
            'sheet': 'Product Info',
            'key': (1, 2, 3),
            'value': 4,
        },
        'product_manufacturing_cost': { # cost per ton
            'sheet': 'Product Info',
            'key': (1, 2, 3),
            'value': {
                'labour': 5,
                'power' : 6,
                'fuel'  : 7,
            },
        },
        'depot_benefit': { # cost per ton
            'sheet': 'Fiscal',
            'key': (1, 2, 3),
            'value': 4,
        },
        'depot_demand': { # ton per year
            'sheet': 'Demand',
            'key': (1, 2),
            'value': 3,
        },
    },
}
