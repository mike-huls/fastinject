# import importlib.util
#
# #from injector import Module, provider, Injector, inject
# from injector import provider, inject, Inject
# from injector import singleton as singleton, threadlocal as scope_threadlocal, noscope as scope_none
#
#
#
#
#
# # conditionally load the scope_request so in the future we can make injectr into a separate package if we want to
# try:
#     #if importlib.util.find_spec("fastapi_injector") is None:
#     from injectr import scope_request
#     #from fastapi_injector import request_scope as scope_request
# except ImportError:
#     # provide a fallback so code won't break
#     scope_request = scope_none
