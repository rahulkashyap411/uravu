"""
Tests for relationship module
"""

# Copyright (c) Andrew R. McCluskey
# Distributed under the terms of the MIT License
# author: Andrew R. McCluskey

import unittest
import numpy as np
import uncertainties
from uncertainties import unumpy as unp
from numpy.testing import assert_almost_equal, assert_equal
from uravu import UREG, utils
from uravu.relationship import Relationship
from uravu.distribution import Distribution


STRING_A = (
    "Function Name: straight_line \n"
    "Abscissa: [ 1.00e+00 2.00e+00 ... 9.00e+00 1.00e+01 ] \n"
    "Ordinate: [ 1.62e+00 -6.12e-01 ... 3.19e-01 -2.49e-01 ] \n"
    "Ordinate uncertainty: [ 1.00e-01 1.00e-01 ... 1.00e-01 1.00e-01 ]\n"
    "Abscissa Name: x \nOrdinate Name: y \nAbscissa Unit: dimensionless \n"
    "Ordinate Unit: dimensionless \nVariables: [ 1.00e+00 1.00e+00 ] \n"
    "Unaccounted uncertainty: False \nMCMC performed: False \n"
    "Nested sampling performed: False \n"
)

STRING_B = (
    "Function Name: straight_line \n"
    "Abscissa: [ 1.00e+00 5.50e+00 1.00e+01 ] \n"
    "Ordinate: [ 1.62e+00 -6.12e-01 -5.28e-01 ] \n"
    "Ordinate uncertainty: [ 1.00e-01 1.00e-01 1.00e-01 ] \n"
    "Abscissa Name: x \nOrdinate Name: y \nAbscissa Unit: dimensionless \n"
    "Ordinate Unit: dimensionless \nVariables: [ 1.00e+00 1.00e+00 ] \n"
    "Unaccounted uncertainty: False \nMCMC performed: False \n"
    "Nested sampling performed: False \n"
)

STRING_C = (
    "Function Name: straight_line \n"
    "Abscissa: [ 1.00e+00 2.00e+00 ... 9.00e+00 1.00e+01 ] \n"
    "Ordinate: [ 1.62e+00 -6.12e-01 ... 3.19e-01 -2.49e-01 ] \n"
    "Ordinate uncertainty: [ 1.00e-01 1.00e-01 ... 1.00e-01 1.00e-01 ]\n"
    "Abscissa Name: x \nOrdinate Name: y \nAbscissa Unit: dimensionless \n"
    "Ordinate Unit: dimensionless \nVariables: [ 1.00e+00 1.00e+00 ] \n"
    "ln(evidence): (-7.89+/-nan)e+02 \nUnaccounted uncertainty: False \n"
    "MCMC performed: False \nNested sampling performed: True \n"
)

STRING_D = (
    "Function Name: straight_line \n"
    "Abscissa: [ 1.00e+00 5.50e+00 1.00e+01 ] \n"
    "Abscissa uncertainty: [ 1.00e-01 1.00e-01 1.00e-01 ] \n"
    "Ordinate: [ 1.62e+00 -6.12e-01 -5.28e-01 ] \n"
    "Ordinate uncertainty: [ 1.00e-01 1.00e-01 1.00e-01 ] \n"
    "Abscissa Name: x \nOrdinate Name: y \nAbscissa Unit: dimensionless \n"
    "Ordinate Unit: dimensionless \nVariables: [ 1.00e+00 1.00e+00 ] \n"
    "Unaccounted uncertainty: False \nMCMC performed: False \n"
    "Nested sampling performed: False \n"
)

