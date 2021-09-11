import pytest
from brownie import *

@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    pass


@pytest.fixture(scope="module")
def rm():
    yield Contract.from_explorer("0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb")


@pytest.fixture(scope="module")
def gold():
    yield Contract.from_explorer("0x2069B76Afe6b734Fb65D1d099E7ec64ee9CC76B2")


@pytest.fixture(scope="module")
def barb(rm):
    yield 466576


@pytest.fixture(scope="module")
def barb2(rm):
    yield 466591


@pytest.fixture(scope="module")
def owner(rm):
    yield accounts[-1]


@pytest.fixture(scope="module")
def authority():
    yield 1317313


@pytest.fixture(scope="module")
def names(accounts, rm, owner):
    names = rarity_names.deploy({'from': accounts[0]})
    rm.transferFrom(owner, names, 1317313, {'from': owner})
    yield names


@pytest.fixture(scope="module")
def n1(gold, barb, authority, owner, names):
    gold.approve(barb, authority, 1000e18, {'from': owner})
    names.claim("Conan", barb, {'from': owner})
    yield names
