from threading import Timer


class repeated_timer:
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.timer = None
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.timer = Timer(self.interval, self._run)
            self.timer.start()
            self.is_running = True

    def stop(self):
        self.timer.cancel()
        self.is_running = False


class timeout:
    def __init__(self, timeout, function, *args, **kwargs):
        self.timeout = timeout
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.timer = None
        self.is_running = False

    def _run(self):
        self.is_running = False
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.timer = Timer(self.timeout, self._run)
            self.timer.start()
            self.is_running = True

    def stop(self):
        self.timer.cancel()
        self.is_running = False


def set_interval(func, interval: float, *args, **kwargs):
    """
    Setting up periodic execution of a function at the specified interval.

    :param func: The function to be executed periodically.
    :param interval: The time interval between function calls in seconds.
    :param args: Positional arguments to be passed to the function.
    :param kwargs: Named arguments to be passed to the function.
    :return: repeated_timer object for possible stopping of periodic execution.
    """

    return repeated_timer(interval, func, *args, **kwargs)


def clear_interval(timer):
    """
    Stopping the periodic execution of a function.

    :param timer: The repeated_timer object to stop.
    """
    timer.stop()


def set_timeout(func, timeout: float, *args, **kwargs):
    """
    Setting a timeout for the execution of a function.

    :param func: The function to be executed after the timeout.
    :param timeout: The delay time in seconds.
    :param args: Positional arguments to be passed to the function.
    :param kwargs: Named arguments to be passed to the function.
    :return: timeout object for possible cancellation of the timeout.
    """

    t = timeout(timeout, func, *args, **kwargs)

    t.start()

    return t


def clear_timeout(timer):
    """
    Stopping the timeout execution of a function.

    :param timer: The timeout object to stop.
    """
    timer.stop()
