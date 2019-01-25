# -*- encoding: utf-8 -*-

from odoo import fields, models


class MRPBoMLine(models.Model):

    _inherit = 'mrp.bom.line'

    reverse_cost_aff_perc = fields.Float(string='Reverse cost affectaction (%)')
