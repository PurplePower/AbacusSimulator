import dash
import dash_cytoscape as cyto
import dash_html_components as html
from modules.basic_modules import RegAdd, RegSub
from modules.EmptyInto import EmptyInto, EmptyInto2
from modules.Additon import Addition
from modules.Multiplication import Multiplication
from modules.ReLU import ReLU
from modules.ModRem import ModRem
from simulation.simulator import simulate, export

if __name__ == '__main__':
    ####################
    #   run simulation
    ####################

    # mod = EmptyInto('m', 'n')
    # mod = EmptyInto2('r', 't1', 't2')
    # mod = Addition('m', 'n', name='my addition')
    # mod = Multiplication('m', 'r', 'n')
    mod = ReLU('x', 'y', 'z')
    # mod = ModRem('x', 'y', 'r', 'q')
    init_values = {
        'x': 5,
        'y': 3,
        # 'z': 0,
        'q': 0,
        'r': 0
    }

    simulate(mod, init_values)

    #######################
    #   export instructions & graph
    #######################

    filename = 'diff.txt'
    id_map, basic_modules = export(mod, init_values, filename)
    print(f'Exported to {filename}')

    # actual_module_names = [
    #     f'[{m.actual_reg}]+' if isinstance(m, RegAdd) else f'[{m.actual_reg}]-'
    #     for m in basic_modules
    # ]
    #
    # app = dash.Dash('My module')
    #
    # nodes = [
    #     {'data': {'id': str(id_map[m]), 'label': actual_module_names[i]}}
    #     for i, m in enumerate(basic_modules)
    # ]
    #
    # edges = []
    # for i, m in enumerate(basic_modules):
    #     edges.extend([
    #         {'data': {'source': str(id_map[m]), 'target': str(id_map[m.next(out)]), 'label': out}}
    #         for out in ['e', 'ne', 'out'] if m.next(out) is not None
    #     ])
    #
    # app.layout = html.Div([
    #     cyto.Cytoscape(
    #         id='Diff abacus',
    #         layout={'name': 'grid'},
    #         style={'width': '100%', 'height': '1000px'},
    #         elements=nodes + edges,
    #         stylesheet=[
    #             {
    #                 "selector": 'edge',
    #                 "style": {
    #                     "width": 5,
    #                     "targetArrowShape": 'triangle',
    #                     "curveStyle": 'bezier',
    #                     'label': 'data(label)'
    #                 }
    #             },
    #             {
    #                 'selector': 'node',
    #                 'style': {
    #                     'content': 'data(label)'
    #                 }
    #             },
    #         ],
    #     )
    # ])
    #
    # app.run_server(debug=True)
