import pytest
import numpy as np
from gradient_free_optimizers import RandomSearchOptimizer

from surfaces.mathematical_functions import (
    SphereFunction,
    RastriginFunction,
    AckleyFunction,
    RosenbrockFunction,
    BealeFunction,
    HimmelblausFunction,
    HölderTableFunction,
    CrossInTrayFunction,
    SimionescuFunction,
    EasomFunction,
    BoothFunction,
    GoldsteinPriceFunction,
    StyblinskiTangFunction,
    BukinFunctionN6,
)

sphere_function = SphereFunction(2)
rastrigin_function = RastriginFunction(2)
ackley_function = AckleyFunction()
rosenbrock_function = RosenbrockFunction(2)
beale_function = BealeFunction()
himmelblaus_function = HimmelblausFunction()
hölder_table_function = HölderTableFunction()
cross_in_tray_function = CrossInTrayFunction()
simionescu_function = SimionescuFunction()
easom_function = EasomFunction()
booth_function = BoothFunction()
goldstein_price_function = GoldsteinPriceFunction()
styblinski_tang_function = StyblinskiTangFunction(2)
bukin_function_n6 = BukinFunctionN6()


objective_function_para_2D = (
    "test_function",
    [
        (sphere_function),
        (rastrigin_function),
        (ackley_function),
        (rosenbrock_function),
        (beale_function),
        (himmelblaus_function),
        (hölder_table_function),
        (cross_in_tray_function),
        (simionescu_function),
        (easom_function),
        (booth_function),
        (goldstein_price_function),
        (styblinski_tang_function),
        (bukin_function_n6),
    ],
)


@pytest.mark.parametrize(*objective_function_para_2D)
def test_optimization_2D(test_function):
    search_space = {
        "x0": np.arange(0, 100, 1),
        "x1": np.arange(0, 100, 1),
    }

    opt = RandomSearchOptimizer(search_space)
    opt.search(test_function.objective_function, n_iter=30)


############################################################

sphere_function = SphereFunction(3)
rastrigin_function = RastriginFunction(3)
rosenbrock_function = RosenbrockFunction(3)


objective_function_para_3D = (
    "test_function",
    [
        (sphere_function),
        (rastrigin_function),
        (rosenbrock_function),
    ],
)


@pytest.mark.parametrize(*objective_function_para_3D)
def test_optimization_3D(test_function):
    search_space = {
        "x0": np.arange(0, 100, 1),
        "x1": np.arange(0, 100, 1),
        "x2": np.arange(0, 100, 1),
    }

    opt = RandomSearchOptimizer(search_space)
    opt.search(test_function.objective_function, n_iter=30)


############################################################

sphere_function = SphereFunction(4)
rastrigin_function = RastriginFunction(4)
rosenbrock_function = RosenbrockFunction(4)


objective_function_para_4D = (
    "test_function",
    [
        (sphere_function),
        (rastrigin_function),
        (rosenbrock_function),
    ],
)


@pytest.mark.parametrize(*objective_function_para_4D)
def test_optimization_4D(test_function):
    search_space = {
        "x0": np.arange(0, 100, 1),
        "x1": np.arange(0, 100, 1),
        "x2": np.arange(0, 100, 1),
        "x3": np.arange(0, 100, 1),
    }

    opt = RandomSearchOptimizer(search_space)
    opt.search(test_function.objective_function, n_iter=30)
