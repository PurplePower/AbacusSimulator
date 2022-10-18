class Module:
    def __init__(self, in_regs, out_regs, name=''):
        self.in_regs = in_regs
        self.out_regs = out_regs
        self.other_regs = []

        self.in_flows = []
        self.in_map = {}  # mapping in_flow to a basic module
        self.out_flows = []
        self.out_map = {}  # mapping to the basic module who comes out at out_flow

        self.submodules = []

        self.name = name

    ##########################################################
    #   Internal methods: use when defining module
    ##########################################################

    def assign_in(self, in_flow, submodule, sub_in_flow):
        """
        Assign self module's in_flow to a submodule's in_flow.
        :param in_flow:
        :param submodule:
        :param sub_in_flow:
        :return:
        """
        assert in_flow in self.in_flows
        assert in_flow not in self.in_map
        self.in_map[in_flow] = submodule.find_entry(sub_in_flow)

        pass

    def assign_out(self, submodule, sub_out_flow, out_flow):
        """
        Assign a submodule's out_flow to this module's out_flow.
        :param submodule:
        :param sub_out_flow:
        :param out_flow:
        :return:
        """
        assert out_flow in self.out_flows
        assert out_flow not in self.out_map
        self.out_map[out_flow] = submodule.find_exit(sub_out_flow)

    ##########################################################
    #   External methods: used by whom use this module
    ##########################################################

    def connect(self, out_flow, target_module, target_in_flow):
        """
        Connect self module's out_flow to other module's in_flow.
        :param out_flow:
        :param target_module:
        :param target_in_flow:
        :return:
        """
        assert out_flow in self.out_flows
        # target_basic_module = target_module.find_entry(target_in_flow)
        pair = self.out_map[out_flow]
        pair[0].connect(pair[1], target_module, target_in_flow)

    def find_entry(self, in_flow):
        """
        Find the basic module effectively points by in_flow.
        :param in_flow:
        :return:
        """

        assert in_flow in self.in_flows
        return self.in_map[in_flow]

    def find_exit(self, out_flow):
        """
        Find the basic module who effectively comes out at out_flow.

        :param out_flow:
        :return:
        """
        assert out_flow in self.out_flows
        return self.out_map[out_flow]


class BasicModule(Module):
    def __init__(self, in_reg, out_reg, **kwargs):
        super(BasicModule, self).__init__([in_reg], [out_reg], **kwargs)
        self.actual_reg = -1
        self.next_ = {}

    def connect(self, out_flow, target_module, target_in_flow):
        assert out_flow in self.out_flows
        self.next_[out_flow] = target_module.find_entry(target_in_flow)

    def next(self, out_flow):
        return self.next_.get(out_flow, None)


class RegAdd(BasicModule):
    def __init__(self, reg):
        super().__init__(reg, reg, name=f'{reg}+')

        self.in_flows = ['in']
        self.in_map['in'] = self

        self.out_flows = ['out']
        self.out_map['out'] = (self, 'out')

        # self.name = f'{reg}+'


class RegSub(BasicModule):
    def __init__(self, reg):
        super().__init__(reg, reg, name=f'{reg}-')

        self.in_flows = ['in']
        self.in_map['in'] = self

        self.out_flows = ['e', 'ne']
        for of in self.out_flows:
            self.out_map[of] = (self, of)

        # self.name = f'{reg}-'
