.. _landmask:

==================
Compute land mask
==================

To get a land flag (boolean) the intersection between a third-party land-mask and the tile footprint is computed.
If the intersection is not null then the computation of spectra is not performed.

.. note::
    currently the processor used the 10 m land-mask distributed through cartopy Python package ( see :cite:t:`landmasknatural10m`).