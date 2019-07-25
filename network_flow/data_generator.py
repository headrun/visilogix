import os, sys, math
from optparse import OptionParser

from utils import *

class DataGenerator:
    def __init__(self):
        pass

    def parse(self):
        parser = OptionParser()
        parser.add_option("-c", "--config-file", dest="config_filename", help="Config FILE", metavar="FILE")
        parser.add_option("-o", "--output-file", dest="output_filename", help="xlsx FILE to output", metavar="FILE")
        parser.add_option("-f", "--force", dest="force", help="Force write output", default=False, action='store_true')

        (self.options, args) = parser.parse_args()

        if not self.options.config_filename or \
            not self.options.output_filename:
            parser.print_help()
            parser.error('Invalid Options')

        if not os.path.exists(self.options.config_filename):
            parser.print_help()
            parser.error('File - ' + self.options.config_filename + ' is missing.')
        if not self.options.force and os.path.exists(self.options.output_filename):
            parser.print_help()
            parser.error('File - ' + self.options.output_filename + ' already exists.')

    def process(self):
        self.config = eval(open(self.options.config_filename, 'r').read())

        self.output_obj = ExcelWrap(self.options.output_filename, mode='write')

        self.gen_factory()
        self.gen_line()
        self.gen_depot()
        self.gen_product()

        self.output_obj.save()
        print('Created data file', self.options.output_filename)

    def close(self):
        pass

    def gen_factory(self):
        cfg = self.config['factory']
        self.ns_factory = name_gen(cfg['prefix'], cfg['count'])

        self.sheet_factory, c = self.gen_sheet_data(
            cfg,
            'Factory',
            ['Factory'],
            ['cost'],
            [(x,) for x in self.ns_factory],
        )

    def gen_line(self):
        cfg = self.config['line']
        self.ns_line = name_gen(cfg['prefix'], cfg['count'])

        self.fl_keys = random_mapping(self.ns_factory, self.ns_line, random_numbers_gen(*cfg['factory_map']))

        sh, columns = self.gen_sheet_data(
            cfg,
            'Factory Line',
            ['Factory', 'Line'],
            ['status_formula' if 'status_formula' in cfg else 'status', 'cost', 'shift'],
            self.fl_keys,
            shuffle_keys=True,
        )

        keys = [x[0] for x in cfg['status']]
        values = [[sum(1 for fl, s in zip_union(self.fl_keys, columns[0]) if fl[0] == f and s == k) for f in self.ns_factory] for k in keys]
        max_line_list = [random.randint(1, x) for x in [sum(1 for fl in self.fl_keys if fl[0] == f) for f in self.ns_factory]]
        self.output_obj.write_sheet(
            self.sheet_factory,
            keys + ['Max Line'],
            matrix_transpose(values + [max_line_list]),
            from_column = 2,
        )

    def gen_depot(self):
        cfg = self.config['depot']
        self.ns_depot = name_gen(cfg['prefix'], cfg['count'])

        self.gen_sheet_data(
            cfg,
            'Freight',
            ['Factory', 'Depot'],
            ('freight',),
            [(f, d) for f in self.ns_factory for d in self.ns_depot],
        )

    def gen_product(self):
        cfg = self.config['product']
        self.ns_product = name_gen(cfg['prefix'], cfg['count'])

        lodability_list = random_numbers_gen(*cfg['lodability']).rvs(len(self.ns_product))
        self.output_obj.write_sheet(
            'Product',
            ['Product', 'Lodability'],
            matrix_transpose([self.ns_product, lodability_list])
        )

        self.gen_sheet_data(
            cfg,
            'Product Info',
            ['Factory', 'Line', 'Product'],
            ('capacity', 'labour', 'power', 'fuel'),
            [(f, l, p) for f, l in self.fl_keys for p in self.ns_product],
        )

        num = math.ceil((len(self.ns_factory)*cfg['factory_fiscal'])/100)
        self.gen_sheet_data(
            cfg,
            'Fiscal',
            ['Factory', 'Depot', 'Product'],
            ('fiscal', ),
            [(f, d, p) for f in self.ns_factory[:num] for d in self.ns_depot for p in self.ns_product],
            shuffle_keys=True
        )

        self.gen_sheet_data(
            cfg,
            'Demand',
            ['Depot', 'Product'],
            ('demand', ),
            [(d, p) for d in self.ns_depot for p in self.ns_product],
            shuffle_keys=True,
        )

    def gen_sheet_data(self, cfg, sheet_name, key_names, info_names, keys, shuffle_keys=False):
        columns = [
            self.get_column_data(len(keys), cfg[x])
            for x in info_names
        ]

        if shuffle_keys:
            random.shuffle(keys)
        values = list(
                    map(
                        lambda x: list(x[0])+x[1],
                        zip(keys, matrix_transpose(columns))
                    )
                )
        sheet = self.output_obj.write_sheet(
            sheet_name,
            key_names + [x.capitalize() for x in info_names],
            values,
        )
        return sheet, columns

    def get_column_data(self, cnt, cfg):
        if isinstance(cfg, str) and cfg[0] == '=':
            return [xlwt.Formula(cfg[1:]) for i in range(cnt)]
        elif isinstance(cfg[0], tuple):
            return random_number_by_weight(cnt, cfg)

        return random_numbers(cnt, *cfg)

if __name__ == '__main__':
    main(DataGenerator)
