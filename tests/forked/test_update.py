import brownie


def test_update(n1, barb, barb2, owner):
    tx = n1.update_capitalization(1, "coNan", {'from': owner})

    assert tx.events["NameUpdated"].values() == (1, "Conan", "coNan")
    assert n1.summoner_name(1) == "coNan"


def test_update_fails(n1, barb, barb2, owner, accounts):
    with brownie.reverts("!owner or approved name"):
        n1.update_capitalization(1, "coNan", {'from': accounts[5]})

    with brownie.reverts("name different"):
        n1.update_capitalization(1, "Conan1", {'from': owner})