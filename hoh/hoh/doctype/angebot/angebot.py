# -*- coding: utf-8 -*-
# Copyright (c) 2020, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _

class Angebot(WebsiteGenerator):
    website = frappe._dict(
        condition_field = "show_in_website",
        template = "templates/generators/angebot.html",
        no_cache = 1,
        show_sidebar = 1
    )
    
    # THIS CODE IS NOT EXECUTED, CONSIDER OPTION IN get_list_context
    #def get_context(self, context):
    #    context.update({
    #        "items": frappe.get_list("Angebot", filters={'docstatus': 1}, fields=['name']),
    #        "title": _("Quotations")
    #    })
    #    
    #    return context
        
# enable list view sidebar
def get_list_context(context=None):
    context.update({
        'no_breadcrumbs': True,
        'show_sidebar': True,
        'row_template': 'templates/includes/angebot_row.html'
    })
    return context

# this function will render an html string will all care symbols
@frappe.whitelist()
def get_care_symbol_html(bemusterung):
    # prepare query
    sql_query = """SELECT `tabPflegesymbol`.`titel` AS `title`, 
          `tabPflegesymbol`.`image` AS `url`
        FROM `tabItem Pflegesymbol` 
        LEFT JOIN `tabPflegesymbol` ON `tabItem Pflegesymbol`.`pflegesymbol` = `tabPflegesymbol`.`name`
        WHERE `tabItem Pflegesymbol`.`parenttype` = "Bemusterung"
          AND `tabItem Pflegesymbol`.`parent` = "{bemusterung}";""".format(bemusterung=bemusterung)
    # collect data
    data = {
        'symbols': frappe.db.sql(sql_query, as_dict=True)
    }
    # render data
    html = frappe.render_template('hoh/hoh/doctype/angebot/care_symbols.html', data)
    return html
