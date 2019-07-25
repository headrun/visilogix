import os, sys, math
from optparse import OptionParser

from utils import main, makedir_p, ExcelWrap

class Optimizer:
    def __init__(self):
        pass

    def parse(self):
        parser = OptionParser()
        parser.add_option("-c", "--config-file", dest="config_filename", help="Config FILE", metavar="FILE")
        parser.add_option("-i", "--input-file", dest="input_filename", help="xlsx FILE to read", metavar="FILE")
        parser.add_option("-o", "--output-dir", dest="output_dirname", help="output directory name", metavar="FILE")
        parser.add_option("-m", "--model", dest="model", help="Name of the Model", default='gurobi')
        parser.add_option("-f", "--force", dest="force", help="Force write output", default=False, action='store_true')

        (self.options, args) = parser.parse_args()

        if not self.options.config_filename or \
                not self.options.input_filename or \
                not self.options.output_dirname:
            parser.print_help()
            parser.error('Invalid Options')

        for x in ('config_filename', 'input_filename'):
            if not os.path.exists(getattr(self.options, x)):
                parser.print_help()
                parser.error('File - ' + x + ' is missing.')

        if not self.options.force and os.path.exists(self.options.output_dirname):
            parser.print_help()
            parser.error('Directory - ' + self.options.output_dirname + ' already exists.')

        self.output_filename = os.path.join(self.options.output_dirname, 'solution.xlsx')
        makedir_p(self.options.output_dirname)

    def process(self):
        self.config = eval(open(self.options.config_filename, 'r').read())
        self.config_data, self.config_model, self.config_output = [self.config[x] for x in ('data', 'model', 'output')]

        self.read_input()

        self.init_model()

        self.init_variables()
        self.set_constraints()
        self.set_objective()

        self.model.solve()
        self.model.save(self.options.output_dirname)

        self.output_solution()

    def close(self):
        pass

    def read_input(self):
        self.input_obj = ExcelWrap(self.options.input_filename)

        for name, cfg in self.config_data.items():
            args = []
            typ = cfg.get('type', 'dict')
            if typ == 'list':
                pass
            else:
                args.append(cfg['key'])

            ret = getattr(self.input_obj, 'read_'+typ)(**cfg)
            setattr(self, name, ret)

    def init_model(self):
        name = self.options.model
        cfg = self.config['model'].get(name, {})

        self.model = getattr(__import__('%s_model' % name), '%sModel' % name.capitalize())()
        self.model.init(cfg)

        for param, value in cfg.get('params', {}).items():
            if param.lower() == 'logfile':
                value = value.format(output_dirname=self.options.output_dirname)
            self.model.setParam(param, value)

    def init_variables(self):
        self.ky_factory_lines = sorted(self.factory_lines.keys())

        self.ns_factory = sorted(list(set([f for f, l in self.ky_factory_lines])))
        self.ns_line    = sorted(list(set([l for f, l in self.ky_factory_lines])))
        self.ns_depot   = sorted(list(set([d for f, d in self.freight.keys()])))
        self.ns_product = sorted(self.product_lodability.keys())

        keys = [
            (f, l, d, p)
            for f, l in self.ky_factory_lines
            for d    in self.ns_depot
            for p    in self.ns_product
        ]
        self.m_flow = self.model.addVars(keys, vtype=self.model.CONST.CONTINUOUS, name='flow')

        self.m_is_valid_line = self.model.addVars(self.ky_factory_lines, vtype=self.model.CONST.BINARY, name='is_line')

        print('...  Number of variables:', (len(keys)+len(self.ky_factory_lines)))

    def set_constraints(self):
        for f in self.ns_factory:
            num_lines = len(self.m_is_valid_line.select(f, '*'))

            # max lines in a factory
            self.model.addConstr(
                self.m_is_valid_line.sum(f, '*') <= self.factory_max_line.get(f, num_lines)
            )

        capacity_lambda = lambda x: self.product_capacity.get(x, 0)
        self.hours_per_shift = self.config_data['line_shifts']['hours']
        for f, l in self.ky_factory_lines:

            # flow <= supply
            for p in self.ns_product:
                if not capacity_lambda((f, l, p)):
                    for d in self.ns_depot:
                        self.model.setValue(self.m_flow[f, l, d, p], 0)

            self.model.addConstr(
                sum([
                    (self.m_flow.sum(f, l, '*', p) * self.hours_per_shift) / capacity_lambda((f, l, p))
                    for p in self.ns_product
                        if capacity_lambda((f, l, p))
                ]) <= self.m_is_valid_line[f, l] * self.line_shifts[f, l] * self.hours_per_shift
            )

        for d in self.ns_depot:
            for p in self.ns_product:
                # flow >= demand
                self.model.addConstr(
                    self.m_flow.sum('*', '*', d, p) >= self.depot_demand.get((d, p), 0)
                )

    def set_objective(self):
        self.model.setObjective(
            # Fixed Cost
            sum(
                self.factory_fixed_cost[f] * (1 if self.m_is_valid_line.sum(f, '*') else 0)
                for f in self.ns_factory
            ) +
            # line capex
            sum(
                self.line_capex.get(l, 0) * self.m_is_valid_line[f, l]
                for f, l in self.ky_factory_lines
            ) +
            # manufacturing cost
            sum(
                self.m_flow.sum(f, l, '*', p) * sum(self.product_manufacturing_cost.get((f, l, p), {}).values())
                for f, l in self.ky_factory_lines
                for p    in self.ns_product
            ) +
            # Transportation cost
            sum(
                #math.ceil
                (self.m_flow.sum(f, '*', d, p) / self.product_lodability[p] + 1) * self.freight.get((f, d), 0)
                for f in self.ns_factory
                for d in self.ns_depot
                for p in self.ns_product
            ) -
            # depot product benefit
            sum(
                self.m_flow.sum(f, '*', d, p) * self.depot_benefit.get((f, d, p), 0)
                for f in self.ns_factory
                for d in self.ns_depot
                for p in self.ns_product
            ),
            self.model.CONST.MINIMIZE
        )

    def output_solution(self):
        if not self.model.isOptimal():
            print('...  Non Optimal output:', self.model.statusName())
            return

        self.output_obj = ExcelWrap( self.output_filename, mode='write')

        val = round(self.model.ObjVal*self.config_output.get('obj_factor', 1), 2)
        print('...  Optimal Cost:', f'{val:,}')
        self.output_obj.write_sheet(
            'Optimal Cost',
            ['Total Cost'],
            [[val]],
        )

        self.output_flow()
        self.output_factory_capacity()
        self.output_line_capacity()

        self.output_obj.save()

    def output_factory_capacity(self):
        val = [(f, round(self.model.getSumValue(self.m_is_valid_line.sum(f, '*')))) for f in self.ns_factory]
        print('Factories unused:', [(f, v) for f, v in val if not v])
        print('Factories used:',   [(f, v) for f, v in val if v])
        print()
        self.output_obj.write_sheet(
            'Factory',
            ['Factory', 'Used Lines', 'Unused Lines'],
            [(f, v, sum(1 for _f, _l in self.ky_factory_lines if _f==f)-v) for f, v in val],
        )

    def output_line_capacity(self):
        print('Lines:')
        values = []
        for (f, l), val in self.m_is_valid_line.items():
            pct = round((sum(
                (self.model.getSumValue(self.m_flow.sum(f, l, '*', p)) * self.hours_per_shift) / self.product_capacity[f, l, p]
                for p in self.ns_product
                if (f, l, p) in self.product_capacity
            ) * 100) / (self.line_shifts[f, l] * self.hours_per_shift), 2)
            values.append((f, l, pct))
            print('%20s' % str((f, l)), ':', '%2.2f%%' % pct if self.model.getValue(val) and pct else '.....close')
        print()
        self.output_obj.write_sheet(
            'Factory Line',
            ['Factory', 'Line', 'Capacity Utilization(%)'],
            values,
        )

    def output_flow(self):
        flow_factor = self.config_output.get('flow_factor', 1)
        print('Network Flow:', flow_factor)
        val_dict = {key: round(self.model.getValue(var)*flow_factor, 2) for key, var in self.m_flow.items()}
        for key, val in val_dict.items():
            if val:
                print('%40s' % str(key), ':', '%14s' % f'{val:,}')

                # Partial truck load %
                #ld = self.product_lodability[key[3]]
                #print('%40s' % str(key), ':', '%2d%%' % round((((val % ld) * 100) / ld)), '%10s' % f'{round(val):,}')
        print()
        self.output_obj.write_sheet(
            'Network Flow',
            ['Factory', 'Line', 'Depot', 'Product', 'Ton'],
            [(f, l, d, p, v) for (f, l, d, p), v in val_dict.items() if v],
        )

    def check_constraints(self):
        for f in self.ns_factory:
            num_lines = len(self.m_is_valid_line.select(f, '*'))

            # max lines in a factory
            assert self.m_is_valid_line.sum(f, '*') <= self.factory_max_line.get(f, num_lines)

        for f, l in self.ky_factory_lines:
            capacity_lambda = lambda x: self.product_capacity.get(x, 0)
            self.hours_per_shift = self.config_data['line_shifts']['hours']

            # flow <= max supply
            for p in self.ns_product:
                if not capacity_lambda((f, l, p)):
                    for d in self.ns_depot:
                        assert self.model.getValue(self.m_flow[f, l, d, p]) == 0

            assert sum([
                    (self.m_flow.sum(f, l, '*', p) * self.hours_per_shift) / capacity_lambda((f, l, p))
                    for p in self.ns_product
                    if capacity_lambda((f, l, p))
                ]) <= self.model.getValue(self.m_is_valid_line[f, l]) * self.line_shifts[f, l] * self.hours_per_shift

        for d in self.ns_depot:
            for p in self.ns_product:
                # flow >= demand
                assert self.m_flow.sum('*', '*', d, p) >= self.depot_demand.get((d, p), 0)

if __name__ == '__main__':
    main(Optimizer)
