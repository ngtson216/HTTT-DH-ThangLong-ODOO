# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime, time
from datetime import timedelta
from openerp.tools.translate import _


class CoefficientTeacher(models.Model):
    _name = "coefficient.teacher"
    _description = "Coefficient Teacher"
    _rec_name = "name_coefficient_teacher"

    id_coefficient_teacher = fields.Char(string='Mã hệ số học hàm', required=True)
    name_coefficient_teacher = fields.Char(string='Tên hệ số học hàm', required=True)
    coefficient_teacher = fields.Float(string='Hệ số học hàm', required=True)
    coefficient_sequence = fields.Char(string='Mã hệ số học hàm tăng', required=True, copy=False,
                                        readonly=True, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        vals['coefficient_sequence'] = self.env['ir.sequence'].next_by_code('coefficient.teacher.sequence')
        vals['id_coefficient_teacher'] = vals['coefficient_sequence'] + str(vals['id_coefficient_teacher'])
        result = super(CoefficientTeacher, self).create(vals)
        return result