"""
Define some modules that empty the input reg's value
into output reg's value.


"""

from modules.basic_modules import RegAdd, RegSub, Module


class EmptyInto(Module):
    """
    [src] + [tar] -> tar
    0 -> src
    """

    def __init__(self, src, tar, **kwargs):
        super().__init__([src], [tar], **kwargs)
        assert src != tar

        self.in_flows = ['in']
        self.out_flows = ['out']

        self.looper = RegSub(src)
        self.adder = RegAdd(tar)

        self.submodules.extend([
            self.looper, self.adder
        ])

        # construct
        self.assign_in('in', self.looper, 'in')
        self.looper.connect('ne', self.adder, 'in')
        self.adder.connect('out', self.looper, 'in')
        self.assign_out(self.looper, 'e', 'out')


class EmptyInto2(Module):
    """
    [s] + [t1] -> t1
    [s] + [t2] -> t2
    0 -> s
    """

    def __init__(self, src, tar1, tar2, **kwargs):
        super().__init__([src], [tar1, tar2], **kwargs)

        # no temp regs

        self.in_flows = ['in']
        self.out_flows = ['out']

        self.looper = RegSub(src)
        self.adder1 = RegAdd(tar1)
        self.adder2 = RegAdd(tar2)

        self.submodules.extend([self.looper, self.adder1, self.adder2])

        # construct
        self.assign_in('in', self.looper, 'in')

        self.looper.connect('ne', self.adder1, 'in')
        self.adder1.connect('out', self.adder2, 'in')
        self.adder2.connect('out', self.looper, 'in')

        self.assign_out(self.looper, 'e', 'out')
