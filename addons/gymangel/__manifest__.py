# -*- coding: utf-8 -*-
{
    'name': "Gimnasio Angel",
    'summary': "Gestión de Gimnasio: Socios, Clases y Reservas",
    'description': """
        Módulo para Práctica 11 SGE.
        Incluye:
        - Gestión de Socios (Herencia)
        - Clases y Actividades
        - Sistema de Reservas con validaciones
        - API REST
    """,
    'author': "Angel",
    'category': 'Sports',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_views.xml',
    ],
    'application': True,
}