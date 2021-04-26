from functools import wraps
import inspect
import datetime


class CodeTrace:
    tracer_mode = {'default': 2}

    def __init__(self, **kwargs):
        dte = self.set_verbose(kwargs)
        self.tracer_mode.update({'default': dte})

    def code_tracer(self, **kwargs):
        dte = self.set_verbose(kwargs)
        def inner(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.tracer_mode.update({func.__name__: dte})
                if dte > 1:
                    print(' --  Calling method:', func.__name__, args[1:])
                res = func(*args, **kwargs)
                if dte > 1:
                    print(' --  Finished:', func.__name__, ':', res if res else '')
                return res

            return wrapper

        return inner

    def log(self, *ob):
        stack = inspect.stack()
        caller_class = stack[1][0].f_locals["self"].__class__.__name__
        caller_method = stack[1][0].f_code.co_name
        if self.tracer_mode.get(caller_method, self.tracer_mode.get('default')) > 0:
            print('[{0}] [{1} # {2}] : {3}'.format(datetime.datetime.now(), caller_class, caller_method, ob))

    def set_verbose(self, kwa):
        return 0 if kwa.get('skip') else (1 if kwa.get('quiet') else 2)

if __name__ == '__main__':
    ct = CodeTrace()


    @ct.code_tracer(quiet=True)
    def test():
        print("I am test")
        ct.log('log test')


    test()
