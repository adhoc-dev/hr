from odoo import fields, models, api, _


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    @api.onchange('employee_id')
    def onchange_employee(self):

        hr_attendance = self.env['hr.attendance']
        for rec in self:

            last_attendance = hr_attendance.search([
                ('employee_id', '=', rec.employee_id.id),
                ('check_in', '!=', False),
                ('check_out', '=', False),
            ])
            check_in_datetime = fields.Datetime.from_string(
                last_attendance.check_in)
            check_in_date = fields.Date.to_string(check_in_datetime)
            total_time_register = self.search([
                ('employee_id', '=', rec.employee_id.id),
                ('date', '=', check_in_date),
            ])
            total_time_register = sum(total_time_register.mapped('unit_amount'))
            current_worked_hours = last_attendance.current_worked_hours
            rec.unit_amount = (current_worked_hours - total_time_register)
