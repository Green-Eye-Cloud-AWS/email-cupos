#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .common import cupo_base, get_char, get_num, get_string, find

def cargar_base(soup):

    #
    # Datos carta de porte del cupo
    #

    s = find(soup, '*Datos faltantes*')
    if s is None:
        return

    for parent in s.parents:
        if parent.name == 'table':
            soup = parent
            break

    s = find(soup, '*Titular Carta Porte*')
    cupo_base.cp.titular.nombre = get_char(get_string(s, 1))
    cupo_base.cp.titular.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Remitente Comercial Productor*')
    cupo_base.cp.rte_com_prod.nombre = get_char(get_string(s, 1))
    cupo_base.cp.rte_com_prod.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Remitente Comercial Venta Primaria*')
    cupo_base.cp.rte_com_vta_pri.nombre = get_char(get_string(s, 1))
    cupo_base.cp.rte_com_vta_pri.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Remitente Comercial Venta Secundaria*')
    cupo_base.cp.rte_com_vta_sec.nombre = get_char(get_string(s, 1))
    cupo_base.cp.rte_com_vta_sec.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Remitente Comercial Venta Secundaria 2*')
    cupo_base.cp.rte_com_vta_sec_2.nombre = get_char(get_string(s, 1))
    cupo_base.cp.rte_com_vta_sec_2.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Mercado a Término*')
    cupo_base.cp.merc_a_ter.nombre = get_char(get_string(s, 1))
    cupo_base.cp.merc_a_ter.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Corredor Venta Primaria*')
    cupo_base.cp.corr_vta_pri.nombre = get_char(get_string(s, 1))
    cupo_base.cp.corr_vta_pri.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Corredor Venta Secundaria*')
    cupo_base.cp.corr_vta_sec.nombre = get_char(get_string(s, 1))
    cupo_base.cp.corr_vta_sec.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Representante / Entregador*')
    cupo_base.cp.repr_entr.nombre = get_char(get_string(s, 1))
    cupo_base.cp.repr_entr.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Destinatario*')
    cupo_base.cp.destinatario.nombre = get_char(get_string(s, 1))
    cupo_base.cp.destinatario.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Destino*')
    cupo_base.cp.destino.nombre = get_char(get_string(s, 1))
    cupo_base.cp.destino.cuit = get_num(get_string(s, 2))

    s = find(soup, '*Planta*')
    cupo_base.cp.planta.nombre = get_num(get_string(s, 1))

    s = find(soup, '*Dirección*')
    cupo_base.cp.planta.direccion = get_string(s, 1)

    s = find(soup, '*Localidad*')
    cupo_base.cp.planta.localidad = get_string(s, 1)

    s = find(soup, '*Provincia*')
    cupo_base.cp.planta.provincia = get_char(get_string(s, 1))

    s = find(soup, '*Producto*')
    cupo_base.cp.producto = get_char(get_string(s, 1))

    s = find(soup, '*Observaciones*')
    cupo_base.cp.observaciones = get_string(s, 1)

    s = find(soup, '*Cosecha*')
    cupo_base.cp.cosecha = get_string(s, 1)

    s = find(soup, '*Contrato*')
    cupo_base.cp.contrato = get_string(s, 1)

    #
    # Datos del cupo para green eye
    #

    s = find(soup, '*Organización*')
    cupo_base.org = get_char(get_string(s, 1))

    s = find(soup, '*Usuario*')
    cupo_base.user = get_char(get_string(s, 1))

    s = find(soup, '*Entregar a*')
    cupo_base.id_pedido = get_string(s, 1)
