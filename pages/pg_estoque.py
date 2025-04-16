import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_ag_grid import AgGrid
import pandas as pd
import database
from sql import sql_p, sql_fornec, sql_oc
from datetime import datetime
from database import get_data, get_data_fornecedor, get_data_oc
from AgGridParams import columnDefs, columnDefs_oc, columnDefs_fornec, dashGridOptions
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path='/', name='Gestão de Estoque')

# Mapeamento para valores do grupo de material
grupo_material_map = {
    'todos': 1,
    'medicamentos': 2,
    'materiais_medicos': 3,
    'insumos': 4
}

layout = html.Div([
    html.Div([
        html.Img(id='logo', src='/assets/logo_branca.png', className='logo-vazada'),
        html.H1('SALDO DE ESTOQUE PARA RESSUPRIMENTO', className='titulo'),
        html.H2(' ', className='subtitulo'),
    ], className='header'),
    
    html.Div([
        html.Div([
            html.Div([
                html.H2("Materiais e medicamentos", className="panel-title"),
                html.Div([
                    html.Img(id='open-filter', src='/assets/tdesign--filter-filled.png', className="filter-icon"),
                    # Painel de filtro expansível
                    html.Div([
                        html.Label("Grupo"),
                        dcc.Dropdown(
                            id='dropdown-filtro',
                            options=[
                                {'label': 'Drogas e Medicamentos', 'value': 1},
                                {'label': 'Materiais de Uso do Paciente', 'value': 4}
                            ],
                            value=1,
                            style={'fontSize':'16px','fontWeight':'normal','color':'black','marginTop':'0.5rem'},
                            clearable=False,
                            className="filter-dropdown"
                        ),
                        html.Label("Padronizado"),
                        dcc.RadioItems(
                            id='radio-filtro',
                            options=[
                                {'label': 'Padronizado', 'value': 'S'},
                                {'label': 'Não Padronizado', 'value': 'N'}
                            ],
                            value='S',
                            inputStyle={'marginRight': '5px'},
                            inline=True,
                            className="filter-radio"
                        ),
                        html.Button("Aplicar", id="btn-aplicar-filtro", className="filter-button")
                    ], id='painel-filtro', className="filter-panel")
                ], className="filter-icon-container")
            ], className="title-container"),
            
            # AG Grid
            html.Div([
                AgGrid(
                    id='tabela-estoque',
                    columnDefs=columnDefs,
                    dashGridOptions=dashGridOptions,
                    dangerously_allow_code=True,
                    columnSize="responsiveSizeToFit",
                    style={"width": "100%", "height": "700px"},
                )
            ]),
            
        ], className="data-panel", style={"flex": "3"}),
        
        html.Div([
            html.Div([
                html.Div([
                    html.H2("Fornecedores", className="panel-title-right"),
                ], className="title-container-right"),
                AgGrid(
                    id='tabela-fornec',
                    columnDefs=columnDefs_fornec,
                    dashGridOptions=dashGridOptions,
                    dangerously_allow_code=True,
                    columnSize="responsiveSizeToFit",
                    style={"width": "100%", "height": "200px"},
                )
            ]),

            html.Div([
                html.Div([
                    html.H2("Ordem de Compra", className="panel-title-right"),
                ], className="title-container-right"),
                AgGrid(
                    id='tabela-oc',
                    columnDefs=columnDefs_oc,
                    dashGridOptions=dashGridOptions,
                    dangerously_allow_code=True,
                    columnSize="responsiveSizeToFit",
                    style={"width": "100%", "height": "400px"},
                )
            ]),
            
        ], className="data-panel-right", style={"flex": "1", 'display': 'flex', 'flex-direction': 'column'})
    ], style={"display": "flex", "gap": "15px", "margin": "20px"}),
    
    # Intervalo para atualização
    dcc.Interval(
        id='interval-component-1',
        n_intervals=0,
        interval=240*1000
    ),
    dcc.Store(
        id='cd-material'
    ),
], className='container')

@callback(
    Output('painel-filtro', 'style'),
    [Input('open-filter', 'n_clicks'),
     Input('btn-aplicar-filtro', 'n_clicks')],
    [State('painel-filtro', 'style')],
    prevent_initial_call=True
)
def toggle_filter_panel(n_open, n_apply, current_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    
    # Se o estilo atual for None, inicialize com um dicionário vazio
    current_style = current_style or {}
    
    # Clone o dicionário de estilo atual
    style = dict(current_style)
    
    # Alterne entre mostrar e ocultar
    if style.get('display') == 'block':
        style['display'] = 'none'
    else:
        style['display'] = 'block'
    
    return style

@callback(
    Output('tabela-estoque', 'rowData'),
    [Input('interval-component-1', 'n_intervals'),
     Input('btn-aplicar-filtro', 'n_clicks')],
    [State('dropdown-filtro', 'value'),
     State('radio-filtro', 'value')],
)
def update_data(n_intervals, n_clicks, grupo_material, ie_padronizado):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    if trigger == 'btn-aplicar-filtro' and n_clicks:
        # Aplicar filtros quando o botão for clicado
        data = get_data(sql_p, grupo_material, ie_padronizado)
    else:
        # Atualização periódica ou carregamento inicial
        data = get_data(sql_p, 1, 'S')
    
    return data.to_dict('records')

@callback(
    Output('tabela-fornec', 'rowData'),
    Output('cd-material', 'data'),
    Input('tabela-estoque', 'selectedRows')   
)
def load_fornecedor(selectedRows):
    data = pd.DataFrame()
    cd_material = None
    if selectedRows:
        cd_material = selectedRows[0]['cd_material']
        data = get_data_fornecedor(sql_fornec, cd_material)
    return data.to_dict('records'), cd_material

@callback(
    Output('tabela-oc', 'rowData'),
    Input('tabela-fornec', 'selectedRows'),
    Input('cd-material', 'data'),
)
def load_oc(selectedRows, cd_material):
    data = pd.DataFrame()
    
    if selectedRows and cd_material:
        try:
            cd_fornecedor = str(selectedRows[0]['cd_fornecedor'])
            data = get_data_oc(sql_oc, cd_material, cd_fornecedor)
        except Exception as e:
            print(f"Erro ao carregar OCs: {e}")
    
    return data.to_dict('records')