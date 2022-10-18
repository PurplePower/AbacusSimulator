from modules.basic_modules import Module, RegSub, RegAdd
from modules.EmptyInto import EmptyInto, EmptyInto2


class ModRem(Module):

    def __init__(self, x, y, r, q, **kwargs):
        super().__init__([x, y], [r, q], **kwargs)

        self.temp_reg1 = '__t1'
        self.temp_reg2 = '__t2'
        self.temp_reg3 = '__t3'
        self.temp_reg4 = '__t4'
        self.other_regs = [
            self.temp_reg1, self.temp_reg2,
            self.temp_reg3, self.temp_reg4
        ]

        self.in_flows = ['in']
        self.out_flows = ['out_y=0', 'out']

        # check if y==0
        self.check_y_sub = RegSub(y)
        self.check_y_add = RegAdd(y)
        self.check_x_to_t4 = EmptyInto(x, self.temp_reg4)
        self.check_write_rem = EmptyInto2(self.temp_reg4, x, r)

        # main loop
        self.ml_t1_add = RegAdd(self.temp_reg1)
        self.ml_y_sub = RegSub(y)
        self.ml_t2_add = RegAdd(self.temp_reg2)
        self.ml_x_sub = RegSub(x)

        # branch: quotient + 1
        self.quo_q_add = RegAdd(q)
        self.quo_restore_y = EmptyInto(self.temp_reg1, y)
        self.quo_y_sub = RegSub(y)
        self.quo_t2_to_t3 = EmptyInto(self.temp_reg2, self.temp_reg3)

        # branch: exit, and write remainder
        self.rem_t2_sub = RegSub(self.temp_reg2)
        self.rem_write_rem = EmptyInto2(self.temp_reg2, self.temp_reg3, r)
        self.rem_restore_y = EmptyInto(self.temp_reg1, y)
        self.rem_restore_x = EmptyInto(self.temp_reg3, x)

        self.submodules.extend([
            self.check_y_sub, self.check_y_add, self.check_x_to_t4, self.check_write_rem,
            self.ml_t1_add, self.ml_y_sub, self.ml_t2_add, self.ml_x_sub,
            self.quo_q_add, self.quo_restore_y, self.quo_y_sub, self.quo_t2_to_t3,
            self.rem_t2_sub, self.rem_write_rem, self.rem_restore_y, self.rem_restore_x
        ])

        # construct

        # IO
        self.assign_in('in', self.check_y_sub, 'in')
        self.assign_out(self.check_x_to_t4, 'out', 'out_y=0')
        self.assign_out(self.rem_restore_x, 'out', 'out')

        # check
        self.check_y_sub.connect('ne', self.check_y_add, 'in')
        self.check_y_sub.connect('e', self.check_x_to_t4, 'in')
        self.check_x_to_t4.connect('out', self.check_write_rem, 'in')

        # main loop
        self.check_y_add.connect('out', self.ml_t1_add, 'in')
        self.ml_t1_add.connect('out', self.ml_y_sub, 'in')
        self.ml_y_sub.connect('ne', self.ml_t2_add, 'in')
        self.ml_t2_add.connect('out', self.ml_x_sub, 'in')
        self.ml_x_sub.connect('ne', self.ml_t1_add, 'in')

        # quotient branch
        self.ml_y_sub.connect('e', self.quo_q_add, 'in')
        self.quo_q_add.connect('out', self.quo_restore_y, 'in')
        self.quo_restore_y.connect('out', self.quo_y_sub, 'in')
        self.quo_y_sub.connect('e', self.quo_t2_to_t3, 'in')
        self.quo_y_sub.connect('ne', self.quo_t2_to_t3, 'in')
        self.quo_t2_to_t3.connect('out', self.ml_t1_add, 'in')

        # remainder branch
        self.ml_x_sub.connect('e', self.rem_t2_sub, 'in')
        self.rem_t2_sub.connect('e', self.rem_write_rem, 'in')
        self.rem_t2_sub.connect('ne', self.rem_write_rem, 'in')
        self.rem_write_rem.connect('out', self.rem_restore_y, 'in')
        self.rem_restore_y.connect('out', self.rem_restore_x, 'in')
