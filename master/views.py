# -*- coding: utf-8 -*-

from datetime import datetime
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.query_utils import DeferredAttribute
from django.db.models.expressions import RawSQL

from .models import UserDetail

def _create_json(status=200, status_text=None, data=None):
    return {
        'status_code': status,
        'status_text': status_text or '',
        'data': data or {},
    }

def ping(request):
    return JsonResponse(_create_json(data={
        'timestamp': datetime.now(),
    }))

def _unsupported_operation():
    return JsonResponse(_create_json(status=500, status_text='Unsupported operation'))

#def _generate_user_data(user_inst):
def _generate_user_list(qs):
    return [{
        'id': user.id,
        'username': user.username,
        'email': user.email,

        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,

        'date_joined': user.date_joined,
        'last_login': user.last_login,
    } for user in qs]

def _list_all_fields_in_model(model_class):
    return [field_name for field_name, field in model_class.__dict__.items() if isinstance(field, DeferredAttribute)]

def _get_json_data_from_request(request):
    return json.loads(request.body.decode('utf-8'))

def _assign_all_fields_in_model(model_instance, json_data):
    available_fields = _list_all_fields_in_model(model_instance.__class__)
    for k, v in json_data:
        if k in available_fields:
            setattr(model_instance, k, v)

def _assign_all_fields_in_model_with_request(model_instance, request):
    _assign_all_fields_in_model(model_instance, _get_json_data_from_request(request))

def _select_latest_rows(model_class, target_column_name):
    query_set = model_class.objects
    table_name = model_class._meta.db_table
    raw_sql = '''
    select * from %s group by %s;
    '''
    return query_set.annotate(val=RawSQL(raw_sql, (table_name, target_column_name,)))

################################################################

def users(request):
    if request.method == 'GET':
        qs = get_user_model().objects.all()

        if qs == None:
            return JsonResponse(_create_json(status=404, status_text='No user found'))

        data = {
            # 总页数
            'pages': 1,
            # 每页显示的用户数
            'pagesize': 20,
            # 用户列表
            'users': _generate_user_list(qs),
        }

        return JsonResponse(_create_json(data=data))

    else:
        return _unsupported_operation()

def user(request, userId):
    if request.method == 'OPTIONS':
        return JsonResponse(_create_json(data=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']))

    else:
        # FIXME order_by('ctime')
        #qs = get_user_model().objects.filter(Q(id=userId)).first()
        #ud = UserDetail.objects.filter(Q(user_id=userId)).first()

        try:
            qs = get_user_model().objects
            ur = qs.get(id=userId)
        except ObjectDoesNotExist:
            return JsonResponse(_create_json(status=404,
                    status_text='No user found',
                    data={ 'id': userId, }))
        except MultipleObjectsReturned:
            return JsonResponse(_create_json(status=500,
                    status_text='Too many users found',
                    data={ 'id': userId, 'users': _generate_user_list(qs), }))

        if request.method == 'GET':
            data = {
                'id': userId,
                'username': ur.username,
                'email': ur.email,

                'es_active': ur.is_active,
                'es_staff': ur.is_staff,
                'es_superuser': ur.is_superuser,

                'date_joined': ur.date_joined,
                'last_login': ur.last_login,
            }

            try:
                data['logentry'] = ur.logentry
            except AttributeError:
                pass

            return JsonResponse(_create_json(data=data))

        elif request.method == 'POST':
            data = request.POST['data']
            assert(str(userId) == data['id'])
            # TODO
            return _unsupported_operation()

        elif request.method == 'PUT':
            return _unsupported_operation()

        elif request.method == 'DELETE':
            return _unsupported_operation()

        else:
            return _unsupported_operation()

def join(request):
    return _unsupported_operation()

################################################################

from .models import AbstractMaterial, RealMaterial

def _generate_real_material_data(real_material_inst):
    return {
        'id': real_material_inst.id,
        'material': real_material_inst.material,
        'provider': real_material_inst.provider,
        'part_number': real_material_inst.part_number,
        'guise': real_material_inst.guise,
        'design': real_material_inst.design,
        'photo': real_material_inst.photo,
        'quantity_unit': real_material_inst.quantity_unit,
        'mpq': real_material_inst.mpq,
        'moq': real_material_inst.moq,
        'pp': real_material_inst.pp,
        'commment': real_material_inst.comment,
        'cuid': real_material_inst.cuid,
        'ctime': real_material_inst.ctime,
    }

def _materials_real(request):
    if request.method == 'GET':
        page = 0
        pagesize = 20
        #qs = _select_latest_rows(RealMaterial, 'part_number')[page:page + pagesize]
        qs = RealMaterial.objects.all()

        if qs == None:
            return JsonResponse(_create_json(status=404, status_text='No material found'))

        data = {
            # 总页数
            'pages': page + 1,
            # 每页显示的用户数
            'pagesize': pagesize,
            # 用户列表
            'real_materials': [_generate_real_material_data(material) for material in qs],
        }

        return JsonResponse(_create_json(data=data))

    return _unsupported_operation()

def _materials_abstract(request):
    return _unsupported_operation()

def materials(request, is_real_material):
    if is_real_material == 1:
        return _materials_real(request)

    else:
        return _materials_abstract(request)

def real_material(request, real_material_id):
    if request.method == 'GET':
        try:
            qs = RealMaterial.objects.filter(id=real_material_id).latest()[:1]
            material = qs.get()
            data = {
                'real_material': _generate_real_material_data(material),
            }

        except ObjectDoesNotExist as e1:
            raise e1

        except MultipleObjectsReturned as e2:
            raise e2

        else:
            return JsonResponse(_create_json(data=data))

    elif request.method == 'POST':
        inst = RealMaterial()
        _assign_all_fields_in_model_with_request(inst, request)
        return JsonResponse(_create_json(data=_generate_real_material_data(inst)))

################################################################

def quotations(request):
    pass
