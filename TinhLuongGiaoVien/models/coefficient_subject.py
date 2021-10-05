# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime, time
from datetime import timedelta
from openerp.tools.translate import _


class CoefficientSubject(models.Model):
    _name = "coefficient.subject"
    _description = "Coefficient Subject"
    _rec_name = "name_coefficient_subject"

    id_coefficient_subject = fields.Char(string='Mã hệ số môn học', required=True)
    name_coefficient_subject = fields.Char(string='Kiểu hệ số môn học', required=True)
    coefficient_subject = fields.Float(string='Hệ số môn học', required=True)
    coefficient_sequence = fields.Char(string='Mã hệ số môn học tăng', required=True, copy=False,
                                        readonly=True, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        vals['coefficient_sequence'] = self.env['ir.sequence'].next_by_code('coefficient.subject.sequence')
        vals['id_coefficient_subject'] = vals['coefficient_sequence'] + str(vals['id_coefficient_subject'])
        result = super(CoefficientSubject, self).create(vals)
        return result