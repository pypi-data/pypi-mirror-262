from __future__ import annotations

from typing import Any

import numpy as np
import pytest
import xarray as xr
from module_utilities import cached

import thermoextrap as xtrap
import thermoextrap.legacy


class FixtureData:
    def __init__(self, n, nv, order=5, uoff=0.0, xoff=0.0, seed=0) -> None:
        self.order = order

        self.rs = np.random.RandomState(seed)
        self.uoff = uoff
        self.xoff = xoff

        self.u = self.rs.rand(n) + uoff
        self.x = self.rs.rand(n, nv) + xoff

        self.ub = self.rs.rand(n) + uoff
        self.xb = self.rs.rand(n, nv) + xoff
        self._cache: dict[str, Any] = {}

    # bunch of things to test
    @cached.prop
    def rdata(self):
        return xtrap.factory_data_values(
            uv=self.u, xv=self.x, order=self.order, central=False
        )

    @cached.prop
    def cdata(self):
        return xtrap.factory_data_values(
            uv=self.u, xv=self.x, order=self.order, central=True
        )

    @cached.prop
    def xdata(self):
        return xtrap.DataCentralMoments.from_vals(
            xv=self.x,
            uv=self.u,
            order=self.order,
            central=True,
            dims=["val"],
            axis=0,
        )

    @cached.prop
    def xdata_val(self):
        return xtrap.DataCentralMomentsVals.from_vals(
            xv=self.x, uv=self.u, order=self.order, central=True
        )

    @cached.prop
    def xrdata(self):
        return xtrap.DataCentralMoments.from_vals(
            xv=self.x,
            uv=self.u,
            order=self.order,
            central=False,
            dims=["val"],
            axis=0,
        )

    @cached.prop
    def xrdata_val(self):
        return xtrap.DataCentralMomentsVals.from_vals(
            xv=self.x,
            uv=self.u,
            order=self.order,
            central=False,
        )

    @property
    def beta0(self) -> float:
        return 0.5

    @property
    def betas(self):
        return [0.3, 0.4]

    @cached.prop
    def em(self):
        """Extrapolation model fixture"""

        em = thermoextrap.legacy.ExtrapModel(maxOrder=self.order)
        em.train(self.beta0, xData=self.x, uData=self.u, saveParams=True)

        return em

    # @staticmethod
    # def fix_ufunc_xufunc(ufunc, xufunc):

    #     ufunc_out = lambda x: float(ufunc(x))
    #     xufunc_out = lambda x: xufunc.avgdict[x]

    #     return ufunc_out, xufunc_out

    @cached.prop
    def u_xu_funcs(self):
        ufunc, xufunc = thermoextrap.legacy.buildAvgFuncs(self.x, self.u, self.order)
        return ufunc, xufunc

    @cached.prop
    def derivs_list(self):
        fs = [thermoextrap.legacy.symDerivAvgX(i) for i in range(self.order + 1)]
        ufunc, xufunc = self.u_xu_funcs

        return [fs[i](ufunc, xufunc) for i in range(self.order + 1)]

    def xr_test_raw(self, b, a=None) -> None:
        if a is None:
            a = self.rdata

        self.xr_test(a.u, b.u.sel(val=0))
        self.xr_test(a.xu, b.xu)

        for i in range(self.order):
            self.xr_test(a.u_selector[i], b.u_selector[i].sel(val=0))
            self.xr_test(a.xu_selector[i], b.xu_selector[i])

    def xr_test_central(self, b, a=None) -> None:
        if a is None:
            a = self.cdata

        self.xr_test(a.du, b.du.sel(val=0))
        self.xr_test(a.dxdu, b.dxdu)
        self.xr_test(a.xave, b.xave)

        for i in range(self.order):
            self.xr_test(a.du_selector[i], b.du_selector[i].sel(val=0))
            self.xr_test(a.dxdu_selector[i], b.dxdu_selector[i])
            self.xr_test(a.xave_selector[i], b.xave_selector[i])

    @staticmethod
    def xr_test(a, b) -> None:
        xr.testing.assert_allclose(a, b.transpose(*a.dims))


