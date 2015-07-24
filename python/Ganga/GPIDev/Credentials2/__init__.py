from __future__ import absolute_import

from .CredentialStore import credential_store

from .VomsProxy import VomsProxy

from .AfsToken import AfsToken

from .exceptions import CredentialsError

from functools import wraps
import threading

import Ganga.Utility.logging
logger = Ganga.Utility.logging.getLogger()


def require_credential(function):
    """
    A decorator for labelling a function as needed a credential.

    If the decorated function is called directly by the user (checked by looking which thread we are on) then if a
    credential is not available, a prompt is given to request one. If the function is being called in another thread
    (monitoring or similar) then a ``CredentialsError`` is raised.
    
    Uses the function's object's ``credential_requirements`` attribute
    """
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        cred_req = args[0].credential_requirements

        try:
            cred = credential_store[cred_req]
            logger.info('got %s', cred)
        except KeyError:
            if isinstance(threading.current_thread(), threading._MainThread):  # threading.main_thread() in Python 3.4
                logger.warning('Required credential not found in store')
                cred = credential_store.create(cred_req, create=True)
                logger.info('created %s', cred)
            else:
                raise CredentialsError('Cannot get proxy which matches requirements')

        if not cred.is_valid():
            raise CredentialsError('Proxy is invalid')
            
        return function(*args, **kwargs)
    return wrapped_function
