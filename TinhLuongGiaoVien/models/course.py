# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime, time
from datetime import timedelta
from openerp.tools.translate import _
import json

class CostOfCourseForTeacher(models.Model):
    _name = 'cost.of.course.for.teacher'
    _description = "Cost Of Course For Teacher"
    _rec_name = "id_cocft"

    id_cocft = fields.Char(string='Mã', readonly=True)
    semester = fields.Many2one('semester', string="Kỳ học", readonly=True)
    teacher = fields.Many2one('teacher', string="Giảng viên", readonly=True)
    coefficient_teacher = fields.Float(string='Hệ số học hàm', related='teacher.coefficient_teacher', readonly=True)
    subject = fields.Many2one('subject', string="Môn học", readonly=True)
    coefficient_subject = fields.Float(string='Hệ số môn học', related='subject.coefficient_subject', readonly=True)
    credit = fields.Integer(string='Số tín chỉ', related='subject.credit', readonly=True)
    teaching_time = fields.Integer(string="Số tiết", readonly=True)
    number_of_students = fields.Integer(string="Số học sinh", readonly=True)
    original_payroll = fields.Float(string="Lương cơ bản",readonly=True, default=200000)

    coefficient_students = fields.Float(string="Hệ số học sinh", readonly=True)
    sum_coefficient = fields.Float(string="Tổng hệ số", readonly=True)
    sum_payroll = fields.Float(string="Tổng tiền lương", readonly=True)

    @api.model
    def create(self, vals):
        vals['id_cocft'] = self.env['ir.sequence'].next_by_code('cost.course.sequence')
        result = super(CostOfCourseForTeacher, self).create(vals)
        return result

class Course(models.Model):
    _name = "course"
    _description = "Course"
    _rec_name = "name_course"

    id_course = fields.Char(string='Mã lớp học', readonly=True)
    name_course = fields.Char(string='Tên lớp học', required=True)
    semester = fields.Many2one('semester', string="Kỳ học")

    teacher = fields.Many2one('teacher', string="Giảng viên", required=True)
    department_of_teacher = fields.Many2one('department', string='Khoa', related='teacher.name_department', readonly=True)
    rank_teacher = fields.Many2one('coefficient.teacher', string='Học hàm giáo viên', related='teacher.rank', readonly=True)
    coefficient_teacher = fields.Float(string='Hệ số học hàm', related='teacher.coefficient_teacher', readonly=True)

    subject = fields.Many2one('subject', string="Môn học", required=True)
    credit = fields.Integer(string='Số tín chỉ', related='subject.credit', readonly=True)
    rank_subject = fields.Many2one('coefficient.subject', string='Độ khó', related='subject.rank', readonly=True)
    coefficient_subject = fields.Float(string='Hệ số môn học', related='subject.coefficient_subject', readonly=True)

    teaching_time = fields.Integer(string="Số tiết", required=True)
    number_of_students = fields.Integer(string="Số học sinh", required=True)

    @api.model
    def create(self, vals):
        vals['id_course'] = self.env['ir.sequence'].next_by_code('course.sequence')
        vals['id_course'] = str(vals['name_course']) + vals['id_course']
        result = super(Course, self).create(vals)

        coefficient_students = 0
        if result.number_of_students < 20:
            coefficient_students = -0.5
        elif (result.number_of_students >= 20 and result.number_of_students <= 40):
            coefficient_students = 0
        else:
            coefficient_students = 0.2
        sum_coefficient = result.teaching_time * (coefficient_students + result.coefficient_subject + result.coefficient_teacher)
        sum_payroll = 200000 * sum_coefficient

        data_cost = {
            'id_cocft': result.id_course,
            'semester': vals['semester'],
            'teacher': vals['teacher'],
            'subject': vals['subject'],
            'teaching_time': vals['teaching_time'],
            'number_of_students': vals['number_of_students'],
            'coefficient_students': coefficient_students,
            'sum_coefficient': sum_coefficient,
            'sum_payroll': sum_payroll
        }
        create_new_cost_course = super(CostOfCourseForTeacher, self.env['cost.of.course.for.teacher']).create(data_cost)
        return result

    