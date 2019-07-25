import os, traceback

from gurobipy import *

class GurobiModel(Model):
    CONST = GRB

    def init(self, cfg):
        pass

    def setValue(self, var, val):
        var.setAttr(GRB.Attr.LB, val)
        var.setAttr(GRB.Attr.UB, val)

    def solve(self):
        self.update()
        self.optimize()

    def isOptimal(self):
        return self.status == GRB.Status.OPTIMAL

    def statusName(self):
        return self.status

    def getValue(self, var):
        return var.X

    def getSumValue(self, sum_var):
        return sum_var.getValue()

    def save(self, dirname):
        for ext in ('lp', 'sol'):
            filename = 'model.%s' % ext
            try:
                self.write(os.path.join(dirname, filename))
            except:
                traceback.print_exc()

        self.printQuality()
