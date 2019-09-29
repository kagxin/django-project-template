import logging
from django.utils.deprecation import MiddlewareMixin
import uuid
import time

log = logging.getLogger("request_info_logger")


class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            req_id = uuid.uuid1()
            request.req_id = req_id
            log.error("\nRequest[{}]==========>"
                      "\nmethod:{}"
                      "\npath:{}"
                      "\nauth:{}"
                      "\nbody:{}"
                      "\nquery params:{}"
                      "\n".format(request.req_id,
                                  request.method,
                                  request.path,
                                  request.META.get('HTTP_AUTHORIZATION', 'no auth'),
                                  request.body if hasattr(request, 'body') else 'no body',
                                  request.META.get('QUERY_STRING'), ))
        except Exception as e:
            log.error("request info middleware error: %s" % e)

    def process_response(self, request, response):
        try:
            log.info("\nResponse[{}][{}]==========>"
                     "\npath:{}"
                     "\nmethod:{}"
                     "\nstatus:{}"
                     "\ncontent:{}\n".format(request.req_id,
                                             time.time(),
                                             request.path,
                                             request.method,
                                             response.status_code,
                                             response.content, ))
        except Exception as e:
            log.error("response info middleware error: %s" % e)
        return response
