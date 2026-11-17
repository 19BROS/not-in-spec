"""A tiny library documented three ways, for the Sphinx reader golden tests."""


def connect(host: str, timeout: float | None = None, retries: int = 3) -> "Connection":
    """Open a connection (reST fields).

    :param host: Server name.
    :param timeout: Seconds to wait; ``None`` waits forever.
    :type timeout: float or None
    :param retries: How many times to retry. Each retry waits twice as long.

        Set to ``0`` to fail on the first error.
    :returns: An open connection.
    :rtype: Connection
    :raises ValueError: If ``host`` is empty.
    :raises TimeoutError: If the server does not answer within ``timeout`` seconds.
    """
    raise NotImplementedError


def send(data: bytes, *, flush: bool = False) -> int:
    """Send bytes (Google style).

    Args:
        data: The payload.
        flush (bool): Flush after sending.

    Returns:
        int: Number of bytes sent.

    Raises:
        ConnectionError: If the connection is closed.
    """
    raise NotImplementedError


def receive(size: int = 1024) -> bytes:
    """Receive bytes (NumPy style).

    Parameters
    ----------
    size : int, optional
        Maximum number of bytes, default 1024.

        Must be positive.
    strict : bool
        Raise instead of returning fewer bytes.

    Returns
    -------
    bytes
        The received data.

    Raises
    ------
    ConnectionError
        If the connection is closed.

    Examples
    --------
    >>> receive(4)
    b'ping'
    """
    raise NotImplementedError


class Connection:
    """An open connection.

    :param host: Server name.
    """

    #: Seconds to wait when no timeout is given.
    default_timeout: float = 30.0

    def __init__(self, host: str) -> None:
        self.host = host

    def close(self) -> None:
        """Close the connection.

        .. versionadded:: 1.1

        .. warning:: Closing twice raises :exc:`RuntimeError`.
        """

    class Stats:
        """Counters of one connection."""

        def reset(self) -> None:
            """Set all counters to zero."""
