# -*- coding: utf-8 -*-
# Copyright (c) 2021 Victor Pham.
"""
Summary:
"""

from datetime import datetime

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class User(models.Model):
    "Basic user information"
    _name = "coflorist.user"
    _description = "User info in Florist Shop"

    id = fields.Integer('Id', required=True)
    user_name = fields.Char('User name', reuquired=True)
    birthday = fields.Date('Birthday')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male', required=True)
    age = fields.Integer('Age', compute='_compute_age')

    # relation
    role_id = fields.Many2one(
        comodel_name="coflorist.user.role",
        string="Role")
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='acitive', required=True)

    addresses = fields.One2many(
        comodel_name="coflorist.user.info",
        string="Addresses",
        # filer by type for addresses
    )
    phone_numbers = fields.One2many(
        comodel_name="coflorist.user.info",
        string="Phone Numbers"
        # filer by type for addresses
    )

    @api.constrains('birthday')
    def _check_birthday(self) -> None:
        for record in self:
            if record.birthday and record.birthday.year < 1900:
                raise ValidationError(_('Invalid Birthday!'))

    @api.depends('birthday')
    def _compute_age(self) -> None:
        "Compute the age of user"
        now = datetime.now()
        current_year = now.year
        for record in self:
            birthday = self.birthday
            birth_year = birthday.year

            if birthday:
                delta_year = current_year - birth_year
                if delta_year < 0:
                    raise ValidationError(
                        _(f"Nagative age: birthday > {current_year}"))
                else:
                    record.age = delta_year
            else:
                record.age = None


class UserRole(models.Model):
    "Use roles"
    _name = "coflorist.user.role"
    _description = "Role of user"
    id = fields.Integer('Id', required=True)
    role_name = fields.Selection([
        ("sale", "Sale"),
        ("admin", "Admin")
    ], string='Role Name', required=True)


class UserInfo(models.Model):
    """Extract information of user, seperate into rows.
    For example: addresses, phone numbders, companies...
    """
    _name = "coflorist.user.info"
    _description = "Store addresses, phone number, ..."
    id = fields.Integer("Id", required=True)
    user_id = fields.Many2one(
        comodel_name="coflorist.user",
        string="User Id"
    )

    info_type = fields.Selection([
        ("address", "Address"),
        ("phone_number", "Phone Number")
    ], string="Info Type")
    info_value = fields.Char('Info Value')
