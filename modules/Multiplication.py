from modules.basic_modules import Module, RegSub
from modules.Additon import Addition


class Multiplication(Module):
    """
    [m1] * [m2] -> n
    0 -> m1
    if [n] = [p] = 0 initially

    """

    def __init__(self, m1, m2, tar, **kwargs):
        super().__init__([m1, m2], [tar], **kwargs)

        self.temp_reg = '__p'
        self.other_regs = [self.temp_reg]

        self.in_flows = ['in']
        self.out_flows = ['out']

        self.adder = Addition(m2, tar)
        self.temp_loop = RegSub(m1)

        self.submodules.extend([self.adder, self.temp_loop])

        # construct
        self.assign_in('in', self.temp_loop, 'in')

        self.temp_loop.connect('ne', self.adder, 'in')
        self.adder.connect('out', self.temp_loop, 'in')

        self.assign_out(self.temp_loop, 'e', 'out')
