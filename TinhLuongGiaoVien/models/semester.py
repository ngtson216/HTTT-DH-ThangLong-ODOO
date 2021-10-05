# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime, time
from datetime import timedelta
from openerp.tools.translate import _


class Semester(models.Model):
    _name = "semester"
    _description = "Semester"
    _rec_name = "name_semester"

    id_semester = fields.Char(string='Mã kỳ', required=True)
    name_semester = fields.Char(string='Tên kỳ học', required=True)
    time_open = fields.Date(string='Thời gian mở', help="Start date",
                        default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                        states={'draft': [('readonly', False)]})
    time_close = fields.Date(string='Thời gian kết thúc', help="Start date",
                        default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                        states={'draft': [('readonly', False)]})