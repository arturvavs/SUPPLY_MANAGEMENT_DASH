sql_p = """
WITH TEMP AS (SELECT
    m.cd_material cd_material,
    m.ds_material ds_material,
    nvl(MAX(obter_consumo_mensal_material('Q', s.cd_estabelecimento, m.cd_material, s.dt_mesano_referencia)),0) consumo_do_mes,
    trunc(nvl(MAX(dividir(obter_consumo_mensal_material('Q', s.cd_estabelecimento, m.cd_material, s.dt_mesano_referencia),
                    decode(s.dt_mesano_referencia,
                           pkg_date_utils.start_of(sysdate, 'mm'),
                           pkg_date_utils.extract_field('DAY', sysdate),
                           pkg_date_utils.extract_field('DAY',
                                                        pkg_date_utils.end_of(s.dt_mesano_referencia, 'MONTH'))))),
        0)) consumo_medio_diario,
    trunc(obter_mat_estabelecimento(l.cd_estabelecimento, l.cd_estabelecimento, m.cd_material, 'CM')) consumo_medio_mensal,
    SUM(obter_saldo_disp_estoque(s.cd_estabelecimento, s.cd_material, s.cd_local_estoque, s.dt_mesano_referencia)) qt_estoque_disp,
    trunc(dividir(SUM(s.qt_estoque),
            AVG(obter_mat_estabelecimento(l.cd_estabelecimento, l.cd_estabelecimento, m.cd_material, 'CM') / 30)))  qt_estoque_dia,
            obter_qt_pendencia_req(l.cd_local_estoque,m.cd_material)qt_req_pendente
FROM
    local_estoque        l,
    unidade_medida       u,
    estrutura_material_v t,
    material             m,
    saldo_estoque        s
WHERE
        m.cd_material = s.cd_material
    AND m.cd_material = t.cd_material
    AND u.cd_unidade_medida = m.cd_unidade_medida_estoque
    AND s.cd_local_estoque = l.cd_local_estoque
    AND s.dt_mesano_referencia = TRUNC(SYSDATE,'MM')
    AND s.cd_estabelecimento = 2
    AND l.cd_local_estoque = '71'
    AND t.cd_grupo_material = :cd_grupo_material
    AND m.ie_padronizado = :ie_padronizado
GROUP BY
    l.cd_estabelecimento,
    l.cd_local_estoque,
    l.ds_local_estoque,
    m.cd_material,
    m.ds_material,
    m.cd_sistema_ant,
    obter_mat_estabelecimento(l.cd_estabelecimento, l.cd_estabelecimento, m.cd_material, 'CM'),
    obter_mat_estabelecimento(l.cd_estabelecimento, l.cd_estabelecimento, m.cd_material, 'PP'),
    substr(obter_desc_loc_material(s.cd_material, s.cd_local_estoque, 'DS'),
           1,
           80),
    substr(obter_desc_loc_material(s.cd_material, s.cd_local_estoque, 'ES'),
           1,
           80),
    substr(obter_dados_material_estab(m.cd_material, l.cd_estabelecimento, 'UME'),
           1,
           30))
    
SELECT 
    rownum as id,
    CD_MATERIAL,
    DS_MATERIAL,
    CONSUMO_DO_MES,
    CONSUMO_MEDIO_DIARIO,
    CONSUMO_MEDIO_MENSAL,
    QT_ESTOQUE_DISP,
    QT_ESTOQUE_DIA,
    QT_REQ_PENDENTE
FROM TEMP
WHERE 1=1
AND ROWNUM <= 100
AND QT_ESTOQUE_DIA BETWEEN 0 AND 8
"""
sql_fornec = """
with temp as (
select 
    distinct
    a.cd_cgc_fornecedor cd_fornecedor,
    hcd_obter_dados_ordem_compra(a.nr_ordem_compra,'F')ds_fornecedor
from ordem_compra a, ordem_compra_item b
where 1=1
and a.nr_ordem_compra = b.nr_ordem_compra
and b.cd_material = :cd_material
and a.dt_baixa is null)
select
    rownum as id,
    cd_fornecedor,
    ds_fornecedor 
from temp
"""

sql_oc = """
select 
    rownum as id,
    a.nr_ordem_compra, 
    to_char(c.dt_prevista_entrega,'dd/mm/yy')dt_prevista_entrega, 
    c.qt_prevista_entrega, nvl(c.qt_real_entrega,0)qt_real_entrega,
    hcd_obter_dados_ordem_compra(a.nr_ordem_compra,'F')ds_fornecedor 
from ordem_compra a, ordem_compra_item b, ordem_compra_item_entrega c
where 1=1
and a.nr_ordem_compra = b.nr_ordem_compra
and b.nr_ordem_compra = c.nr_ordem_compra
and b.nr_item_oci = c.nr_item_oci
and b.cd_material = :cd_material
and a.cd_cgc_fornecedor = :cd_cgc_fornecedor
and ((c.dt_real_entrega is null) or (c.qt_prevista_entrega > nvl(c.qt_real_entrega,0)))
and a.dt_baixa is null
order by c.dt_prevista_entrega asc
"""