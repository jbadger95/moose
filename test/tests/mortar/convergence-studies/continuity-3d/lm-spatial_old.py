import mms
import unittest
import sympy
from sympy import sin, pi, cos
def fuzzyEqual(test_value, true_value, tolerance):
    return abs(test_value - true_value) / abs(true_value) < tolerance
class TestContinuity(unittest.TestCase):
# class TestContinuity(object):
    def __init__(self, methodName='runTest'):
        super(TestContinuity, self).__init__(methodName)
        exact_soln = 'sin(pi*x) * sin(pi*y) * sin(pi*z)'
        f, exact = mms.evaluate('-div(grad(T)) + T', exact_soln, variable='T')
        x,y,z = sympy.symbols('x y z')
        u = eval(str(exact).replace('R.x','x').replace('R.y','y').replace('R.z','z'))
        du_dx = sympy.diff(u, x)
        lm = du_dx
        self.function_args = [
            'Functions/forcing_function/value="' + mms.fparser(f) + '"',
            'Functions/exact_soln_primal/value="' + mms.fparser(exact) + '"',
            'Functions/exact_soln_lambda/value="' + mms.fparser(lm) + '"']
        self.gold_values = {
            'p1p0-u_0' : 1.9527311839612733,
            'p1p0-lm_0' : 1.0074018502991284,
            'p1p1-u_0' : 1.9261022315757947,
            'p1p1-lm_0' : 2.0219548308141335,
            'p1p1dual-u_0' : 1.9261022315758136,
            'p1p1dual-lm_0' : 1.4803634663860212,
            'p2p0-u_0' : 3.02831459237971,
            'p2p0-lm_0' : 1.0216165211724608,
            'p2p1-u_0' : 2.9909837229093217,
            'p2p1-lm_0' : 2.03216049463456,
            'p2p2-u_0' : 2.97001208916348,
            'p2p2-lm_0' : 2.982767657075597,
            'p1p0mixed-u_0.1' : 1.8375145189885218,
            'p1p0mixed-lm_0.1' : 0.8860253144660545,
            'p1p0tet-u_0.1' : 1.8181774968755893,
            'p1p0tet-lm_0.1' : 1.097405734029184
        }

        self.tolerance = 1e-3
    def do_plot(self, input_file, num_refinements, cli_args, figure, label, mpi=1):
        cli_args = " ".join(cli_args + self.function_args)
        df = mms.run_spatial(input_file,
                             num_refinements,
                             cli_args,
                             x_pp='h',
                             y_pp=['L2u', 'L2lambda'],
                             mpi=mpi)
        figure.plot(df,
                    label=['u_' + label, 'lm_' + label],
                    num_fitted_points=3,
                    slope_precision=1,
                    marker='o')
    def secondary_and_primary_plots(self,
                               fine,
                               num_refinements,
                               additional_cli_args,
                               name,
                               plots_to_do=None,
                               mpi=1):
        fig = mms.ConvergencePlot('Element Size ($h$)', ylabel='$L_2$ Error')
        has_tets = False
        for cli_arg in additional_cli_args:
            if "TET" in cli_arg:
                has_tets = True
        if has_tets:
            deltas = [0.1]
        else:
            deltas = [0]
        for delta in deltas:
            self.do_plot('continuity.i',
                         num_refinements,
                         ["Constraints/mortar/delta="+str(delta)] + additional_cli_args,
                         fig,
                         str(delta),
                         mpi)
        fig.set_title(name)
        fig.save(name+'.png')
        return fig
    def run_geometric_discretization(self, geom_disc, fine_values, num_refinements, mpi=1):
        if geom_disc == "p1p0":
            cli_args = ["Variables/T/order=FIRST",
                        "Variables/lambda/family=MONOMIAL",
                        "Variables/lambda/order=CONSTANT",
                        "Variables/lambda/use_dual=false",
                        "Mesh/left_block/nx=1",
                        "Mesh/left_block/ny=1",
                        "Mesh/left_block/nz=1",
                        "Mesh/left_block/elem_type=HEX8",
                        "Mesh/right_block/nx=1",
                        "Mesh/right_block/ny=1",
                        "Mesh/right_block/nz=1",
                        "Mesh/right_block/elem_type=HEX8"]
        elif geom_disc == "p1p1":
            cli_args = ["Variables/T/order=FIRST",
                        "Variables/lambda/family=LAGRANGE",
                        "Variables/lambda/order=FIRST",
                        "Variables/lambda/use_dual=false",
                        "Mesh/left_block/nx=1",
                        "Mesh/left_block/ny=1",
                        "Mesh/left_block/nz=1",
                        "Mesh/left_block/elem_type=HEX8",
                        "Mesh/right_block/nx=1",
                        "Mesh/right_block/ny=1",
                        "Mesh/right_block/nz=1",
                        "Mesh/right_block/elem_type=HEX8"]
        elif geom_disc == "p1p1dual":
            cli_args = ["Variables/T/order=FIRST",
                        "Variables/lambda/family=LAGRANGE",
                        "Variables/lambda/order=FIRST",
                        "Variables/lambda/use_dual=true",
                        "Mesh/left_block/nx=1",
                        "Mesh/left_block/ny=1",
                        "Mesh/left_block/nz=1",
                        "Mesh/left_block/elem_type=HEX8",
                        "Mesh/right_block/nx=1",
                        "Mesh/right_block/ny=1",
                        "Mesh/right_block/nz=1",
                        "Mesh/right_block/elem_type=HEX8"]
        elif geom_disc == "p2p0":
            cli_args = ["Mesh/second_order=true",
                        "Variables/T/order=SECOND",
                        "Variables/lambda/family=MONOMIAL",
                        "Variables/lambda/order=CONSTANT",
                        "Variables/lambda/use_dual=false",
                        "Mesh/left_block/nx=1",
                        "Mesh/left_block/ny=1",
                        "Mesh/left_block/nz=1",
                        "Mesh/left_block/elem_type=HEX27",
                        "Mesh/right_block/nx=1",
                        "Mesh/right_block/ny=1",
                        "Mesh/right_block/nz=1",
                        "Mesh/right_block/elem_type=HEX27"]
        elif geom_disc == "p2p1":
            cli_args = ["Mesh/second_order=true",
                        "Variables/T/order=SECOND",
                        "Variables/lambda/family=LAGRANGE",
                        "Variables/lambda/order=FIRST",
                        "Variables/lambda/use_dual=false",
                        "Mesh/left_block/nx=1",
                        "Mesh/left_block/ny=1",
                        "Mesh/left_block/nz=1",
                        "Mesh/left_block/elem_type=HEX27",
                        "Mesh/right_block/nx=1",
                        "Mesh/right_block/ny=1",
                        "Mesh/right_block/nz=1",
                        "Mesh/right_block/elem_type=HEX27"]
        elif geom_disc == "p2p2":
            cli_args = ["Mesh/second_order=true",
                        "Variables/T/order=SECOND",
                        "Variables/lambda/family=LAGRANGE",
                        "Variables/lambda/order=SECOND",
                        "Variables/lambda/use_dual=false",
                        "Mesh/left_block/nx=1",
                        "Mesh/left_block/ny=1",
                        "Mesh/left_block/nz=1",
                        "Mesh/left_block/elem_type=HEX27",
                        "Mesh/right_block/nx=1",
                        "Mesh/right_block/ny=1",
                        "Mesh/right_block/nz=1",
                        "Mesh/right_block/elem_type=HEX27"]
        elif geom_disc == "p1p0mixed":
            cli_args = ["Mesh/second_order=false",
                        "Variables/T/order=FIRST",
                        "Variables/lambda/family=MONOMIAL",
                        "Variables/lambda/order=CONSTANT",
                        "Variables/lambda/use_dual=false",
                        "Mesh/left_block/nx=1",
                        "Mesh/left_block/ny=1",
                        "Mesh/left_block/nz=1",
                        "Mesh/left_block/elem_type=TET4",
                        "Mesh/right_block/nx=1",
                        "Mesh/right_block/ny=1",
                        "Mesh/right_block/nz=1",
                        "Mesh/right_block/elem_type=HEX8"]
        elif geom_disc == "p1p0tet":
            cli_args = ["Mesh/second_order=false",
                        "Variables/T/order=FIRST",
                        "Variables/lambda/family=MONOMIAL",
                        "Variables/lambda/order=CONSTANT",
                        "Variables/lambda/use_dual=false",
                        "Mesh/left_block/nx=1",
                        "Mesh/left_block/ny=1",
                        "Mesh/left_block/nz=1",
                        "Mesh/left_block/elem_type=TET4",
                        "Mesh/right_block/nx=1",
                        "Mesh/right_block/ny=1",
                        "Mesh/right_block/nz=1",
                        "Mesh/right_block/elem_type=TET4"]
        name_to_slope = {}
        for fine_value in fine_values:
            name = geom_disc
            fig = self.secondary_and_primary_plots(fine_value,
                                              num_refinements,
                                              cli_args,
                                              name,
                                              mpi=mpi)
            for key, value in fig.label_to_slope.items():
                name_to_slope.update({"-".join([name, key]) : value})
        for key, test_value in name_to_slope.items():
            # print("{} : {}".format(key, test_value))
            gold_value = self.gold_values.get(key)
            self.assertIsNotNone(gold_value)
            self.assertTrue(fuzzyEqual(test_value, gold_value, self.tolerance))
    def do_it_all(self, fine_values, num_refinements, mpi=1):
         self.run_geometric_discretization("p1p0", fine_values, num_refinements, mpi)
         self.run_geometric_discretization("p1p1", fine_values, num_refinements, mpi)
         self.run_geometric_discretization("p1p1dual", fine_values, num_refinements, mpi)
         self.run_geometric_discretization("p2p0", fine_values, num_refinements, mpi)
         self.run_geometric_discretization("p2p1", fine_values, num_refinements, mpi)
         self.run_geometric_discretization("p2p2", fine_values, num_refinements, mpi)
         self.run_geometric_discretization("p1p0mixed", fine_values, num_refinements, mpi)
         self.run_geometric_discretization("p1p0tet", fine_values, num_refinements, mpi)
         for key, test_value in self.gold_values.items():
             print("{} : {}".format(key, test_value))

