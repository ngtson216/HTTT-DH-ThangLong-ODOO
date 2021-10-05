# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime, time
from datetime import timedelta
from openerp.tools.translate import _


class Teacher(models.Model):
    _name = "teacher"
    _description = "Professor Teacher"
    _rec_name = "name_teacher"

    employee_id = fields.Many2one('hr.employee', string='Nhân viên', required=True, 
                                 help="Employee",
                                states={'draft': [('readonly', False)]})
    id_teacher = fields.Char(string='Mã giảng viên', required=True)
    name_teacher = fields.Char(string='Tên giảng viên', required=True)
    gender = fields.Selection([
        ('nam', 'Nam'),
        ('nữ', 'Nữ'),
        ('khác', 'Khác'),
    ], required=True, default='male', string="Giới tính")
    age = fields.Integer(string='Tuổi', default=20)
    rank = fields.Many2one('coefficient.teacher', string="Tên hàm học")
    coefficient_teacher = fields.Float(string='Hệ số hàm học', related='rank.coefficient_teacher')
    name_department = fields.Many2one('department', string="Tên khoa")
    id_department = fields.Char(string='Mã khoa', related='name_department.id_department')
    teacher_sequence = fields.Char(string='Mã hệ số', required=True, copy=False,
                                        readonly=True, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        vals['teacher_sequence'] = self.env['ir.sequence'].next_by_code('professor.sequence')
        vals['id_teacher'] = vals['teacher_sequence'] + str(vals['id_teacher'])
        result = super(Teacher, self).create(vals)
        return result