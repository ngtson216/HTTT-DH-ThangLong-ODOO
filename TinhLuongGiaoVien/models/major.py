# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime, time
from datetime import timedelta
from openerp.tools.translate import _

class Major(models.Model):
    _name = "department.major"
    _description = "Department Major"
    _rec_name = 'name_major'

    id_major = fields.Char(string='Mã ngành', required=True)
    name_major = fields.Char(string='Tên ngành', required=True)
    short_name = fields.Char(string='Tên ngành viết tắt', required=True)
    name_department = fields.Many2one('department', string="Tên khoa")
    id_department = fields.Char(string='Mã khoa', related='name_department.id_department')
    time_open = fields.Date(string='Thời gian mở ngành', required=True, help="Start date",
                            default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                            states={'draft': [('readonly', False)]})
    major_sequence = fields.Char(string='Mã ngành tự động', required=True, copy=False,
                                        readonly=True, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        vals['major_sequence'] = self.env['ir.sequence'].next_by_code('department.major.sequence') or _('New')
        vals['id_major'] = vals['major_sequence'] + str(vals['id_major'])
        result = super(Major, self).create(vals)
        return result
