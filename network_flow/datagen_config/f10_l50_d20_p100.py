{
    'factory': {
        'prefix': 'F',
        'count': 10,
        'cost': (1, 15, 10**7),#min, max, unit
    },
    'line': {
        'prefix': 'L',
        'count': 50,
        'factory_map': (1, 10, 5, 1),#min, max, mean, sd

        'status': (('Existing', 30), ('New', 70)),
        'cost': (1, 15, 10**7, 50),#min, max, unit, %
        'shift': ((900, 60), (987, 40)),#(option, weight)
    },
    'depot': {
        'prefix': 'D',
        'count': 20,
        'freight': (1, 20, 10**4),
    },
    'product': {
        'prefix': 'P',
        'count': 100,
        'lodability': (1, 7, 4, 3),

        'capacity': (10, 20),
        'labour': (2, 15, 10**3),
        'power': (3, 20, 10**2),
        'fuel': (5, 70, 10**2),

        'factory_fiscal': 2, #%
        'fiscal': (1, 50, 10**3),
        'demand': (1, 10**3, 1, 40),
    },
}
