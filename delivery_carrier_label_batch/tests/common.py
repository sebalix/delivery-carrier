
# -*- coding: utf-8 -*-
# Copyright 2013-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import openerp.tests.common as common


class CommonGenerateLabels(common.SavepointCase):

    """ Test the wizard for delivery carrier label generation """

    @classmethod
    def setUpClass(cls):
        super(CommonGenerateLabels, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        Move = cls.env['stock.move']
        Picking = cls.env['stock.picking']
        BatchPicking = cls.env['stock.batch.picking']

        cls.batch = BatchPicking.create(
            {
                'name': 'demo_prep001',
                'picker_id': cls.env.ref('base.user_demo').id,
            }
        )

        cls.picking_out_1 = Picking.create(
            {
                'partner_id': cls.env.ref('base.res_partner_12').id,
                'batch_picking_id': cls.batch.id,
                'location_id': cls.env.ref('stock.stock_location_14').id,
                'location_dest_id': cls.env.ref('stock.stock_location_7').id,
                'picking_type_id': cls.env.ref('stock.picking_type_out').id
            }
        )

        cls.picking_out_2 = Picking.create(
            {
                'partner_id': cls.env.ref('base.res_partner_12').id,
                'batch_picking_id': cls.batch.id,
                'location_id': cls.env.ref('stock.stock_location_14').id,
                'location_dest_id': cls.env.ref('stock.stock_location_7').id,
                'picking_type_id': cls.env.ref('stock.picking_type_out').id,
            }
        )

        Move.create(
            {
                'name': '/',
                'picking_id': cls.picking_out_1.id,
                'product_id': cls.env.ref('product.product_product_33').id,
                'product_uom': cls.env.ref('product.product_uom_unit').id,
                'product_uom_qty': 2,
                'location_id': cls.env.ref('stock.stock_location_14').id,
                'location_dest_id': cls.env.ref('stock.stock_location_7').id,
            }
        )

        Move.create(
            {
                'name': '/',
                'picking_id': cls.picking_out_2.id,
                'product_id': cls.env.ref('product.product_product_33').id,
                'product_uom': cls.env.ref('product.product_uom_unit').id,
                'product_uom_qty': 1,
                'location_id': cls.env.ref('stock.stock_location_14').id,
                'location_dest_id': cls.env.ref('stock.stock_location_7').id,
            }
        )
