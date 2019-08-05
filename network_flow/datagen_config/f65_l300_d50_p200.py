{
    'factory': {
        'prefix': 'F',
        'count': 65,
        'cost': (1, 15, 10**7),#min, max, unit
    },
    'line': {
        'prefix': 'L',
        'count': 300,
        'factory_map': (1, 10, 5, 1),#min, max, mean, sd

        'status': (('Existing', 30), ('New', 70)),
        'cost': (1, 15, 10**7, 50),#min, max, unit, %
        'shift': ((900, 60), (987, 40)),#(option, weight)
    },
    'depot': {
        'prefix': 'D',
        'count': 50,
        'freight': (1, 20, 10**4),#min, max, unit
    },
    'product': {
        'prefix': 'P',
        'count': 200,
        'lodability': (1, 7, 4, 3),#min, max, mean, sd

        'capacity': (10, 20),#min, max
        'labour': (2, 15, 10**3),#min, max, unit
        'power': (3, 20, 10**2),#min, max, unit
        'fuel': (5, 70, 10**2),#min, max, unit

        'factory_fiscal': 2, #%
        'fiscal': (1, 50, 10**3),#min, max, unit

        'demand': (1, 10**3, 1, 40),#min, max, unit, %
    },
}
