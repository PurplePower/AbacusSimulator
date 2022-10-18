from modules.basic_modules import Module, RegSub, RegAdd
from modules.EmptyInto import EmptyInto, EmptyInto2


class ReLU(Module):
    """
    compute diff(x, y) = max(0, x-y) = ReLU(x-y)
    Input reg: x, y
    Output reg: user defined, different from x and y
    """

    def __init__(self, x, y, out, **kwargs):
        super().__init__([x, y], [out], **kwargs)

        self.temp_reg1 = '__t1'
        self.temp_reg2 = '__t2'
        self.other_regs = [self.temp_reg1, self.temp_reg2]

        self.in_flows = ['in']
        self.out_flows = ['out_gt', 'out_lt_ne', 'out_lt_e']

        # main loop to subtract alternatively
        self.ml_t1 = RegAdd(self.temp_reg1)
        self.ml_x = RegSub(x)
        self.ml_t2 = RegAdd(self.temp_reg2)
        self.ml_y = RegSub(y)

        # x <= y (less than)branch
        self.lt_restore_x = EmptyInto(self.temp_reg1, x)
        self.lt_restore_y = EmptyInto(self.temp_reg2, y)
        self.lt_dec_x = RegSub(x)

        # x > y (greater than) branch
        self.gt_restore_y = EmptyInto(self.temp_reg2, y)
        self.gt_dec_y = RegSub(y)
        self.gt_write_res = EmptyInto2(x, self.temp_reg1, out)
        self.gt_inc_res = RegAdd(out)
        self.gt_restore_x = EmptyInto(self.temp_reg1, x)

        self.submodules.extend([
            self.ml_t1, self.ml_x, self.ml_t2, self.ml_y,
            self.lt_restore_x, self.lt_restore_y, self.lt_dec_x,
            self.gt_restore_y, self.gt_dec_y, self.gt_write_res,
            self.gt_inc_res, self.gt_restore_x
        ])

        # construct IO
        self.assign_in('in', self.ml_t1, 'in')
        self.assign_out(self.gt_restore_x, 'out', 'out_gt')
        self.assign_out(self.lt_dec_x, 'ne', 'out_lt_ne')
        self.assign_out(self.lt_dec_x, 'e', 'out_lt_e')

        # construct main loop
        self.ml_t1.connect('out', self.ml_x, 'in')
        self.ml_x.connect('ne', self.ml_t2, 'in')
        self.ml_t2.connect('out', self.ml_y, 'in')
        self.ml_y.connect('ne', self.ml_t1, 'in')

        # construct less than branch
        self.ml_x.connect('e', self.lt_restore_x, 'in')
        self.lt_restore_x.connect('out', self.lt_restore_y, 'in')
        self.lt_restore_y.connect('out', self.lt_dec_x, 'in')

        # construct greater than branch
        self.ml_y.connect('e', self.gt_restore_y, 'in')
        self.gt_restore_y.connect('out', self.gt_dec_y, 'in')
        self.gt_dec_y.connect('e', self.gt_write_res, 'in')
        self.gt_dec_y.connect('ne', self.gt_write_res, 'in')
        self.gt_write_res.connect('out', self.gt_inc_res, 'in')
        self.gt_inc_res.connect('out', self.gt_restore_x, 'in')