STRING_E = (
    "Function Name: straight_line \n"
    "Abscissa: [ 1.00e+00 3.25e+00 ... 7.75e+00 1.00e+01 ] \n"
    "Abscissa uncertainty: [ 1.00e-01 1.00e-01 ... 1.00e-01 1.00e-01 ] \n"
    "Ordinate: [ 1.62e+00 -6.12e-01 ... -1.07e+00 8.65e-01 ] \n"
    "Ordinate uncertainty: [ 1.00e-01 1.00e-01 ... 1.00e-01 1.00e-01 ]\n"
    "Abscissa Name: x \nOrdinate Name: y \nAbscissa Unit: dimensionless \n"
    "Ordinate Unit: dimensionless \nVariables: [ 1.00e+00 1.00e+00 ] \n"
    "Unaccounted uncertainty: False \nMCMC performed: False \n"
    "Nested sampling performed: False \n"
)

STRING_F = (
    "Function Name: straight_line \n"
    "Abscissa: [ 1.00e+00 2.00e+00 ... 9.00e+00 1.00e+01 ] \n"
    "Ordinate: [ 1.62e+00 -6.12e-01 ... 3.19e-01 -2.49e-01 ] \n"
    "Ordinate uncertainty: [ 1.00e-01 1.00e-01 ... 1.00e-01 1.00e-01 ]\n"
    "Abscissa Name: x \nOrdinate Name: y \nAbscissa Unit: dimensionless \n"
    "Ordinate Unit: dimensionless \n"
    "Variables: [ 1.13e-02+3.17e+00-9.35e-01 3.41e-01+4.90e+00-3.18e+00 ] \n"
    "Unaccounted uncertainty: False \nMCMC performed: True \n"
    "Nested sampling performed: False \n"
)

STRING_G = (
    "Function Name: straight_line \n"
    "Abscissa: [ 1.00e+00 2.00e+00 ... 9.00e+00 1.00e+01 ] \n"
    "Ordinate: [ 1.62e+00 -6.12e-01 ... 3.19e-01 -2.49e-01 ] \n"
    "Ordinate uncertainty: [ 1.00e-01 1.00e-01 ... 1.00e-01 1.00e-01 ]\n"
    "Abscissa Name: x \nOrdinate Name: y \nAbscissa Unit: dimensionless \n"
    "Ordinate Unit: dimensionless \n"
    "Variables: [ 1.13e-02+/-9.35e-01 3.41e-01+/-3.18e+00 ] \n"
    "Unaccounted uncertainty: False \nMCMC performed: True \n"
    "Nested sampling performed: False \n"
)

