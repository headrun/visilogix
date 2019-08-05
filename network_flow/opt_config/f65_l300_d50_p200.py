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
        # scaling factors the flow needs to be multiplied with. This is because of production capacity and demand value_func. The unit considered for the algo is 10Tons and then multiplying by 10 to get result in Tons. This is to reduce the range of coefficients, which helped the gurobi algo to give optimal solution in less than an hour.
        'obj_factor': 10,
        'flow_factor': 10,
    },
    'data': {
        'factory_fixed_cost': { # cost per year
            'sheet': 'Factory',
            'key': 1, #column num
            'value': 2, #column num
            'value_func': lambda x: 0.1*x, #scaling down because of product_capacity value_func
        },
        'factory_max_line': {
            'sheet': 'Factory',
            'key': 1, #column num
            'value': 5, #column num
        },
        'factory_lines': {
            'sheet': 'Factory Line',
            'key': (1, 2), #column nums
            'value': 3, #column num
            'value_type': 'str',
        },
        'line_capex': { # cost per year
            'sheet': 'Factory Line',
            'key': (1, 2), #column num
            'value': 4, #column num
            'value_func': lambda x: 0.1*x, #scaling down because of product_capacity value_func
        },
        'line_shifts': { # shifts per line per year
            'sheet': 'Factory Line',
            'key': (1, 2), #column num
            'value': 5, #column num
            'hours': 8,
        },
        'freight': { # cost per truck
            'sheet': 'Freight',
            'key': (1, 2), #column num
            'value': 3, #column num
        },
        'product_lodability': { # ton per truck
            'sheet': 'Product',
            'key': 1, #column num
            'value': 2, #column num
            'value_type': 'float',
        },
        'product_capacity': { # ton per shift
            'sheet': 'Product Info',
            'key': (1, 2, 3), #column num
            'value': 4, #column num
            'value_func': lambda x: 0.1*x,
        },
        'product_manufacturing_cost': { # cost per ton
            'sheet': 'Product Info',
            'key': (1, 2, 3), #column num
            'value': {
                'labour': 5, #column num
                'power' : 6, #column num
                'fuel'  : 7, #column num
            },
        },
        'depot_benefit': { # cost per ton
            'sheet': 'Fiscal',
            'key': (1, 2, 3), #column num
            'value': 4, #column num
        },
        'depot_demand': { # ton per year
            'sheet': 'Demand',
            'key': (1, 2), #column num
            'value': 3, #column num
            'value_func': lambda x: 0.1*x,
        },
    },
}
