# -*- coding: utf-8 -*-

from datetime import datetime
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate, login as authLogin, logout as authLogout
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, OuterRef, Subquery, Value as V, Count, Min, Sum, Avg
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.expressions import RawSQL
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import UserDetail

def _create_json(status=200, status_text=None, data=None):
    return {
        'status_code': status,
        'status_text': status_text or '',
        'data': data or {},
    }

@ensure_csrf_cookie
def ping(request):
    return JsonResponse(_create_json(data={
        'timestamp': datetime.now(),
    }))

def _unsupported_operation(data=None):
    return JsonResponse(_create_json(status=500, status_text='Unsupported operation', data=data))

def _generate_user_data(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,

        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,

        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }

def _list_all_fields_in_model(model_class):
    return model_class._meta.get_fields()

def _get_json_data_from_request(request):
    return json.loads(request.body.decode('utf-8'))

def _assign_all_fields_in_model(model_instance, json_data):
    available_fields = _list_all_fields_in_model(model_instance.__class__)
    for k, v in json_data:
        if k in available_fields:
            setattr(model_instance, k, v)

def _assign_all_fields_in_model_with_request(model_instance, request):
    _assign_all_fields_in_model(model_instance, _get_json_data_from_request(request))

def _get_working_company_id(request):
    detail = UserDetail.objects.filter(user=request.user).latest()
    return detail.company_id

################################################################

#@login_required
@ensure_csrf_cookie
def users(request):
    if request.method == 'GET':
        qs = get_user_model().objects.all()

        '''
        SELECT T3.username, T4.gender, T3.first_name, T3.last_name, T3.email, T4.nin, T4.company_id, T3.last_login, T3.date_joined, T4.cuid_id, T4.ctime
        FROM `auth_user` AS T3
        LEFT JOIN (
            SELECT *
            FROM `master_userdetail` AS T2
            WHERE T2.`id` = (SELECT `id`
                        FROM `master_userdetail` AS T1
                        WHERE T1.`user_id` = T2.`user_id`
                        ORDER BY `ctime` DESC
                        LIMIT 1)
        ) AS T4
        ON T3.id = T4.user_id;
        '''

        # TODO
        #UserDetail.objects.filter(user=OuterRef('pk')).order_by('-ctime').values('id')[:1]

        if qs is None:
            return JsonResponse(_create_json(status=404, status_text='No user found'))

        data = {
            # 总页数
            'pages': 1,
            # 每页显示的用户数
            'pagesize': 20,
            # 用户列表
            'users': [_generate_user_data(user) for user in qs],
        }

        return JsonResponse(_create_json(data=data))

    else:
        return _unsupported_operation()

#@login_required
@ensure_csrf_cookie
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
                    data={
                        'id': userId,
                        'users': [_generate_user_data(user) for user in qs],
                    }))

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

################################################################

