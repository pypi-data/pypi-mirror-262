uniform ground tiling for Sentinel-1 SLC burst
##############################################

Burst division into constant ground segment (``tiles``)
-------------------------------------------------------


SAR SLC product are defined in the radar geometry on a uniform (slant range distance x azimuth distance) grid.
In order to define ground segment (``tiles``) with a constant size in range direction, it is mandatory to define and adaptative variable number of slant range points per segment.

Denoting :math:`theta_i` the incidence angle on the ground at pixel location :math:`i`, we define the cumulative length as

.. math::
    C_0[n] = \Delta s\sum_{i=i_0}^{i_0+n}\dfrac{1}{\sin(\theta_i)}


where :math:`\Delta s` is the slant range spacing.

The total length of a ground segment defined between pixel :math:`i_0` and :math:`i_N=i_0+N` writes:

.. math::
    :label: lb

      l_b = C_0[N] = \Delta s\sum_{i=i_0}^{i_N}\dfrac{1}{\sin(\theta_i)}



In order to divide :math:`l_b` into equidistant segments of constant ground length :math:`l_t` with possible overlaping length :math:`l_o` (:math:`l_o<l_t`) we define
the ground limits :math:`(s_n, e_n)` of segment :math:`n` as:

.. math::
    :label: Startend

      s_n &=& n(l_t-l_o), n \in [0,1,2,...,N]\\
      e_n &=& s_n+l_t


where :math:`N` is the larger possible integer such as :math:`e_N\le l_b`.



Centering tiles
---------------

Defined as in equation :eq:`Startend`, the :math:`N` segments are not centered over the total length :math:`l_b`.
To center the N segments it is enough to add :math:`\frac{l_b-e_N}{2}` to the segment location, i.e.

.. math::
    s_c^n &=& n(l_t-l_o)+\frac{l_b-e_N}{2}, n \in [0,1,2,...,N]\\
    e_c^n &=& s_c^n+l_t+\frac{l_b-e_N}{2}


Pixel indexes pertaining to segment :math:`n` are thus in :math:`[i^n_{min}, i^n_{max}]` defined such as:

.. math::
    i^n_{min} = \text{larger $i$ such as}\ s_c^n&>&C_0[i]\\
    i^n_{max} = \text{smaller $i$ such as}\ e_c^n&<&C_0[i]




In practice, :math:`l_b` is the ground length of a burst (:math:`l_b\approx` 80 km), the slant spacing is :math:`\Delta s\approx` 2.5 m