#DEFINIÇÃO DAS COLUNAS QUE SERÃO EXIBIDAS NO GRID, ASSIM COMO ALGUNS PARÂMETROS
columnDefs=[
    #{'headerName': 'ID.', 'field': 'id', "autoHeight": True,"cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},"resizable": False},
    {
        'headerName': 'COD.', 
        'field': 'cd_material', 
        "autoHeight": True,
        "width":'100px',
        "headerStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        #"resizable": False,
        #"cellClass": "center-text"
    },

    {
        'headerName': 'MATERIAL', 
        'field': 'ds_material', 
        "autoHeight": True,
        "width":'350px',
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        #"resizable": False,
    },

    {
        'headerName': 'SALDO', 
        'field': 'qt_estoque_disp', 
        'suppressStickyLabel': True,
        "autoHeight": True,
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        #"resizable": False,
        "headerClass": "center-header",
        "cellClass": "center-cell"
    },

    {
        'headerName': 'C.M DIARIO', 
        'field': 'consumo_medio_diario', 
        "autoHeight": True,
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        #"resizable": False,
        "headerClass": "center-header",
        "cellClass": "center-cell"
    },

    {
        'headerName': 'DIAS COBERTURA', 
        'field': 'qt_estoque_dia', 
        'suppressStickyLabel': True,
        "autoHeight": True,
        "cellStyle": {
            'fontSize': '0.9rem',
            'fontWeight': 'bold',
            "styleConditions": [
                {
                    "condition": "params.data.qt_estoque_dia <= 1",#"condition":"params.data.qt_estoque_dia <= 2 ",
                    "style": {"color": "#d32f2f", "fontSize":"0.9rem", "fontWeight": "bold"}#"style":{"animation": "blink 2s infinite", "fontSize":"0.9rem", "fontWeight": "bold"}
                },
                {
                    "condition": "params.data.qt_estoque_dia >= 2 && params.data.qt_estoque_dia <= 3",#"condition":"params.data.qt_estoque_dia >= 3 && params.data.qt_estoque_dia <= 5 ",
                    "style": {"color": "#f57c00", "fontSize":"0.9rem", "fontWeight": "bold"}#"style":{"backgroundColor": "#FFFD55", "fontSize":"0.9rem", "fontWeight": "bold"}
                }
            ],
            "defaultStyle":{"fontSize":"0.9rem", "fontWeight": "bold"}
            },
        #"resizable": False,
        "headerClass": "center-header",
        "cellClass": "center-cell"
    },

    {
        'headerName': 'C.M MENSAL', 
        'field': 'consumo_medio_mensal', 
        "autoHeight": True,
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        #"resizable": False,
        "headerClass": "center-header",
        "cellClass": "center-cell"
    },

    {
        'headerName': 'QT. REQUISIÇÃO', 
        'field': 'qt_req_pendente', 
        "autoHeight": True,
        "cellStyle": {
            'fontSize': '0.9rem',
            'fontWeight': 'bold',
            "styleConditions": [
                {
                    "condition": "params.data.qt_req_pendente > params.data.qt_estoque_disp",#"condition":"params.data.qt_estoque_dia <= 2 ",
                    "style": {"color": "#d32f2f", "fontSize":"0.9rem", "fontWeight": "bold"}#"style":{"animation": "blink 2s infinite", "fontSize":"0.9rem", "fontWeight": "bold"}
                },
            ],
            "defaultStyle":{"fontSize":"0.9rem", "fontWeight": "bold"}
            },
        #"resizable": False,
        "headerClass": "center-header",
        "cellClass": "center-cell"
    },
    
]

columnDefs_oc=[
    #{'headerName': 'ID.', 'field': 'id', "autoHeight": True,"cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},"resizable": False},
    {
        'headerName': 'OC', 
        'field': 'nr_ordem_compra', 
        "autoHeight": True,
        "width":'120px',
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        "headerClass": "center-header",
        #"resizable": False,
        "cellClass": "center-cell",
    },

    {
        'headerName': 'ENTREGA', 
        'field': 'dt_prevista_entrega', 
        "autoHeight": True,
        "width":'120px',
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        "cellClass": "center-cell",
        "headerClass": "center-header"
        #"resizable": False,
    },

    {
        'headerName': 'PREVISTA', 
        'field': 'qt_prevista_entrega', 
        "autoHeight": True,
        "width":'120px',
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        #"resizable": False,
        "headerClass": "center-header",
        "cellClass": "center-cell"
    },

    {
        'headerName': 'ENTREGUE', 
        'field': 'qt_real_entrega', 
        "autoHeight": True,
        "width":'120px',
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        #"resizable": False,
        "headerClass": "center-header",
        "cellClass": "center-cell"
    },
    
]

columnDefs_fornec=[
    {
        'headerName': 'CNPJ', 
        'field': 'cd_fornecedor', 
        "autoHeight": True,
        "width":'80px',
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        #"resizable": False,
        "headerClass": "center-header",
        "cellClass": "center-cell",
        "hide":True
    },
    {
        'headerName': 'FORNECEDOR', 
        'field': 'ds_fornecedor', 
        "autoHeight": True,
        "cellStyle": {'fontSize': '0.9rem','fontWeight': 'bold'},
        #"resizable": False,
        "headerClass": "center-header",
        "cellClass": "center-cell"
    },
    
]

dashGridOptions={
    #"loadingOverlayComponent": "CustomLoadingOverlay",
    "loadingOverlayComponentParams": {"loadingMessage": "Carregando...",},
    "rowSelection":'single',
    'animateRows':False,
    'multiSortKey': 'ctrl',
    'getRowId': {"function": "params.data.id"},
    #"enableCellTextSelection": True,
    "onColumnResized": {
        "function": """
            function(event) {
                window.columnState = event.columnApi.getColumnState();
            }
        """
    },
    "suppressCellSelection": True,
}