@ensure_csrf_cookie
def join(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return JsonResponse(_create_json(status=403, status_text='Already logined'))

        _data = _get_json_data_from_request(request)
        _username = _data['username']
        _email = _data['email']
        _password = _data['password']

        _user = get_user_model().objects.create_user(_username, _email, _password)
        _user.save()

        return JsonResponse(_create_json(status=200, status_text='Join successfully'))

    return _unsupported_operation()

@ensure_csrf_cookie
def login(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return JsonResponse(_create_json(status=403, status_text='Already logined', data={
                    'login_state': request.user.is_authenticated,
                }))

        _data = _get_json_data_from_request(request)['data']
        _username = _data['username']
        _password = _data['password']

        # 验证用户名和密码
        user = authenticate(request, username=_username, password=_password)

        if user is not None and user.is_active:
            # 将用户实例附着到会话
            authLogin(request, user)

            return JsonResponse(_create_json(status=200, status_text='Login successfully', data={
                    'login_state': request.user.is_authenticated,
                }))

        return JsonResponse(_create_json(status=401, status_text='Fail to login', data={
                'login_state': request.user.is_authenticated,
            }))

    elif request.method == 'GET':
        login_state = request.user.is_authenticated

        if login_state:
            response_status = 200
            response_status_text = 'Already logined'

        else:
            response_status = 401
            response_status_text = 'Not yet logged in'

        return JsonResponse(_create_json(status=response_status, status_text=response_status_text, data={
                'login_state': login_state,
            }))

    return _unsupported_operation(data={
            'login_state': request.user.is_authenticated,
        })

#@login_required
@ensure_csrf_cookie
def logout(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse(_create_json(status=403, status_text='Not yet logined'))

        authLogout(request)

        return JsonResponse(_create_json(status=200, status_text='Logout successfully'))

    return _unsupported_operation()

#@login_required
@ensure_csrf_cookie
def change_password(request):
    if request.method == 'POST' and request.user.is_active():
        request.user.set_password(new_password)
        return JsonResponse(_create_json(status=200, status_text='Password is changed'))

    return _unsupported_operation()

################################################################

from .models import AbstractMaterial, RealMaterial

def _generate_real_material_data(material):
    return {
        'id': material.id,
        'material': material.material_id,
        'provider': material.provider,
        'part_number': material.part_number,
        'guise': material.guise,
        'design': material.design,
        'photo': material.photo,
        'quantity_unit': material.quantity_unit,
        'mpq': material.mpq,
        'moq': material.moq,
        'pp': material.pp,
        'commment': material.comment,
        'cuid': material.cuid_id,
        'ctime': material.ctime,
    }

#@login_required
@ensure_csrf_cookie
def materials_real(request):
    if request.method == 'GET':
        page = 0
        pagesize = 20

        qs = RealMaterial.objects.filter(pk=Subquery(RealMaterial.objects.filter(material_id__exact=OuterRef('material_id')).order_by(F('ctime').desc(nulls_last=True)).values('pk')[:1]))
        pagelen = qs.aggregate(pagelen=Count(F('pk')))['pagelen']
        qs = qs[page : page + pagesize]

        #print('qs.query:\n', qs.query)

        data = {
            'pages': page + 1,
            'pagelen': pagelen,
            'pagesize': pagesize,
            'real_materials': [_generate_real_material_data(material) for material in qs],
        }

        return JsonResponse(_create_json(data=data))

    return _unsupported_operation()

def _generate_abstract_material_data(material):
    return {
        'id': material.id,
        'material': material.material_id,
        'name': material.name,
        'brand': material.brand,
        'part_number': material.part_number,
        'gauge': material.gauge,
        'comment': material.comment,
        'cuid': material.cuid_id,
        'ctime': material.ctime,
    }

#@login_required
@ensure_csrf_cookie
def materials_abstract(request):
    if request.method == 'GET':
        page = 0
        pagesize = 20

        qs = AbstractMaterial.objects.filter(pk=Subquery(AbstractMaterial.objects.filter(material_id__exact=OuterRef('material_id')).order_by(F('ctime').desc(nulls_last=True)).values('pk')[:1]))
        pagelen = qs.aggregate(pagelen=Count(F('pk')))['pagelen']
        qs = qs[page : page + pagesize]

        #print('qs.query:\n', qs.query)

        data = {
            'pages': page + 1,
            'pagelen': pagelen,
            'pagesize': pagesize,
            'abstract_material': [_generate_abstract_material_data(material) for material in qs],
        }

        return JsonResponse(_create_json(data=data))

    return _unsupported_operation()

#@login_required
@ensure_csrf_cookie
def real_material(request, real_material_id):
    if request.method == 'GET':
        try:
            qs = RealMaterial.objects.filter(id=real_material_id).latest()
            material = qs.get()
            data = {
                'real_material': _generate_real_material_data(material),
            }

        except ObjectDoesNotExist:
            return JsonResponse(_create_json(status=404,
                    status_text='RealMaterial not found',
                    data={ 'id': real_material_id, }))

        except MultipleObjectsReturned:
            return JsonResponse(_create_json(status=500,
                    status_text='Too many materials found',
                    data={
                        'id': real_material_id,
                        'real_materials': [_generate_real_material_data(entry) for entry in qs],
                    }))

        else:
            return JsonResponse(_create_json(data=data))

    elif request.method == 'POST':
        inst = RealMaterial()
        _assign_all_fields_in_model_with_request(inst, request)
        return JsonResponse(_create_json(data=_generate_real_material_data(inst)))

################################################################

from .models import QuotationSheet, QuotationDetail, QuotationPrice

def _select_quotations(request, role):
    query_set = QuotationSheet.objects
    company_id = _get_working_company_id(request)

    if role == 'demander':
        return query_set.filter(demander_id=company_id)
    elif role == 'supplier':
        return query_set.filter(supplier_id=company_id)
    else:
        return None

def _generate_quotation_data(quotation):
    return {
        'id': quotation.id,
        'quotation_number': quotation.quotation_number,
        'demander': quotation.demander_id,
        'supplier': quotation.supplier_id,
        'date_onset': quotation.date_onset,
        'date_offset': quotation.date_offset,
        'cuid': quotation.cuid_id,
        'ctime': quotation.ctime,
    }

#@login_required
@ensure_csrf_cookie
def quotations(request, role):
    if request.method == 'GET':
        page = 0
        pagesize = 20

        db = _select_quotations(request, role)

        if db is None:
            qs = []
            pagelen = 0

        else:
            qs = db.filter(pk=Subquery(db.filter(quotation_number__exact=OuterRef('quotation_number')).order_by(F('ctime').desc(nulls_last=True)).values('pk')[:1]))
            pagelen = qs.aggregate(pagelen=Count(F('pk')))['pagelen']
            qs = qs[page : page + pagesize]

        data = {
            'pages': page + 1,
            'pagelen': pagelen,
            'pagesize': pagesize,
            'quotations': [_generate_quotation_data(quotation) for quotation in qs],
        }

        return JsonResponse(_create_json(data=data))

    return _unsupported_operation()

#@login_required
@ensure_csrf_cookie
def quotation(request, role, quotation_id):
    return _unsupported_operation()
