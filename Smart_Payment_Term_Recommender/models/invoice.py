# -*- coding: utf-8 -*-
# Part of Creyox Technologies.
from odoo import models, fields, api
from datetime import date


class AccountMove(models.Model):
    _inherit = ['account.move']

    @api.onchange('partner_id')
    def calculate_customer_invoice_score(self):
        customer_invoices = self.env['account.move'].search([('partner_id', '=', self.partner_id.id), ('payment_reference', '!=', None)])
        payment_matrices = self.env['payment.term.matrix.rule'].search([])
        for matrix in payment_matrices:
            match matrix.matrix_id.id:
                case 1:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # average_days_score = self.cal_avg_days_to_pay(customer_invoices, rules)
                case 2:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # on_time_score = self.on_time_percent(customer_invoices, rules)
                case 3:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # overdue_invoice_score = self.overdue_invoice_count(customer_invoices, rules)
                case 4:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    oldest_overdue_invoice_score = self.oldest_overdue_age(customer_invoices, rules)
                case 5:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.order_frequency_monthly(customer_invoices, rules)
                case 6:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.sales_volume_6mo(customer_invoices, rules)
                case 7:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.outstanding_balance(customer_invoices, rules)
                case 8:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.credit_note_ratio(customer_invoices, rules)
                case 9:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.days_since_last_payment(customer_invoices, rules)
                case 10:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.first_sale_age(customer_invoices, rules)
                case 11:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.avg_order_value(customer_invoices, rules)
                case 12:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.dispute_count(customer_invoices, rules)
                case 13:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.return_rate(customer_invoices, rules)
                case 14:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.payment_bounce_count(customer_invoices, rules)
                case 15:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.invoice_volume_monthly(customer_invoices, rules)

    def find_invoice_payment_date(self, invoice):
        if invoice :
            payment_date = []
            invoice_name = invoice.payment_reference
            payment_refs = self.env['account.move'].search([('ref', '=', invoice_name)])
            for ref in payment_refs:
                payment_date.append(ref.create_date)
            return max(payment_date).date()

    def verify_rules(self, rules, value):
        for rule in rules:
            if rule.operator == 'lt':
                if value < rule.value_1:
                    return rule.score

            elif rule.operator == 'le':
                if value <= rule.value_1:
                    return rule.score

            elif rule.operator == 'gt':
                if value > rule.value_1:
                    return rule.score

            elif rule.operator == 'ge':
                if value >= rule.value_1:
                    return rule.score

            elif rule.operator == 'eq':
                if value == rule.value_1:
                    return rule.score
            else:
                if value >= rule.value_1 and value <= rule.value_2:
                    return rule.score

    def cal_avg_days_to_pay(self, invoices, rules):
        """
        This method calculates the customer payment score based on average score of each invoice's score
        """
        if len(list(invoices)):
            total_score = 0
            per_invoice_score = []
            counter = 0
            total_paid_invoices = 0
            for invoice in invoices:
                payment_date = []
                if invoice.payment_state == 'paid':
                    total_paid_invoices += 1
                    invoice_confirm_date = invoice.create_date.date()
                    payment_date = self.find_invoice_payment_date(invoice)
                    days_to_pay = (payment_date - invoice_confirm_date).days
                    per_invoice_score.append(self.verify_rules(rules, days_to_pay))
            total_score = sum(per_invoice_score) / total_paid_invoices
            return total_score


    def on_time_percent(self, invoices, rules):
        """
        This method calculates the score based on percentage of payment done before due date.
        """
        if len(list(invoices)):
            total_paid_invoices = 0
            on_time_invoices = 0
            for invoice in invoices:
                if invoice.payment_state == 'paid':
                    total_paid_invoices += 1
                    invoice_due_date = invoice.invoice_date_due
                    payment_date = self.find_invoice_payment_date(invoice)
                    if payment_date <= invoice_due_date:
                        on_time_invoices += 1
            try:
                ontime_invoice_percentage = (100 * on_time_invoices) / total_paid_invoices
                return self.verify_rules(rules, ontime_invoice_percentage)
            except ZeroDivisionError:
                return "no records"

    def overdue_invoice_count(self, invoices, rules):
        """
        This method calculate customer score based on overdue invoice payments
        """
        if len(list(invoices)):
            overdue_invoices = 0
            flag = 0
            for invoice in invoices:
                if invoice.payment_state == 'paid':
                    invoice_due_date = invoice.invoice_date_due
                    payment_date = self.find_invoice_payment_date(invoice)
                    flag = 1 # indicates that some invoices are paid
                    if payment_date > invoice_due_date:
                        overdue_invoices += 1
            if flag:
                return self.verify_rules(rules, overdue_invoices)
            else:
                return "no records"


    def oldest_overdue_age(self, invoices, rules):
        """
        This method calculate customer score based the oldest overdue invoice payment
        """
        if len(list(invoices)):
            days = None
            flag = 0
            oldest_paid_invoice = 0
            max_date = None
            for invoice in invoices:
                if invoice.payment_state == 'paid':
                    payment_date = self.find_invoice_payment_date(invoice)
                    if payment_date > invoice.invoice_date_due:
                        max_date = payment_date
                        break

            for invoice in invoices:
                if invoice.payment_state == 'paid':
                    payment_date = self.find_invoice_payment_date(invoice)
                    if payment_date > invoice.invoice_date_due:
                        flag = 1
                        if max_date <= payment_date:
                            max_date = payment_date
                            oldest_paid_invoice = invoice
                            days = (payment_date - invoice.invoice_date_due).days

            if flag:
                return self.verify_rules(rules, days)
            else :
                return "no record"


    def order_frequency_monthly(self, invoices, rules):
        if len(list(invoices)):


    def sales_volume_6mo(self, invoices, rules):
        if len(list(invoices)):
            pass

    def outstanding_balance(self, invoices, rules):
        if len(list(invoices)):
            pass

    def credit_note_ratio(self, invoices, rules):
        if len(list(invoices)):
            pass

    def days_since_last_payment(self, invoices, rules):
        if len(list(invoices)):
            pass

    def first_sale_age(self, invoices, rules):
        if len(list(invoices)):
            pass

    def avg_order_value(self, invoices, rules):
        if len(list(invoices)):
            pass

    def dispute_count(self, invoices, rules):
        if len(list(invoices)):
            pass

    def return_rate(self, invoices, rules):
        if len(list(invoices)):
            pass

    def payment_bounce_count(self, invoices, rules):
        if len(list(invoices)):
            pass

    def invoice_volume_monthly(self, invoices, rules):
        if len(list(invoices)):
            pass
