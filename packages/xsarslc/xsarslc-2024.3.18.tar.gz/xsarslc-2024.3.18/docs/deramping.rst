.. _deramping:

============================
Deramping of digital numbers
============================

Lets call :math:`DN(sample, line)` the 2D matrix of RAW digital numbers with dimensions: sample (fast time) and line (slow time) provided in L1 SLC IW,EW or WV products.
Fast time is in the range direction and slow time is the azimuth direction.

Due to the TOPS mode of IWS acquisition, it is mandatory to deramp the complex digital numbers.
  - The deramping procedure has to be applied to compensate for the antenna steering rate during the acquisition.
  - The deramping procedure do not need to be applied for Wave Mode acquisitions because of the absence of steering.
  - The deramping procedure for IW acquisitions follows the steps described in the ESA Technical note :cite:t:`miranda2017definition`.

The deramped digital number writes:

.. math::
   \overline{DN}=DNe^{i\phi}\qquad\text{with}\qquad\phi=-\pi k_t(\tau)(\eta-\eta_{ref})^2

Definition of :math:`\phi` and how to compute it from L1 SLC products is described in `ESA Technical note COPE-GSEG-EOPG-TN-14-0025`_.

.. _ESA Technical note COPE-GSEG-EOPG-TN-14-0025: https://sentinel.esa.int/documents/247904/1653442/sentinel-1-tops-slc_deramping

