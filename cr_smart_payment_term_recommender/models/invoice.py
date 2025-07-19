# -*- coding: utf-8 -*-
# Part of Creyox Technologies.
from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class AccountMove(models.Model):
    _inherit = ['account.move']

    @api.onchange('partner_id')
    def calculate_customer_invoice_score(self):
        customer_invoices = self.env['account.move'].search(
            [('partner_id', '=', self.partner_id.id), ('payment_reference', '!=', None), ('state', '=', 'posted')])
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
                    # oldest_overdue_invoice_score = self.oldest_overdue_age(customer_invoices, rules)
                case 5:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # self.order_frequency_monthly(customer_invoices, rules)
                case 6:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # self.sales_volume_6mo(customer_invoices, rules)
                case 7:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # self.outstanding_balance(customer_invoices, rules)
                case 8:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # self.credit_note_ratio(customer_invoices, rules)
                case 9:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # self.days_since_last_payment(customer_invoices, rules)
                case 10:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # self.first_sale_age(customer_invoices, rules)
                case 11:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # self.avg_order_value(customer_invoices, rules)
                case 12:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # self.dispute_count(customer_invoices, rules)
                case 13:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # self.return_rate(customer_invoices, rules)
                case 14:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    # self.payment_bounce_count(customer_invoices, rules)
                case 15:
                    rules = self.env['payment.term.matrix.rule.line'].search([('rule_id', '=', matrix.matrix_id.id)])
                    self.invoice_volume_monthly(customer_invoices, rules)

    def find_invoice_payment_date(self, invoice):
        if invoice:
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
        else:
            return "new customer"

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
        else:
            return "new customer"

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
                    flag = 1  # indicates that some invoices are paid
                    if payment_date > invoice_due_date:
                        overdue_invoices += 1
            if flag:
                return self.verify_rules(rules, overdue_invoices)
            else:
                return "no records"
        else:
            return "new customer"

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
            else:
                return "no record"
        else:
            return "new customer"

    def order_frequency_monthly(self, invoices, rules):
        """
        This method calculates the customer score based on average confirmed orders for last 6 months
        """
        if len(list(invoices)):
            months = 6
            current_date = date.today()
            monthly_dates = [current_date - relativedelta(months=months)]
            while months:
                monthly_dates.append((monthly_dates[6 - months] + relativedelta(months=1)))
                months -= 1
            monthly_order_frequency = [0, 0, 0, 0, 0, 0]
            for invoice in invoices:
                if invoice.invoice_date >= monthly_dates[0] and invoice.invoice_date <= monthly_dates[1]:
                    monthly_order_frequency[0] += 1

                elif invoice.invoice_date > monthly_dates[1] and invoice.invoice_date <= monthly_dates[2]:
                    monthly_order_frequency[1] += 1

                elif invoice.invoice_date > monthly_dates[2] and invoice.invoice_date <= monthly_dates[3]:
                    monthly_order_frequency[2] += 1

                elif invoice.invoice_date > monthly_dates[3] and invoice.invoice_date <= monthly_dates[4]:
                    monthly_order_frequency[3] += 1

                elif invoice.invoice_date > monthly_dates[4] and invoice.invoice_date <= monthly_dates[5]:
                    monthly_order_frequency[4] += 1

                else:
                    monthly_order_frequency[5] += 1

            average_order_frequency = sum(monthly_order_frequency) / len(monthly_order_frequency)
            return self.verify_rules(rules, average_order_frequency)
        else:
            return "new customer"

    def sales_volume_6mo(self, invoices, rules):
        """
        This method calculates the customer score based on amount of total confirmed sales in last 6 months
        """
        if len(list(invoices)):
            months = 6
            current_date = date.today()
            six_months_before_date = current_date - relativedelta(months=months)
            six_months_sales = 0
            for invoice in invoices:
                if invoice.invoice_date >= six_months_before_date and invoice.invoice_date <= current_date:
                    six_months_sales += invoice.amount_total
            return self.verify_rules(rules, six_months_sales)
        else:
            return "new customer"

    def outstanding_balance(self, invoices, rules):
        """
        This method calculates the customer score based on Unpaid amount from all open invoices
        """
        if len(list(invoices)):
            outstanding_balance = 0
            new_customer = 1
            for invoice in invoices:
                new_customer = 0
                if invoice.payment_state != 'paid':
                    outstanding_balance += invoice.amount_residual
            if new_customer:
                return "no record"
            return self.verify_rules(rules, outstanding_balance)
        else:
            return "new customer"

    def credit_note_ratio(self, invoices, rules):
        """
        This method calculates the customer score based on the ratio of refund invoices to total invoices
        """
        if len(list(invoices)):
            reversed_invoices = 0
            score = 0
            no_reversed = 0
            for invoice in invoices:
                if invoice.payment_state == 'reversed':
                    no_reversed = 1
                    reversed_invoices += 1
            reversed_invoices_percentage = (reversed_invoices * 100) / len(list(invoices))
            if no_reversed:
                return self.verify_rules(rules, reversed_invoices_percentage)
            return "no record"
        else:
            return "new customer"

    def days_since_last_payment(self, invoices, rules):
        """
        This method calculates the customer score based on number of days since the last invoice paid
        """
        if len(list(invoices)):
            days = None
            flag = 0
            max_date = None
            for invoice in invoices:
                if invoice.payment_state == 'paid':
                    max_date = self.find_invoice_payment_date(invoice)
                    break
            for invoice in invoices:
                if invoice.payment_state == 'paid':
                    payment_date = self.find_invoice_payment_date(invoice)
                    flag = 1
                    if max_date <= payment_date:
                        max_date = payment_date
                        days = (date.today() - payment_date).days
            if flag:
                return self.verify_rules(rules, days)
            else:
                return "no record"
        else:
            return "new customer"

    def first_sale_age(self, invoices, rules):
        """
        This method calculates the customer score based on days since the first invoice
        """
        if len(list(invoices)):
            first_invoice_age = None
            no_invoices = 1
            min_date = None
            for invoice in invoices:
                if invoice.payment_state == 'paid':
                    no_invoices = 0
                    min_date = self.find_invoice_payment_date(invoice)
                    break
            for invoice in invoices:
                if invoice.payment_state == 'paid':
                    payment_date = self.find_invoice_payment_date(invoice)
                    if min_date >= payment_date:
                        min_date = payment_date
                        first_invoice_age = (date.today() - payment_date).days
            if not no_invoices:
                return self.verify_rules(rules, first_invoice_age)
            return "no record"
        else:
            return "new customer"

    def avg_order_value(self, invoices, rules):
        """
        This method calculates the customer score based on average amount of order per months for past 6 months
        """
        if len(list(invoices)):
            per_invoice_amount = []
            no_invoices = 0
            for invoice in invoices:
                no_invoices = 1
                per_invoice_amount.append(invoice.amount_total)
            average_order_value = sum(per_invoice_amount)/ len(list(invoices))
            if no_invoices:
                return self.verify_rules(rules, average_order_value)
            return "no record"
        else:
            return "new customer"

    def dispute_count(self, invoices, rules):
        if len(list(invoices)):
            pass
        else:
            return "new customer"

    def return_rate(self, invoices, rules):
        if len(list(invoices)):
            pass
        else:
            return "new customer"

    def payment_bounce_count(self, invoices, rules):
        if len(list(invoices)):
            pass
        else:
            return "new customer"

    def invoice_volume_monthly(self, invoices, rules):
        """
        This method calculates the customer score based on the number of invoices for past 6 months
        """
        if len(list(invoices)):
            months = 6
            current_date = date.today()
            monthly_dates = [current_date - relativedelta(months=months)]
            while months:
                monthly_dates.append((monthly_dates[6 - months] + relativedelta(months=1)))
                months -= 1
            monthly_invoices = [0, 0, 0, 0, 0, 0]
            for invoice in invoices:
                if invoice.invoice_date >= monthly_dates[0] and invoice.invoice_date <= monthly_dates[1]:
                    monthly_invoices[0] += 1

                elif invoice.invoice_date > monthly_dates[1] and invoice.invoice_date <= monthly_dates[2]:
                    monthly_invoices[1] += 1

                elif invoice.invoice_date > monthly_dates[2] and invoice.invoice_date <= monthly_dates[3]:
                    monthly_invoices[2] += 1

                elif invoice.invoice_date > monthly_dates[3] and invoice.invoice_date <= monthly_dates[4]:
                    monthly_invoices[3] += 1

                elif invoice.invoice_date > monthly_dates[4] and invoice.invoice_date <= monthly_dates[5]:
                    monthly_invoices[4] += 1

                else:
                    monthly_invoices[5] += 1

            average_monthly_invoices = sum(monthly_invoices) / len(list(monthly_invoices))
            return self.verify_rules(rules, average_monthly_invoices)

        else:
            return "new customer"