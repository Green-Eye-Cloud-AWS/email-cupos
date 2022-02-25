#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unicodedata

accents = set(map(unicodedata.lookup, ('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT')))

def find(soup, string):
    soup = soup.find(string=string)
    if soup is None:
        print(f'{string} not found!')
    return soup
        
def get_string(soup, position):
    if soup is None:
        return ''

    for parent in soup.parents:
        if parent.name == 'tr':
            text = parent.find_all('td')[position].get_text(separator=' ')
            text = [c for c in unicodedata.normalize('NFD', text) if c not in accents]
            text = unicodedata.normalize('NFC', ''.join(text))
            # text = unicodedata.normalize('NFD', text).encode('ascii','ignore').decode('ascii')
            text = re.sub('[^A-Za-z0-9-/.ñÑ ]', '', text)
            text = re.sub(' +', ' ', text)
            return text.strip()
    
def get_char(string):
    return re.sub('[^A-Za-z-/. ]', '', string).strip()

def get_num(string):
    return re.sub('[^0-9-]', '', string).strip()

def get_date(string):
    return re.sub('[^0-9-/]', '', string).strip()

def get_cupo(string):
    return re.sub('[^A-Za-z0-9-]', '', string).strip()

def obj_property(name):
    @property
    def prop(self):
        value = getattr(self, name, '')
        if value.strip() == '':
            return None
            # return '-'
        return value

    @prop.setter
    def prop(self, new_value):
        old_value = getattr(self, name, '')
        if old_value.strip() != '':
            return
        if new_value.strip() == '':
            return
        setattr(self, name, new_value)

    return prop

class NC(object):
    nombre = obj_property('_nombre')
    cuit = obj_property('_cuit')

class Planta(object):
    nombre = obj_property('_nombre')
    direccion = obj_property('_direccion')
    localidad = obj_property('_localidad')
    provincia = obj_property('_provincia')

class CP(object):
    titular = NC()
    rte_com_prod = NC()
    rte_com_vta_pri = NC()
    rte_com_vta_sec = NC()
    rte_com_vta_sec_2 = NC()
    merc_a_ter = NC()
    corr_vta_pri = NC()
    corr_vta_sec = NC()
    repr_entr = NC()
    destinatario = NC()
    destino = NC()
    planta = Planta()
    producto = obj_property('_producto')
    observaciones = obj_property('_observaciones')
    cosecha = obj_property('_cosecha')
    contrato = obj_property('_contrato')

class CupoBase(object):
    org = obj_property('_org')
    user = obj_property('_user')
    id_pedido = obj_property('_id_pedido')
    cp = CP()

cupo_base = CupoBase()

class Cupo(object):
    id_cupo = obj_property('_id_cupo')
    fecha_cupo = obj_property('_fecha_cupo')

    def __init__(self, id_cupo, fecha_cupo) -> None:
        self.id_cupo = id_cupo
        self.fecha_cupo = fecha_cupo

    def clean(self, obj):
        if type(obj) == list:
            return [self.clean(e) for e in obj]
        elif type(obj) == dict:
            for k, v in list(obj.items()):
                if v is None:
                    del obj[k]
                else:
                    obj[k] = self.clean(v)
        return obj

    def toJSON(self):
        obj = {
            'id_cupo': self.id_cupo,
            'fecha_cupo': self.fecha_cupo,
            'org': cupo_base.org,
            'user': cupo_base.user,
            'id_pedido': cupo_base.id_pedido,
            'cp': {
                'titular': {
                    'nombre': cupo_base.cp.titular.nombre,
                    'cuit': cupo_base.cp.titular.cuit
                },
                'rte_com_prod': {
                    'nombre': cupo_base.cp.rte_com_prod.nombre,
                    'cuit': cupo_base.cp.rte_com_prod.cuit
                },
                'rte_com_vta_pri': {
                    'nombre': cupo_base.cp.rte_com_vta_pri.nombre,
                    'cuit': cupo_base.cp.rte_com_vta_pri.cuit
                },
                'rte_com_vta_sec': {
                    'nombre': cupo_base.cp.rte_com_vta_sec.nombre,
                    'cuit': cupo_base.cp.rte_com_vta_sec.cuit
                },
                'rte_com_vta_sec_2': {
                    'nombre': cupo_base.cp.rte_com_vta_sec_2.nombre,
                    'cuit': cupo_base.cp.rte_com_vta_sec_2.cuit
                },
                'merc_a_ter': {
                    'nombre': cupo_base.cp.merc_a_ter.nombre,
                    'cuit': cupo_base.cp.merc_a_ter.cuit
                },
                'corr_vta_pri': {
                    'nombre': cupo_base.cp.corr_vta_pri.nombre,
                    'cuit': cupo_base.cp.corr_vta_pri.cuit
                },
                'corr_vta_sec': {
                    'nombre': cupo_base.cp.corr_vta_sec.nombre,
                    'cuit': cupo_base.cp.corr_vta_sec.cuit
                },
                'repr_entr': {
                    'nombre': cupo_base.cp.repr_entr.nombre,
                    'cuit': cupo_base.cp.repr_entr.cuit
                },
                'destinatario': {
                    'nombre': cupo_base.cp.destinatario.nombre,
                    'cuit': cupo_base.cp.destinatario.cuit
                },
                'destino': {
                    'nombre': cupo_base.cp.destino.nombre,
                    'cuit': cupo_base.cp.destino.cuit
                },
                'planta': {
                    'nombre': cupo_base.cp.planta.nombre,
                    'direccion':  cupo_base.cp.planta.direccion,
                    'localidad':  cupo_base.cp.planta.localidad,
                    'provincia':  cupo_base.cp.planta.provincia
                },
                'producto':  cupo_base.cp.producto,
                'observaciones':  cupo_base.cp.observaciones,
                'contrato': cupo_base.cp.contrato,
                'cosecha': cupo_base.cp.cosecha
            }
        }

        return self.clean(obj)
        # return json.dumps(obj)