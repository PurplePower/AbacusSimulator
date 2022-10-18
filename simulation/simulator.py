from modules.basic_modules import Module, BasicModule, RegSub, RegAdd


def assign_registers(module: Module, scopes=None, count=1):
    input_regs = module.in_regs
    output_regs = module.out_regs
    other_regs = module.other_regs
    # top_level = scopes is None
    if scopes is None:
        scopes = []
        count = 1
        s = {}
        for i in input_regs:
            assert i not in s
            s[i] = count
            count += 1
        for i in output_regs:
            assert i not in s
            s[i] = count
            count += 1
        for i in other_regs:
            assert i not in s
            s[i] = count
            count += 1

        scopes.append(s)

    if isinstance(module, BasicModule):
        # no more new regs in module
        s = scopes[-1]
        module.actual_reg = s[module.in_regs[0]]
        return scopes

    scopes.append(scopes[-1].copy())  # make a copy for this scope
    s = scopes[-1]

    # set regs assignment in this module
    for r in input_regs + output_regs + other_regs:
        if r not in s:
            s[r] = count
            count += 1

    if not module.submodules:
        print(f'[WARNING] module {module} has no submodules, but not basic module')
    for submodule in module.submodules:
        assign_registers(submodule, scopes, count)

    scopes.pop()
    return scopes


def simulate(module: Module, value_map):
    scopes = assign_registers(module)
    input_assign = scopes[0]

    registers = {
        input_assign[k]: v
        for k, v in value_map.items() if k in input_assign
    }  # default value is 0

    state = module.find_entry(module.in_flows[0])  # TODO more flows
    while True:
        assert isinstance(state, BasicModule)
        reg = state.actual_reg
        if isinstance(state, RegAdd):
            registers[reg] = registers.get(reg, 0) + 1
            state = state.next('out')
            print(f'Reg[{reg}]+ : {registers[reg] - 1} -> {registers[reg]}')
        else:
            if registers.get(reg, 0) > 0:
                registers[reg] -= 1  # reg must be in registers
                state = state.next('ne')
                print(f'Reg[{reg}]- : {registers[reg] + 1} -> {registers[reg]}')
            else:
                # go empty out_flow
                state = state.next('e')
                print(f'Reg[{reg}]- : empty')
        if state is None:
            print('Simulation ends.\n')
            break

    # print registers
    reverse_input_assign = {v: k for k, v in input_assign.items()}
    for r, v in sorted(registers.items(), key=lambda x: x[0]):
        reg_name = reverse_input_assign[r]
        if reg_name.startswith('__'):
            continue  # skip temp reg
        print(f'Reg[{reg_name}]/[{r}] = {v}')

    pass


def export(module: Module, init_values, filename):
    f = open(filename, 'w')

    scopes = assign_registers(module)
    input_assign = scopes[0]

    # export init values
    for reg_name, value in init_values.items():
        if reg_name in input_assign:
            f.write(f'machine.initalizeRegister({input_assign[reg_name]}, {value});\n')

    f.write('\n')

    # get all basic modules
    all_basic_modules = []
    this_layer = [module]
    next_layer = []
    while this_layer:
        for m in this_layer:
            if isinstance(m, BasicModule):
                all_basic_modules.append(m)
            else:
                next_layer.extend(m.submodules)

        this_layer = next_layer
        next_layer = []
        pass

    id_map = {m: i + 1 for i, m in enumerate(all_basic_modules)}  # each module with unique id
    id_map[None] = len(id_map) + 1  # halting module

    for i, m in enumerate(all_basic_modules):
        if isinstance(m, RegAdd):
            f.write(
                f'program.addCode({id_map[m]}, {m.actual_reg}, \'+\', {id_map[m.next("out")]});\n'
            )
        else:
            f.write(
                f'program.addCode({id_map[m]}, {m.actual_reg}, \'-\', '
                f'{id_map[m.next("ne")]}, {id_map[m.next("e")]});\n'
            )

    f.write('\n')
    f.close()
    return id_map, all_basic_modules
