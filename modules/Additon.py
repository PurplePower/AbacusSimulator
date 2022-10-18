from modules.basic_modules import RegAdd, RegSub, Module


class Addition(Module):
    """
    [m] + [n] -> n
    a temporary reg p is 0 initially
    """

    def __init__(self, src, tar, **kwargs):
        super().__init__([src], [tar], **kwargs)

        self.temp_reg = '__p'
        self.other_regs = [self.temp_reg]

        self.in_flows = ['in']
        self.out_flows = ['out']

        self.src = RegSub(src)
        self.tar = RegAdd(tar)
        self.src_restore = RegAdd(src)

        self.temp1 = RegAdd(self.temp_reg)
        self.temp2 = RegSub(self.temp_reg)

        self.submodules.extend([
            self.src, self.tar, self.temp1, self.temp2, self.src_restore
        ])

        # construct
        self.assign_in('in', self.src, 'in')

        # construct empty src into tar and temp
        self.src.connect('ne', self.tar, 'in')
        self.tar.connect('out', self.temp1, 'in')
        self.temp1.connect('out', self.src, 'in')

        # restore src
        self.src.connect('e', self.temp2, 'in')
        self.temp2.connect('ne', self.src_restore, 'in')
        self.src_restore.connect('out', self.temp2, 'in')

        self.assign_out(self.temp2, 'e', 'out')