CITATION_A = "Please consider citing the following:\n - Publication of uravu (to come).\n - Zenodo DOI for uravu version: 0.0.1\n"
CITATION_B = "Please consider citing the following:\n - Publication of uravu (to come).\n - Zenodo DOI for uravu version: 0.0.1\nThe scipy.optimize.minimize function was used to maximise the ln likelihood. Please consider citing:\n - P. Virtanen, r. Gommers, T. E. Oliphant, M. Haberland, T. Reddy, D. Cournapeau, E. Burovski, P. Peterson, W. Weckesser, J. Bright, S. J. van der Walt, M. Brett, J./ Wilson, K. J. Millman, N. Mayorov, A. R. J. Nelson, E. Jones, R. Kern, E. Larson, C. Carey, I. Polat, Y. Feng, E. W. Moore, J. VanderPlas, D. Laxalde, J. Perktold, R. Cimrman, I. Henriksen, E. A. Quintero, C. R Harris, A. M. Archibald, A. H. Ribeiro, F. Pedregosa, P. van Mulbregt, & SciPy 1.0 Contributors, (2020). Nature Methods, in press. DOI: 10.1038/s41592-019-0686-2\n"
CITATION_C = "Please consider citing the following:\n - Publication of uravu (to come).\n - Zenodo DOI for uravu version: 0.0.1\nThe scipy.optimize.minimize function was used to maximise the ln likelihood. Please consider citing:\n - P. Virtanen, r. Gommers, T. E. Oliphant, M. Haberland, T. Reddy, D. Cournapeau, E. Burovski, P. Peterson, W. Weckesser, J. Bright, S. J. van der Walt, M. Brett, J./ Wilson, K. J. Millman, N. Mayorov, A. R. J. Nelson, E. Jones, R. Kern, E. Larson, C. Carey, I. Polat, Y. Feng, E. W. Moore, J. VanderPlas, D. Laxalde, J. Perktold, R. Cimrman, I. Henriksen, E. A. Quintero, C. R Harris, A. M. Archibald, A. H. Ribeiro, F. Pedregosa, P. van Mulbregt, & SciPy 1.0 Contributors, (2020). Nature Methods, in press. DOI: 10.1038/s41592-019-0686-2\nThe emcee package was used to perform the MCMC analysis. Please consider citing:\n - D. Foreman-Mackey, W. Farr, M. Sinha, A. Archibald, D. Hogg, J. Sanders, J. Zuntz, P. Williams, A. Nelson, M. de Val-Borro, T. Erhardt, I. Pashchenko, & O. Pla, (2019). Journal of Open Source Software, 4(43), 1864. DOI: 10.21105/joss.01864\n - J. Goodman & J. Weare, (2010). Communications in applied mathematics and computational science, 5(1), 65. DOI: 10.2140/camcos.2010.5.65\n"
CITATION_D = "Please consider citing the following:\n - Publication of uravu (to come).\n - Zenodo DOI for uravu version: 0.0.1\nThe scipy.optimize.minimize function was used to maximise the ln likelihood. Please consider citing:\n - P. Virtanen, r. Gommers, T. E. Oliphant, M. Haberland, T. Reddy, D. Cournapeau, E. Burovski, P. Peterson, W. Weckesser, J. Bright, S. J. van der Walt, M. Brett, J./ Wilson, K. J. Millman, N. Mayorov, A. R. J. Nelson, E. Jones, R. Kern, E. Larson, C. Carey, I. Polat, Y. Feng, E. W. Moore, J. VanderPlas, D. Laxalde, J. Perktold, R. Cimrman, I. Henriksen, E. A. Quintero, C. R Harris, A. M. Archibald, A. H. Ribeiro, F. Pedregosa, P. van Mulbregt, & SciPy 1.0 Contributors, (2020). Nature Methods, in press. DOI: 10.1038/s41592-019-0686-2\nThe dynesty package was used to carry out the nested sampling. Please consider citing:\n - J. S. Speagle, (2019), Monthly Notices of the Royal Astronomical Society, staa278. DOI: 10.1093/mnras/staa278.\n - J. Skilling (2004), AIP Conference Proceedings, 735(1), 395. DOI: 10.1063/1.1835238.\n - J. Skilling (2006), Bayesian Analysis, 1(4), 833. DOI: 10.1214/06-BA127.\n"


