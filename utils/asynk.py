import sqlite3
import threading
import time

from gi.repository import GObject

from models.email import Email


class Asynk:
    @staticmethod
    def load_emails_async(on_done):
        if not on_done:
            on_done = lambda r, e: None

        def do_call():
            conn = sqlite3.connect("/home/danielcorreia/DataGripProjects/Earth/earth.sqlite")
            GObject.threads_init()
            error = None

            try:
                cur = conn.cursor()
                for row in cur.execute("select * from emails"):
                    email = Email(
                        id=row[0],
                        from_name=row[1],
                        email_from=row[2],
                        to=row[3],
                        subject=row[4],
                        file_path=row[5],
                        cc=row[6],
                        date=row[7],
                        account_id=row[8]
                    )
                    GObject.idle_add(lambda: on_done(email, error))
                    time.sleep(0.05)
                conn.close()
                print("DONE")
            except Exception as err:
                error = err
                conn.close()
                print(err)

        thread = threading.Thread(target=do_call)
        thread.daemon = True
        thread.start()

    # calls f on another thread
    @staticmethod
    def async_call(f, on_done):
        """
        Starts a new thread that calls f and schedules on_done to be run (on the main
        thread) when GTK is not busy.
        Args:
          f (function): the function to call asynchronously. No arguments are passed
                        to it. f should not use any resources used by the main thread,
                        at least not without locking.
          on_done (function): the function that is called when f completes. It is
                              passed f's result as the first argument and whatever
                              was thrown (if anything) as the second. on_done is
                              called on the main thread, so it can access resources
                              on the main thread.
        Returns:
          Nothing.
        Raises:
          Nothing.
        """

        if not on_done:
            on_done = lambda r, e: None

        def do_call():
            result = None
            error = None

            try:
                result = f()
            except Exception as err:
                error = err

            GObject.threads_init()
            GObject.idle_add(lambda: on_done(result, error))

        thread = threading.Thread(target=do_call)
        thread.daemon = False
        thread.start()

    # free function decorator
    @staticmethod
    def async_function(on_done=None):
        """
        A decorator that can be used on free functions so they will always be called
        asynchronously. The decorated function should not use any resources shared
        by the main thread.
        Example:
        @async_function(on_done = do_whatever_done)
        def do_whatever(look, at, all, the, pretty, args):
          # ...
        Args:
          on_done (function): the function that is called when the decorated function
                              completes. If omitted or set to None this will default
                              to a no-op. This function will be called on the main
                              thread.
                              on_done is called with the decorated function's result
                              and any raised exception.
        Returns:
          A wrapper function that calls the decorated function on a new thread.
        Raises:
          Nothing.
        """

        def wrapper(f):
            def run(*args, **kwargs):
                Asynk.async_call(lambda: f(*args, **kwargs), on_done)

            return run

        return wrapper

    # method decorator
    @staticmethod
    def async_method(on_done=None):
        """
        A decorator that can be used on class methods so they will always be called
        asynchronously. The decorated function should not use any resources shared
        by the main thread.
        Example:
        @async_method(on_done = lambda self, result, error: self.on_whatever_done(result, error))
        def do_whatever(self, look, at, all, the, pretty, args):
          # ...
        Args:
          on_done (function): the function that is called when the decorated function
                              completes. If omitted or set to None this will default
                              to a no-op. This function will be called on the main
                              thread.
                              on_done is called with the class instance used, the
                              decorated function's result and any raised exception.
        Returns:
          A wrapper function that calls the decorated function on a new thread.
        Raises:
          Nothing.
        """

        if not on_done:
            on_done = lambda s, r, e: None

        def wrapper(f):
            def run(self, *args, **kwargs):
                Asynk.async_call(lambda: f(self, *args, **kwargs), lambda r, e: on_done(self, r, e))

            return run

        return wrapper
