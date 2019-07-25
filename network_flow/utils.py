import os, errno, time, random

import xlrd, xlwt

def main(cls):
    s = time.time()
    status = 0

    obj = cls()
    obj.parse()

    status = obj.process()
    if status:
        print(cls.__name__, 'process failed with status:', status)

    obj.close()

    print('Time Taken:', time.time()-s)

def makedir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

class ExcelWrap:
    def __init__(self, filename, mode='read'):
        self.filename = filename

        self.book = xlwt.Workbook() if mode == 'write' else xlrd.open_workbook(self.filename)

    def read_list(self, sheet, value=None, start_row=1, value_func=None, **kwargs):
        sheet_obj = self.book.sheet_by_name(sheet)
        lines = []
        for r in range(start_row, sheet_obj.nrows):
            val = sheet_obj.cell_value(r, value-1)
            lines.append(self.get_value(val, value_func) if value_func else val)

        return lines

    def read_dict(self, sheet, key=None, value=None, value_type='int', start_row=1, value_func=None, **kwargs):
        sheet_obj = self.book.sheet_by_name(sheet)
        value_type_func = lambda x: int(x) if value_type == 'int' and x else x
        
        dt = {}
        for r in range(start_row, sheet_obj.nrows):
            if isinstance(key, int):
                key_row = sheet_obj.cell_value(r, key-1)
                if not key_row:
                    continue
            else:
                key_row = tuple([sheet_obj.cell_value(r, c-1) for c in key])
                if [1 for x in key_row if not x]:
                    continue

            if isinstance(value, int):
                value_row = value_type_func(sheet_obj.cell_value(r, value-1))
            else:
                value_row = {j: value_type_func(sheet_obj.cell_value(r, c-1)) for j, c in value.items()}

            dt[key_row] = value_func(value_row) if value_func else value_row
        return dt

    def get_value(self, value, func):
        return func(value) if func else value

    def save(self):
        self.book.save(self.filename)

    def write_sheet(self, sheet, keys, values, from_row=0, from_column=0):
        sheet = self.get_sheet(sheet)
        self.write(sheet, [keys], from_row, from_column)
        self.write(sheet, values, from_row+1, from_column)
        return sheet

    def write(self, sheet, values, from_row=0, from_column=0):
        for r, d in enumerate(values):
            for c, v in enumerate(d):
                sheet.write(from_row+r, from_column+c, v)

    def get_sheet(self, sheet):
        return self.book.add_sheet(sheet) if isinstance(sheet, str) else sheet

def zip_union(*args):
    val = list(zip(*args))
    n = len(val)

    while True:
        x, flag = ['']*len(args), False
        for i, v in enumerate(args):
            if n < len(v):
                x[i] = v[n]
                flag = True
        if not flag:
            break
        val.append(x)
        n += 1

    return val

def name_gen(prefix, cnt):
    size = len(str(cnt))
    return [f'{prefix}{i:0{size}}' for i in range(1, cnt+1)]

def matrix_transpose(val):
    return list(map(list, zip_union(*val)))

def random_numbers_gen(low, upp, mean, sd):
    from scipy.stats import truncnorm

    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

def random_numbers(cnt, low, upp, unit=1, pct=100):
    return [random.randint(low, upp)*unit for i in range(int(round(cnt*(pct/100 if pct != None else 1))))]

def random_number_by_weight(cnt, wt_val):
    val = []
    total_wt = sum(x[1] for x in wt_val)
    for v, wt in wt_val:
        n = min(int(round((wt*cnt)/total_wt)), cnt-len(val))
        val += [v]*n
    if len(val) < cnt:
        val += [v]*(cnt-len(val))
    random.shuffle(val)
    return val

def random_mapping(ls_a, ls_b, gen):
    val, j = [], 0
    rn_val = gen.rvs(len(ls_a))
    for i, a in enumerate(ls_a):
        n = min(int(round(rn_val[i])), len(ls_b)-len(ls_a)-j+i+1) if i < len(ls_a)-1 else len(ls_b)-j
        for k in range(n):
            val.append((a, ls_b[j]))
            j += 1

    return val

