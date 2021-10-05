# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime, time
from datetime import timedelta
from openerp.tools.translate import _


class Subject(models.Model):
    _name = "subject"
    _description = "Subject"
    _rec_name = "name_subject"

    id_subject = fields.Char(string='Mã môn học', required=True)
    name_subject = fields.Char(string='Tên môn học', required=True)
    rank = fields.Many2one('coefficient.subject', string="Độ khó môn học")
    coefficient_subject = fields.Float(string='Hệ số môn học', related='rank.coefficient_subject')
    credit = fields.Integer(string='Số tín chỉ', required=True)
    subject_sequence = fields.Char(string='Mã môn học tăng', required=True, copy=False,
                                        readonly=True, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        vals['subject_sequence'] = self.env['ir.sequence'].next_by_code('subject.sequence')
        vals['id_subject'] = vals['subject_sequence'] + str(vals['id_subject'])
        result = super(Subject, self).create(vals)
        return result