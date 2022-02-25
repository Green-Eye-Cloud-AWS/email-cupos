#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from .common import Cupo, cupo_base, get_char, get_num, get_string, find, get_date, get_cupo
from .datos_faltantes import cargar_base

def zeni(soup) -> list[Cupo]:

    cargar_base(soup)

    #
    # Datos carta de porte del cupo
    #

    s = find(soup, 'Titular Carta Porte:')
    cupo_base.cp.titular.nombre = get_char(get_string(s, 1))
    cupo_base.cp.titular.cuit = get_num(get_string(s, 3))

    s = find(soup, 'Remitente Comercial Productor:')
    cupo_base.cp.rte_com_prod.nombre = get_char(get_string(s, 1))
    cupo_base.cp.rte_com_prod.cuit = get_num(get_string(s, 3))

    s = find(soup, 'Remitente Comercial Venta Primaria:')
    cupo_base.cp.rte_com_vta_pri.nombre = get_char(get_string(s, 1))
    cupo_base.cp.rte_com_vta_pri.cuit = get_num(get_string(s, 3))

    s = find(soup, 'Remitente Comercial Venta Secundaria:')
    cupo_base.cp.rte_com_vta_sec.nombre = get_char(get_string(s, 1))
    cupo_base.cp.rte_com_vta_sec.cuit = get_num(get_string(s, 3))

    s = find(soup, 'Remitente Comercial Venta Secundaria 2:')
    cupo_base.cp.rte_com_vta_sec_2.nombre = get_char(get_string(s, 1))
    cupo_base.cp.rte_com_vta_sec_2.cuit = get_num(get_string(s, 3))

    s = find(soup, 'Mercado a Término:')
    cupo_base.cp.merc_a_ter.nombre = get_char(get_string(s, 1))
    cupo_base.cp.merc_a_ter.cuit = get_num(get_string(s, 3))

    s = find(soup, 'Corredor Venta Primaria:')
    cupo_base.cp.corr_vta_pri.nombre = get_char(get_string(s, 1))
    cupo_base.cp.corr_vta_pri.cuit = get_num(get_string(s, 3))

    s = find(soup, 'Corredor Venta Secundaria:')
    cupo_base.cp.corr_vta_sec.nombre = get_char(get_string(s, 1))
    cupo_base.cp.corr_vta_sec.cuit = get_num(get_string(s, 3))

    # '*Representante / Entregador*'

    s = find(soup, 'Destinatario:')
    cupo_base.cp.destinatario.nombre = get_char(get_string(s, 1))
    cupo_base.cp.destinatario.cuit = get_num(get_string(s, 3))

    s = find(soup, 'Destino:')
    cupo_base.cp.destino.nombre = get_char(get_string(s, 1))
    cupo_base.cp.destino.cuit = get_num(get_string(s, 3))

    s = find(soup, 'Nro. Inscripción:')
    cupo_base.cp.planta.nombre = get_num(get_string(s, 3))

    s = find(soup, 'Destino de los Granos:')
    cupo_base.cp.planta.direccion = get_string(s, 1)

    # '*Localidad*'

    # '*Provincia*'

    s = find(soup, 'Producto:')
    cupo_base.cp.producto = get_char(get_string(s, 1))

    s = find(soup, 'Observaciones:')
    cupo_base.cp.observaciones = get_string(s, 1)

    s = find(soup, 'Cosecha:')
    cupo_base.cp.cosecha = get_string(s, 1)

    s = find(soup, 'Contrato:')
    cupo_base.cp.contrato = get_string(s, 1)

    #
    # Cupos
    #

    cupos: list[Cupo] = []

    s = find(soup, 'Nro.Cupo')
    if s is None:
        return cupos

    for parent in s.parents:
        if parent.name == 'table':
            trs = parent.find_all('tr')

            for i in range(1, len(trs)):
                row = trs[i]
                c1 = get_date(row.find_all('td')[0].get_text(separator=' '))
                if c1:
                    fecha = datetime.strptime(c1, r'%d/%m/%Y').strftime(r'%Y-%m-%dT03:00:00Z')
                cupo = get_cupo(row.find_all('td')[2].get_text(separator=' '))

                if cupo and fecha:
                    cupos.append(Cupo(cupo, fecha))

            break

    return cupos
