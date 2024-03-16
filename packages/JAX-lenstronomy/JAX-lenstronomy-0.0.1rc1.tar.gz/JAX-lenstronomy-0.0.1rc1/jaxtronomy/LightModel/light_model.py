# High-level interface to a light model
#
# Copyright (c) 2018-2022, lenstronomy developers
# Copyright (c) 2021, herculens developers and contributors


__author__ = 'sibirrer', 'austinpeel', 'aymgal'


from jaxtronomy.LightModel.light_model_base import LightModelBase

__all__ = ['LightModel']


class LightModel(LightModelBase):
    """Model extended surface brightness profiles of sources and lenses.

    Notes
    -----
    All profiles come with a surface_brightness parameterization (in units per
    square angle and independent of the pixel scale.) The parameter `amp` is
    the linear scaling parameter of surface brightness. Some profiles have
    a total_flux() method that gives the integral of the surface brightness
    for a given set of parameters.

    """
    # TODO: inherit from LinearBasis first with additional features
    def __init__(self, light_model_list, deflection_scaling_list=None,
                 source_redshift_list=None, smoothing=0.001,
                 pixel_interpol='bilinear', pixel_allow_extrapolation=False, kwargs_pixelated={}):
        """

        :param light_model_list: list of light models
        :param deflection_scaling_list: list of floats indicating a relative scaling of the deflection angle from the
         reduced angles in the lens model definition (optional, only possible in single lens plane with multiple source
          planes)
        :param source_redshift_list: list of redshifts for the different light models
         (optional and only used in multi-plane lensing in conjunction with a cosmology model)
        :param smoothing: smoothing factor for certain models (deprecated)
        :param sersic_major_axis: boolean or None, if True, uses the semi-major axis as the definition of the Sersic
         half-light radius, if False, uses the product average of semi-major and semi-minor axis. If None, uses the
         convention in the lenstronomy yaml setting (which by default is =False)
        """
        super(LightModel, self).__init__(light_model_list, smoothing, 
                                         pixel_interpol=pixel_interpol, 
                                         pixel_allow_extrapolation=pixel_allow_extrapolation,
                                         kwargs_pixelated=kwargs_pixelated)
        # TODO add self variables as in lenstronomy
