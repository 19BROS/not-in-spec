User Guide
==========

Connections are cheap. Call :func:`fixturelib.connect` with a ``host``; see the
footnote [#f1]_ for limits.

.. note:: Notes are prose.

.. warning::
   Warnings too, even with a list and code:

   - one
   - two

   .. code-block:: python

      conn.close()

Timeouts
--------

.. versionadded:: 1.1
   The ``timeout`` parameter.

A timeout is in *seconds*.

.. rubric:: Example

.. code-block:: python
   :caption: Connecting with a timeout

   conn = connect("example.com", timeout=2.5)

.. literalinclude:: ../fixturelib.py
   :pyobject: Connection.close

.. list-table:: Limits
   :header-rows: 1

   * - Setting
     - Default
   * - ``timeout``
     - ``None`` (wait forever)

Definitions:

term
   A word with its definition.

Low-level API
-------------

.. function:: ping(host, count=1)

   Send pings.

   :param str host: Server name.
   :param int count: How many.
   :returns: Round-trip times in seconds.

Prose after the function stays in the section's own chunk.

.. class:: Pool(size)

   A pool of connections.

   .. method:: acquire()

      Take a connection.

   .. method:: release(conn)

      Give it back.

   .. attribute:: size

      Number of connections.

.. seealso:: The :doc:`api`.

.. rubric:: Footnotes

.. [#f1] At most ``100`` connections.