class TestRelationship(unittest.TestCase):
    """
    Tests for the relationship module and class.
    """

    def test_init_all_default_one_dimensional(self):
        """
        Test the initialisation of the relationship class with one
        dimensional data and all defaults.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_equal(test_rel.function, utils.straight_line)
        assert_almost_equal(test_rel.abscissa.m, test_x)
        assert_almost_equal(unp.nominal_values(test_rel.ordinate.m), test_y)
        assert_almost_equal(unp.std_devs(test_rel.ordinate.m), test_y_e)
        assert_almost_equal(test_rel.variables, np.ones((2)))

    def test_init_all_default_two_dimensional(self):
        """
        Test the initialisation of the relationship class with two
        dimensional data and all defaults.
        """
        test_x = np.array([np.linspace(0, 99, 100), np.linspace(0, 99, 100)]).T
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_equal(test_rel.function, utils.straight_line)
        assert_almost_equal(test_rel.abscissa.m, test_x)
        assert_almost_equal(unp.nominal_values(test_rel.ordinate.m), test_y)
        assert_almost_equal(unp.std_devs(test_rel.ordinate.m), test_y_e)
        assert_almost_equal(test_rel.variables, np.ones((2)))

    def test_init_additional_uncertainty_one_dimensional(self):
        """
        Test the initialisation of the relationship class with one
        dimensional data and an additional uncertainty.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            unaccounted_uncertainty=True,
        )
        assert_equal(test_rel.function, utils.straight_line)
        assert_almost_equal(test_rel.abscissa.m, test_x)
        assert_almost_equal(unp.nominal_values(test_rel.ordinate.m), test_y)
        assert_almost_equal(unp.std_devs(test_rel.ordinate.m), test_y_e)
        assert_almost_equal(test_rel.variables, np.ones((3)))

    def test_init_additional_uncertainty_two_dimensional(self):
        """
        Test the initialisation of the relationship class with two
        dimensional data and an additional uncertainty.
        """
        test_x = np.array([np.linspace(0, 99, 100), np.linspace(0, 99, 100)]).T
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            unaccounted_uncertainty=True,
        )
        assert_equal(test_rel.function, utils.straight_line)
        assert_almost_equal(test_rel.abscissa.m, test_x)
        assert_almost_equal(unp.nominal_values(test_rel.ordinate.m), test_y)
        assert_almost_equal(unp.std_devs(test_rel.ordinate.m), test_y_e)
        assert_almost_equal(test_rel.variables, np.ones((3)))

    def test_init_different_length_x_and_y_one_dimension(self):
        """
        Test initialisation with different array lengths and one dimensional
        data.
        """
        with self.assertRaises(ValueError):
            test_x = np.linspace(0, 99, 100)
            test_y = np.linspace(0, 199, 99)
            test_y_e = test_y * 0.1
            Relationship(utils.straight_line, test_x, test_y, test_y_e)

    def test_init_different_length_x_and_y_two_dimension(self):
        """
        Test initialisation with different array lengths and two dimensional
        data.
        """
        with self.assertRaises(ValueError):
            test_x = np.array(
                [np.linspace(0, 99, 100), np.linspace(0, 99, 100)]
            ).T
            test_y = np.linspace(0, 199, 99)
            test_y_e = test_y * 0.1
            Relationship(utils.straight_line, test_x, test_y, test_y_e)

    def test_init_different_length_y_and_y_err_one_dimension(self):
        """
        Test initialisation with different array lengths and one dimensional
        data.
        """
        with self.assertRaises(ValueError):
            test_x = np.linspace(0, 99, 100)
            test_y = np.linspace(0, 199, 100)
            test_y_e = np.linspace(0, 199, 99)
            Relationship(utils.straight_line, test_x, test_y, test_y_e)

    def test_init_different_length_y_and_y_err_two_dimension(self):
        """
        Test initialisation with different array lengths and one dimensional
        data.
        """
        with self.assertRaises(ValueError):
            test_x = np.array(
                [np.linspace(0, 99, 100), np.linspace(0, 99, 100)]
            ).T
            test_y = np.linspace(0, 199, 100)
            test_y_e = np.linspace(0, 199, 99)
            Relationship(utils.straight_line, test_x, test_y, test_y_e)

    def test_init_x_u_one_dimensional(self):
        """
        Test the initialisation of the relationship class with one
        dimensional data and an uncertainty in the abscissa.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_x_e = test_x * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            abscissa_uncertainty=test_x_e,
        )
        assert_equal(test_rel.function, utils.straight_line)
        assert_almost_equal(unp.nominal_values(test_rel.abscissa.m), test_x)
        assert_almost_equal(unp.std_devs(test_rel.abscissa.m), test_x_e)
        assert_almost_equal(unp.nominal_values(test_rel.ordinate.m), test_y)
        assert_almost_equal(unp.std_devs(test_rel.ordinate.m), test_y_e)
        assert_almost_equal(test_rel.variables, np.ones((2)))

    def test_init_x_unit_one_dimensional(self):
        """
        Test the initialisation of the relationship class with one
        dimensional data and an unit in abscissa.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            abscissa_unit=UREG.meter,
        )
        assert_equal(test_rel.function, utils.straight_line)
        assert_almost_equal(test_rel.abscissa.m, test_x)
        assert_equal(test_rel.abscissa.u, UREG.meter)
        assert_almost_equal(unp.nominal_values(test_rel.ordinate.m), test_y)
        assert_almost_equal(unp.std_devs(test_rel.ordinate.m), test_y_e)
        assert_almost_equal(test_rel.variables, np.ones((2)))

    def test_init_y_unit_one_dimensional(self):
        """
        Test the initialisation of the relationship class with one
        dimensional data and an unit in ordinate.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            ordinate_unit=UREG.meter,
        )
        assert_equal(test_rel.function, utils.straight_line)
        assert_almost_equal(test_rel.abscissa.m, test_x)
        assert_equal(test_rel.ordinate.u, UREG.meter)
        assert_almost_equal(unp.nominal_values(test_rel.ordinate.m), test_y)
        assert_almost_equal(unp.std_devs(test_rel.ordinate.m), test_y_e)
        assert_almost_equal(test_rel.variables, np.ones((2)))

    def test_x_a(self):
        """
        Test the x property with no uncertainty.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_almost_equal(test_rel.x.m, test_x)
        assert_equal(test_rel.x.u, UREG.dimensionless)

    def test_x_b(self):
        """
        Test the x property with uncertainty.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_x_e = test_x * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            abscissa_uncertainty=test_x_e,
        )
        assert_almost_equal(unp.nominal_values(test_rel.x.m), test_x)
        assert_almost_equal(unp.std_devs(test_rel.x.m), test_x_e)
        assert_equal(test_rel.x.u, UREG.dimensionless)

    def test_y(self):
        """
        Test the y property.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_almost_equal(unp.nominal_values(test_rel.y.m), test_y)
        assert_almost_equal(unp.std_devs(test_rel.y.m), test_y_e)
        assert_equal(test_rel.y.u, UREG.dimensionless)

    def test_x_m_a(self):
        """
        Test the x_m property with no uncertainty.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_almost_equal(test_rel.x_m, test_x)

    def test_x_m_b(self):
        """
        Test the x_m property with uncertainty.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_x_e = test_x * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            abscissa_uncertainty=test_x_e,
        )
        assert_almost_equal(unp.nominal_values(test_rel.x_m), test_x)
        assert_almost_equal(unp.std_devs(test_rel.x_m), test_x_e)

    def test_y_m(self):
        """
        Test the y_m property.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_almost_equal(unp.nominal_values(test_rel.y_m), test_y)
        assert_almost_equal(unp.std_devs(test_rel.y_m), test_y_e)

    def test_x_u(self):
        """
        Test the x_u property.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            abscissa_unit=UREG.meter,
        )
        assert_equal(test_rel.x_u, UREG.meter)

    def test_y_u(self):
        """
        Test the y_u property.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            ordinate_unit=UREG.meter,
        )
        assert_equal(test_rel.y_u, UREG.meter)

    def test_x_n_a(self):
        """
        Test the x_n property with no uncertainty.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_almost_equal(test_rel.x_n, test_x)

    def test_x_n_b(self):
        """
        Test the x_n property with uncertainty.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_x_e = test_x * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            abscissa_uncertainty=test_x_e,
        )
        assert_almost_equal(test_rel.x_n, test_x)

    def test_x_s_a(self):
        """
        Test the x_n property with no uncertainty.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_equal(test_rel.x_s, None)

    def test_x_s_b(self):
        """
        Test the x_n property with uncertainty.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_x_e = test_x * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            abscissa_uncertainty=test_x_e,
        )
        assert_almost_equal(test_rel.x_s, test_x_e)

    def test_y_n(self):
        """
        Test the y_n property.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_almost_equal(test_rel.y_n, test_y)

    def test_y_s(self):
        """
        Test the y_s property.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_almost_equal(test_rel.y_s, test_y_e)

    def test_variable_medians_b(self):
        """
        Test variable_medians property when the variables are Distributions.
        """
        test_x = np.linspace(0, 99, 10)
        test_y = (
            np.linspace(1, 199, 10)
            + np.linspace(1, 199, 10) * np.random.randn(10) * 0.05
        )
        test_y_e = test_y * 0.2
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e,)
        test_rel.max_likelihood()
        test_rel.mcmc(n_burn=10, n_samples=10)
        medians = test_rel.variable_medians
        assert_equal(medians.shape, (2,))

    def test_variable_medians_a(self):
        """
        Test variable_medians property when the variables are floats.
        """
        test_x = np.linspace(0, 99, 10)
        test_y = (
            np.linspace(1, 199, 10)
            + np.linspace(1, 199, 10) * np.random.randn(10) * 0.05
        )
        test_y_e = test_y * 0.2
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e,)
        test_rel.max_likelihood()
        medians = test_rel.variable_medians
        assert_equal(medians.shape, (2,))

    def test_len_parameters(self):
        """
        test the len_parameters function.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(0, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_equal(test_rel.len_parameters(), 2)

    def test_max_likelihood(self):
        """
        Test max_likelihood function.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(1, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        test_rel.max_likelihood()
        assert_almost_equal(test_rel.variables, np.array([2, 1]))

    def test_prior(self):
        """
        Test prior function.
        """
        test_x = np.linspace(0, 99, 100)
        test_y = np.linspace(1, 199, 100)
        test_y_e = test_y * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        test_rel.max_likelihood()
        result_priors = test_rel.prior(np.random.random((2, 100)))
        assert_equal(result_priors.shape, (2, 100))
        assert_equal(result_priors[0].min() > -18, True)
        assert_equal(result_priors[0].max() < 22, True)
        assert_equal(result_priors[1].min() > -9, True)
        assert_equal(result_priors[1].max() < 11, True)

    def test_mcmc(self):
        """
        Test mcmc function.
        """
        test_x = np.linspace(0, 99, 10)
        test_y = (
            np.linspace(1, 199, 10)
            + np.linspace(1, 199, 10) * np.random.randn(10) * 0.05
        )
        test_y_e = test_y * 0.2
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e,)
        test_rel.max_likelihood()
        test_rel.mcmc(n_burn=10, n_samples=10)
        assert_equal(isinstance(test_rel.variables[0], Distribution), True)
        assert_equal(isinstance(test_rel.variables[1], Distribution), True)
        assert_equal(test_rel.variables[0].size, 1000)
        assert_equal(test_rel.variables[1].size, 1000)
        assert_equal(test_rel.mcmc_done, True)
        assert_equal(test_rel.nested_sampling_done, False)

    def test_nested_sampling(self):
        """
        Test nested sampling.
        """
        test_y = np.ones(10) * np.random.randn(10)
        test_y_e = np.ones(10) * 0.1
        test_x = np.linspace(1, 10, 10)
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        test_rel.nested_sampling(maxiter=10)
        assert_equal(
            isinstance(test_rel.ln_evidence, uncertainties.core.Variable), True
        )
        assert_equal(test_rel.nested_sampling_done, True)
        assert_equal(test_rel.mcmc_done, False)

    def test_str_a(self):
        """
        Test __str__ function A.
        """
        np.random.seed(1)
        test_y = np.ones(10) * np.random.randn(10)
        test_y_e = np.ones(10) * 0.1
        test_x = np.linspace(1, 10, 10)
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_equal(test_rel.__str__(), STRING_A)

    def test_str_b(self):
        """
        Test __str__ function B.
        """
        np.random.seed(1)
        test_y = np.ones(3) * np.random.randn(3)
        test_y_e = np.ones(3) * 0.1
        test_x = np.linspace(1, 10, 3)
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_equal(test_rel.__str__(), STRING_B)

    def test_str_c(self):
        """
        Test __str__ function C.
        """
        np.random.seed(1)
        test_y = np.ones(10) * np.random.randn(10)
        test_y_e = np.ones(10) * 0.1
        test_x = np.linspace(1, 10, 10)
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        test_rel.nested_sampling(maxiter=10)
        assert_equal(test_rel.__str__(), STRING_C)

    def test_str_d(self):
        """
        Test __str__ function d.
        """
        np.random.seed(1)
        test_y = np.ones(3) * np.random.randn(3)
        test_y_e = np.ones(3) * 0.1
        test_x = np.linspace(1, 10, 3)
        test_x_e = np.ones(3) * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            abscissa_uncertainty=test_x_e,
        )
        assert_equal(test_rel.__str__(), STRING_D)

    def test_str_e(self):
        """
        Test __str__ function d.
        """
        np.random.seed(1)
        test_y = np.ones(5) * np.random.randn(5)
        test_y_e = np.ones(5) * 0.1
        test_x = np.linspace(1, 10, 5)
        test_x_e = np.ones(5) * 0.1
        test_rel = Relationship(
            utils.straight_line,
            test_x,
            test_y,
            test_y_e,
            abscissa_uncertainty=test_x_e,
        )
        assert_equal(test_rel.__str__(), STRING_E)

    def test_str_f(self):
        """
        Test __str__ function F.
        """
        np.random.seed(1)
        test_y = np.ones(10) * np.random.randn(10)
        test_y_e = np.ones(10) * 0.1
        test_x = np.linspace(1, 10, 10)
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        test_rel.mcmc(n_burn=10, n_samples=10)
        assert_equal(test_rel.__str__(), STRING_F)

    def test_str_g(self):
        """
        Test __str__ function G.
        """
        np.random.seed(1)
        test_y = np.ones(10) * np.random.randn(10)
        test_y_e = np.ones(10) * 0.1
        test_x = np.linspace(1, 10, 10)
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        test_rel.mcmc(n_burn=10, n_samples=10)
        for var in test_rel.variables:
            var.normal = True
        assert_equal(test_rel.__str__(), STRING_G)

    def test_repr(self):
        """
        Test __repr__ function.
        """
        np.random.seed(1)
        test_y = np.ones(10) * np.random.randn(10)
        test_y_e = np.ones(10) * 0.1
        test_x = np.linspace(1, 10, 10)
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_equal(test_rel.__repr__(), STRING_A)

    def test_bic(self):
        """
        Test bayesian_information_criteria function.
        """
        test_x = np.linspace(0, 99, 10)
        test_y = np.ones(10)
        test_y_e = np.ones(10) * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        expected_bic = -23.06776100915812
        actual_bic = test_rel.bayesian_information_criteria()
        assert_almost_equal(actual_bic, expected_bic)

    def test_citations_a(self):
        """
        test citations a.
        """
        test_x = np.linspace(0, 99, 10)
        test_y = np.ones(10)
        test_y_e = np.ones(10) * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        assert_equal(test_rel.citations, CITATION_A)

    def test_citations_b(self):
        """
        test citations b.
        """
        test_x = np.linspace(0, 99, 10)
        test_y = np.ones(10) * 2
        test_y_e = np.ones(10) * 0.1
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e)
        test_rel.max_likelihood()
        assert_equal(test_rel.citations, CITATION_B)

    def test_citations_c(self):
        """
        test citations c.
        """
        test_x = np.linspace(0, 99, 10)
        test_y = (
            np.linspace(1, 199, 10)
            + np.linspace(1, 199, 10) * np.random.randn(10) * 0.05
        )
        test_y_e = test_y * 0.2
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e,)
        test_rel.max_likelihood()
        test_rel.mcmc(n_burn=10, n_samples=10)
        assert_equal(test_rel.citations, CITATION_C)

    def test_citations_d(self):
        """
        test citations d.
        """
        test_x = np.linspace(0, 99, 10)
        test_y = (
            np.linspace(1, 199, 10)
            + np.linspace(1, 199, 10) * np.random.randn(10) * 0.05
        )
        test_y_e = test_y * 0.2
        test_rel = Relationship(utils.straight_line, test_x, test_y, test_y_e,)
        test_rel.max_likelihood()
        test_rel.nested_sampling(maxiter=10)
        assert_equal(test_rel.citations, CITATION_D)
