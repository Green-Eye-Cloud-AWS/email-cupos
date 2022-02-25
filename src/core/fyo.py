#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from .common import Cupo, cupo_base, get_char, get_num, get_string, find, get_date, get_cupo
from .datos_faltantes import cargar_base    

def fyo(soup) -> list[Cupo]:

    cargar_base(soup)

    #
    # Tabla cuerpo
    #

    sp = soup.find_all(style='width:11.25pt;background:#353535;padding:4.5pt 6.0pt 4.5pt 6.0pt')[0]
    for parent in sp.parents:
        if parent.name == 'div':
            sp = parent.parent
            break

    s = find(sp, 'Titular de la carta de porte')
    string = get_string(s, 1)
    cupo_base.cp.titular.nombre = get_char(string)
    cupo_base.cp.titular.cuit = get_num(string)

    s = find(sp, 'Remitente comercial productor')
    string = get_string(s, 1)
    cupo_base.cp.rte_com_prod.nombre = get_char(string)
    cupo_base.cp.rte_com_prod.cuit = get_num(string)

    s = find(sp, 'Remitente comercial venta primaria')
    string = get_string(s, 1)
    cupo_base.cp.rte_com_vta_pri.nombre = get_char(string)
    cupo_base.cp.rte_com_vta_pri.cuit = get_num(string)

    s = find(sp, 'Remitente comercial venta secundaria')
    string = get_string(s, 1)
    cupo_base.cp.rte_com_vta_sec.nombre = get_char(string)
    cupo_base.cp.rte_com_vta_sec.cuit = get_num(string)

    s = find(sp, 'Remitente comercial venta secundaria 2')
    string = get_string(s, 1)
    cupo_base.cp.rte_com_vta_sec_2.nombre = get_char(string)
    cupo_base.cp.rte_com_vta_sec_2.cuit = get_num(string)

    # '*Mercado a Término*'

    s = find(sp, 'Corredor venta primaria')
    string = get_string(s, 1)
    cupo_base.cp.corr_vta_pri.nombre = get_char(string)
    cupo_base.cp.corr_vta_pri.cuit = get_num(string)

    s = find(sp, 'Corredor venta secundaria')
    string = get_string(s, 1)
    cupo_base.cp.corr_vta_sec.nombre = get_char(string)
    cupo_base.cp.corr_vta_sec.cuit = get_num(string)

    s = find(sp, 'Representante / Entregador')
    string = get_string(s, 1)
    cupo_base.cp.repr_entr.nombre = get_char(string)
    cupo_base.cp.repr_entr.cuit = get_num(string)

    s = find(sp, 'Destinatario')
    string = get_string(s, 1)
    cupo_base.cp.destinatario.nombre = get_char(string)
    cupo_base.cp.destinatario.cuit = get_num(string)

    s = find(sp, 'Destino')
    string = get_string(s, 1)
    cupo_base.cp.destino.nombre = get_char(string)
    cupo_base.cp.destino.cuit = get_num(string)

    sp = soup.find_all(style='width:11.25pt;background:#353535;padding:4.5pt 6.0pt 4.5pt 6.0pt')[1]
    for parent in sp.parents:
        if parent.name == 'div':
            sp = parent.parent
            break

    s = find(sp, 'Cosecha')
    cupo_base.cp.cosecha = get_string(s, 1)

    s = find(sp, 'Observaciones')
    cupo_base.cp.observaciones = get_string(s, 1)

    sp = soup.find_all(style='width:11.25pt;background:#353535;padding:4.5pt 6.0pt 4.5pt 6.0pt')[2]
    for parent in sp.parents:
        if parent.name == 'div':
            sp = parent.parent
            break

    s = find(sp, 'Dirección')
    cupo_base.cp.planta.direccion = get_string(s, 1)

    s = find(sp, 'N° Planta (RUCA)')
    cupo_base.cp.planta.nombre = get_num(get_string(s, 1))

    s = find(sp, 'Localidad')
    cupo_base.cp.planta.localidad = get_string(s, 1)

    s = find(sp, 'Provincia')
    cupo_base.cp.planta.provincia = get_char(get_string(s, 1))

    #
    # Tabla cabecera
    #

    s = find(soup, 'Producto')
    cupo_base.cp.producto = get_char(get_string(s, 1))

    s = find(soup, 'Contrato')
    cupo_base.cp.contrato = get_string(s, 1)

    #
    # Cupos
    #

    cupos: list[Cupo] = []

    s = find(soup, 'Fecha de entrega')
    fecha = datetime.strptime(get_date(get_string(s, 1)), r'%d/%m/%Y').strftime(r'%Y-%m-%dT03:00:00Z') 

    if not fecha:
        return cupos

    s = find(soup, 'Códigos')
    codigos = get_string(s, 1).split(' ')

    for codigo in codigos:

        codigo = get_cupo(codigo)

        if codigo:
            cupos.append(Cupo(codigo, fecha))

    return cupos