class P1P0(TestContinuity):
    def testP1P0(self, fine_values=[2], num_refinements=4, mpi=1):
        self.run_geometric_discretization("p1p0", fine_values, num_refinements, mpi)
class P1P1(TestContinuity):
    def testP1P1(self, fine_values=[2], num_refinements=4, mpi=1):
        self.run_geometric_discretization("p1p1", fine_values, num_refinements, mpi)
class P1P1dual(TestContinuity):
    def testP1P1(self, fine_values=[2], num_refinements=4, mpi=1):
        self.run_geometric_discretization("p1p1dual", fine_values, num_refinements, mpi)
class P2P0(TestContinuity):
    def testP2P0(self, fine_values=[2], num_refinements=4, mpi=1):
        self.run_geometric_discretization("p2p0", fine_values, num_refinements, mpi)
class P2P1(TestContinuity):
    def testP2P1(self, fine_values=[2], num_refinements=4, mpi=1):
        self.run_geometric_discretization("p2p1", fine_values, num_refinements, mpi)
class P2P2(TestContinuity):
    def testP2P2(self, fine_values=[2], num_refinements=4, mpi=1):
        self.run_geometric_discretization("p2p2", fine_values, num_refinements, mpi)
class P1P0Mixed(TestContinuity):
    def testP1P0(self, fine_values=[2], num_refinements=4, mpi=1):
        self.run_geometric_discretization("p1p0mixed", fine_values, num_refinements, mpi)
class P1P0Tet(TestContinuity):
    def testP1P0(self, fine_values=[2], num_refinements=4, mpi=1):
        self.run_geometric_discretization("p1p0tet", fine_values, num_refinements, mpi)

if __name__ == '__main__':
    unittest.main(__name__, verbosity=2)
# instance = TestContinuity()
# instance.do_it_all([3], 8, 32)
# # instance.secondary_and_primary_plots(2,
# #                                 8,
# #                                 "Mesh/second_order=false " + \
# #                                 "Variables/T/order=FIRST " + \
# #                                 "Variables/lambda/family=MONOMIAL " + \
# #                                 "Variables/lambda/order=CONSTANT",
# #                                 "p1p0-asymptotic-same",
# #                                 ['same'],
# #                                 32)