@pytest.fixture(params=[(100, 5)], scope="module")
def fixture(request):
    return FixtureData(*request.param)


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--run-slow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config) -> None:
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items) -> None:
    if config.getoption("--run-slow"):
        # --run-slow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


# an attempt for using fixtures better
# whatever, went with above

# def get_test_u_x(n, nv, uoff=0.0, xoff=0.0, seed=0):

#     if isinstance(nv, int):
#         nv = (nv,)

#     shape = (n,) + nv

#     rs = np.random.RandomState(seed)
#     u = rs.rand(n) + uoff
#     x = rs.rand(*shape) + xoff

#     return u, x


# class Fixture_Old:
#     def __init__(self, x, u, order):
#         self.x = x
#         self.u = u
#         self.order = order

#     @cached.prop
#     def u_xu_funcs(self):
#         ufunc, xufunc = thermoextrap.legacy.buildAvgFuncs(self.x, self.u, self.order)
#         return ufunc, xufunc

#     @cached.meth
#     def em(self, alpha0=0.5):
#         return thermoextrap.legacy.ExtrapModel(self.order, alpha0, self.x, self.u)


# class Fixture_New:
#     def __init__(self, data):
#         self.data = data

#     @cached.meth
#     def xem(self, alpha0=0.5, minus_log=False):
#         return xtrap.beta.factory_extrapmodel(alpha0=alpha0, data=self.data,
#                                              minus_log=minus_log)

#     def xr_test_raw(self, other):

#         self.xr_test(self.data.u, other.u.sel(val=0))
#         self.xr_test(self.data.xu, other.xu)

#         for i in range(self.data.order):
#             self.xr_test(self.data.u_selector[i], other.u_selector[i].sel(val=0))
#             self.xr_test(self.data.xu_selector[i], other.xu_selector[i])

#     def xr_test_central(self, other):

#         self.xr_test(self.data.du, other.du.sel(val=0))
#         self.xr_test(self.data.dxdu, other.dxdu)
#         self.xr_test(self.data.xave, other.xave)

#         for i in range(self.data.order):
#             self.xr_test(self.data.du_selector[i], other.du_selector[i].sel(val=0))
#             self.xr_test(self.data.dxdu_selector[i], other.dxdu_selector[i])
#             self.xr_test(self.data.xave_selector[i], other.xave_selector[i])

#     @staticmethod
#     def xr_test(a, b):
#         xr.testing.assert_allclose(a, b.transpose(*a.dims))


# @pytest.fixture
# def test_ux():
#     u, x = get_test_u_x(n=100, nv=5, uoff=0.0, xoff=0.0, seed=0)
#     return u, x, 5


# @pytest.fixture
# def fix_old(test_ux):
#     u, x, order = test_ux
#     return Fixture_Old(x=x, u=u, order=order)

# @pytest.fixture
# def fix_rdata(test_ux):
#     u, x, order = test_ux
#     data = xtrap.factory_data_values(uv=u, xv=x, order=order, central=False)
#     return Fixture_New(data)

# @pytest.fixture
# def fix_cdata(test_ux):
#     u, x, order = test_ux
#     data = xtrap.factory_data_values(uv=u, xv=x, order=order, central=True)
#     return Fixture_New(data)

# @pytest.fixture
# def fix_xdata(test_ux):
#     u, x, order = test_ux
#     data = xtrap.DataCentralMoments.from_vals(
#         xv=x, uv=u, order=order, central=True, dims=['val'])
#     return Fixture_New(data)

# @pytest.fixture
# def fix_xrdata(test_ux):
#     u, x, order = test_ux
#     data = xtrap.DataCentralMoments.from_vals(
#         xv=x, uv=u, order=order, central=False, dims=['val'])
#     return Fixture_New(data)

# @pytest.fixture
# def fix_xdata_val(test_ux):
#     u, x, order = test_ux
#     data = xtrap.DataCentralMomentsVals.from_vals(
#         xv=x, uv=u, order=order, central=True)
#     return Fixture_New(data)

# @pytest.fixture
# def fix_xrdata_val(test_ux):
#     u, x, order = test_ux
#     data = xtrap.DataCentralMomentsVals.from_vals(
#         xv=x, uv=u, order=order, central=False)
#     return Fixture_New(data)
