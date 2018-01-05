import glob
import logging
import re
import commands
import ldap

from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import commit_on_success
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from networkapi.api_rest.exceptions import NetworkAPIException,VariableDoesNotExistException
from networkapi.util import convert_string_or_int_to_boolean

from networkapi.distributedlock import distributedlock
from networkapi.distributedlock import LOCK_TESTS_AVAILABLE

from networkapi.system.facade import get_value


log = logging.getLogger(__name__)

class CacheTestView(APIView):

    def get(self, user, *args, **kwargs):
        """Handles GET requests to check memcache connectivity"""

        try:
            log.info('Testing Memcache connectivity')

            locked = False
            with distributedlock(LOCK_TESTS_AVAILABLE % 'lock_test', None, False):
                locked = True
                data = 'WORKING'
        except Exception, e:
            log.exception(e)
            raise api_exceptions.NetworkAPIException(e)

        return Response(data, status=status.HTTP_200_OK)

class AuthenticationTestView(APIView):

    log = logging.getLogger(__name__)

    def get(self, user, *args, **kwargs):
        """Handles GET requests to check connectivity to LDAP server"""

        bypass = 0
        try:
            try:
                use_ldap = convert_string_or_int_to_boolean(
                    get_value('use_ldap'))
                if use_ldap:
                    ldap_param = get_value('ldap_config')
                    ldap_server = get_value('ldap_server')
                else:
                    bypass = 1
            except Exception, e:
                error_msg = 'Error getting LDAP config variables (use_ldap, ldap_config, ldap_server).'
                raise NetworkAPIException(error_msg)

            if not bypass:
                try:
                    username = 'void'
                    password = 'void'
                    connect = ldap.open(ldap_server)
                    user_dn = 'cn=' + username + ',' + c
                    connect.simple_bind_s(user_dn, password)
                except ldap.INVALID_CREDENTIALS, e:
                    #LDAP is fine
                    debug_msg = 'LDAP authentication error %s - Should be fine, this is only a test with invalid user' % e
                    self.log.debug(debug_msg)

            data = 'WORKING'
            return Response(data, status=status.HTTP_200_OK)

        except Exception, e:
            self.log.exception(e)
            raise NetworkAPIException(e)


class ForemanTestView(APIView):

    log = logging.getLogger(__name__)

    def get(self, user, *args, **kwargs):
        try:
            """Handles GET requests to check connectivity to Foreman server"""

            use_foreman = 0
            try:
                use_foreman = int(get_variable('use_foreman'))
            except Exception, e:
                error_msg = 'Error getting use_foreman config variable.'
                raise NetworkAPIException(error_msg)

            try:
                NETWORKAPI_FOREMAN_URL = get_variable("foreman_url")
                NETWORKAPI_FOREMAN_USERNAME = get_variable("foreman_username")
                NETWORKAPI_FOREMAN_PASSWORD = get_variable("foreman_password")
                FOREMAN_HOSTS_ENVIRONMENT_ID = get_variable("foreman_hosts_environment_id")
            except Exception, e:
                error_msg = 'Error getting foreman config variables.'
                raise NetworkAPIException(error_msg)

            if use_foreman:
                from foreman.client import Foreman, ForemanException
                foreman = Foreman(NETWORKAPI_FOREMAN_URL, (NETWORKAPI_FOREMAN_USERNAME, NETWORKAPI_FOREMAN_PASSWORD), api_version=2)

            data = 'WORKING'
            return Response(data, status=status.HTTP_200_OK)

        except Exception, e:
            self.log.exception(e)
            raise NetworkAPIException(e)
