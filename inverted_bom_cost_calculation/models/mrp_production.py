# -*- encoding: utf-8 -*-

from odoo import api, models


class MRPProduction(models.Model):

    _inherit = 'mrp.production'

    @api.multi
    def button_mark_done(self):

        total_cost = 0.0
        for finished_move in self.move_finished_ids:
            total_cost += finished_move.product_id.standard_price * finished_move.quantity_done

        for raw_move in self.move_raw_ids:
            raw_move.write({
                'price_unit': (total_cost * raw_move.bom_line_id.reverse_cost_aff_perc/100) / raw_move.quantity_done
            })

        return super(MRPProduction, self).button_mark_done()
