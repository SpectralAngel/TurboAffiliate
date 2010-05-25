#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# controllers.py
# This file is part of TurboAffiliate
#
# Copyright © 2007 - 2010 Carlos Flores <cafg10@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from turbogears import controllers, expose
from turbogears import identity, redirect
from turbogears.toolbox.catwalk import CatWalk
from cherrypy import request, response
from turboaffiliate import model
from turboaffiliate.controllers import (affiliate, loan, company, obligation,
                                        flyer, account, payed, logger,
                                        elecciones, solicitud, reintegro)

# import logging
# log = logging.getLogger("turboaffiliate.controllers")

class Root(controllers.RootController):
    
    affiliate = affiliate.Affiliate()
    loan = loan.Loan()
    escalafon = flyer.Flyer()
    company = company.Company()
    obligation = obligation.Obligation()
    account = account.Account()
    catwalk = CatWalk(model)
    payed = payed.PayedLoan()
    logger = logger.Logger()
    elecciones = elecciones.Elecciones()
    solicitud = solicitud.Solicitud()
    reintegro = reintegro.Reintegro()
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.welcome")
    # @identity.require(identity.in_group("admin"))
    def index(self):
        import time
        # log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(now=time.ctime())
    
    @expose(template="turboaffiliate.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):
        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            raise redirect(forward_url)
        
        forward_url=None
        previous_url= request.path
        
        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                  "this resource.")
        else:
            msg=_("Please log in.")
            forward_url= request.headers.get("Referer", "/")
        
        response.status=403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)
    
    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")
