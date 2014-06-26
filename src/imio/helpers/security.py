# -*- coding: utf-8 -*-

from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager

from Products.CMFCore.tests.base.security import OmnipotentUser

from plone import api


def call_as_super_user(callable_obj, *args, **named_args):
    """
    Call a callable object after switching to a security manager with omnipotent user
    then fall back to the original security manager.
    """

    class SuperUser(OmnipotentUser):
        """
        OmnipotentUser does  not implement has_role() so we have to define our own super
        user class implmenting the method.
        """
        def has_role(self, *rags, **kwargs):
            return True

    oldsm = getSecurityManager()
    # login as an super user
    portal = api.portal.getSite()
    newSecurityManager(None, SuperUser().__of__(portal.aq_inner.aq_parent.acl_users))
    try:
        callable_obj(*args, **named_args)
    except Exception, exc:
        # in case something wrong happen, make sure we fall back to original user
        setSecurityManager(oldsm)
        raise exc
    # fall back to original user
    setSecurityManager(oldsm)
