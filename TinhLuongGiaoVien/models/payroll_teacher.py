# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime, time
from datetime import timedelta
from openerp.tools.translate import _

class PayrollTeacher(models.Model):
    _name = "payroll.teacher"
    _description = "Payroll Teacher"
    _rec_name = "id_payroll_teacher"

    id_payroll_teacher = fields.Char(string='ID Tính lương', readonly=True)
    teacher = fields.Many2one('teacher', string='Giáo viên', required=True)
    semester = fields.Many2one('semester', string="Kỳ học", required=True)
    course_of_teacher = fields.Many2many('cost.of.course.for.teacher', 'id_cocft', string='Các lớp', readonly=True, compute="set_course_of_teacher")
    time = fields.Date(string='Thời gian tính lương', help="Start date",
                                default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                                states={'draft': [('readonly', False)]})
    sum_cost = fields.Float(string="Tổng tiền", readonly=True)
    pay_check = fields.Char(string="Trạng thái", required=True, default='Chưa thanh toán', readonly=True)

    @api.model
    def create(self, vals):
        vals['id_payroll_teacher'] = self.env['ir.sequence'].next_by_code('payroll.teacher.sequence')
        result = super(PayrollTeacher, self).create(vals)
        return result
    
    @api.depends('teacher', 'semester')
    def set_course_of_teacher(self):
        for item in self:
            item.sum_cost = 0
            item.course_of_teacher = []
            data_set = []
            data_default = [6, False]
            data = []
            sum_all_cost = 0
            all_course_of_teacher = self.env['cost.of.course.for.teacher'].search([])
            for rec in all_course_of_teacher:
                if (rec.teacher == item.teacher) and (rec.semester == item.semester):
                    sum_all_cost += rec.sum_payroll
                    data.append(rec.id)
            data_default.append(data)
            data_set.append(data_default)
            item.course_of_teacher = data_set
            item.sum_cost = sum_all_cost


    @api.onchange('teacher', 'semester')
    def change_course_of_teacher(self):
        if self.teacher and self.semester:
            all_course_of_teacher = self.env['cost.of.course.for.teacher'].search([])
            data_set = []
            data_default = [6, False]
            data = []
            for rec in all_course_of_teacher:
                if (rec.teacher == self.teacher) and (rec.semester == self.semester):
                    data.append(rec.id)
            data_default.append(data)
            data_set.append(data_default)
            self.course_of_teacher = data_set

    def change_pay_check(self):
        self.pay_check = "Đã thanh toán"

class ListPayrollTeacher(models.Model):
    _name = "list.payroll.teacher"
    _description = "List Payroll Teacher"
    _rec_name = "id_list_payroll_teacher"

    id_list_payroll_teacher = fields.Char(string='ID Danh sách lương', readonly=True)
    semester = fields.Many2one('semester', string="Kỳ học", required=True)
    course_of_teacher = fields.Many2many('cost.of.course.for.teacher', 'id_cocft', string='Các lớp', compute='set_course_of_teacher')
    time = fields.Date(string='Thời gian tính lương', help="Start date",
                                default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                                states={'draft': [('readonly', False)]})
    sum_cost = fields.Float(string="Tổng tiền", readonly=True)
    pay_check = fields.Char(string="Trạng thái", required=True, default='Chưa thanh toán', readonly=True)     

    @api.model
    def create(self, vals):
        vals['id_list_payroll_teacher'] = self.env['ir.sequence'].next_by_code('list.payroll.teacher.sequence')
        result = super(ListPayrollTeacher, self).create(vals)

        arr_check = []
        all_course_of_teacher = self.env['cost.of.course.for.teacher'].search([])
        for rec in all_course_of_teacher:
            if result.semester == rec.semester:
                if not rec.teacher in arr_check:
                    print(rec.semester)
                    print(vals['semester'])
                    data_payroll_teacher = {
                        'id_payroll_teacher': result.id_list_payroll_teacher,
                        'teacher': rec.teacher.id,
                        'semester': vals['semester'],
                        'time': vals['time']
                    }
                    create_new_payroll_teacher = super(PayrollTeacher, self.env['payroll.teacher']).create(data_payroll_teacher)
                    arr_check.append(rec.teacher)

        return result

    def change_pay_check(self):
        all_payroll_teacher = self.env['payroll.teacher'].search([])
        for rec in all_payroll_teacher:
            if rec.id_payroll_teacher == self.id_list_payroll_teacher:
                rec.pay_check = "Đã thanh toán"
        self.pay_check = "Đã thanh toán"

    @api.depends('semester')
    def set_course_of_teacher(self):
        for item in self:
            sum_all_cost = 0
            item.course_of_teacher = []
            item.sum_cost = 0
            all_course_of_teacher = self.env['cost.of.course.for.teacher'].search([])
            data_set = []
            data_default = [6, False]
            data = []
            for rec in all_course_of_teacher:
                if rec.semester == item.semester:
                    sum_all_cost += rec.sum_payroll
                    data.append(rec.id)
            data_default.append(data)
            data_set.append(data_default)
            item.course_of_teacher = data_set
            item.sum_cost = sum_all_cost


    @api.onchange('semester')
    def change_course_of_teacher(self):
        if self.semester:
            all_course_of_teacher = self.env['cost.of.course.for.teacher'].search([])
            data_set = []
            data_default = [6, False]
            data = []
            for rec in all_course_of_teacher:
                if rec.semester == self.semester:
                    data.append(rec.id)
            data_default.append(data)
            data_set.append(data_default)
            self.course_of_teacher = data_set
