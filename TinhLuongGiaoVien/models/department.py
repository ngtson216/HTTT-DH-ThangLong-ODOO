# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime, time
from datetime import timedelta
from openerp.tools.translate import _

class Department(models.Model):
    _name = "department"
    _description = "Department"
    _rec_name = 'name_department'

    id_department = fields.Char(string='Mã khoa', required=True, copy=False,
                                        readonly=True, index=True, default=lambda self: _('New'))
    name_department = fields.Char(string='Tên khoa', required=True)
    short_name = fields.Char(string='Tên khoa viết tắt', required=True)
    time_open = fields.Date(string='Thời gian mở khoa', help="Start date",
                            default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                            states={'draft': [('readonly', False)]})
    description = fields.Text(string="Mô tả")

    @api.model
    def create(self, vals):
        if vals.get('id_department', _('New')) == _('New'):
            vals['id_department'] = self.env['ir.sequence'].next_by_code('department.sequence') or _('New')
        result = super(Department, self).create(vals)
        return result