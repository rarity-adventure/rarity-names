import brownie


def test_assign(n1, barb, barb2, owner):
    tx = n1.assign_name(1, barb2, {'from': owner})
    assert n1.summoner_name(barb) == ""
    assert n1.summoner_name(barb2) == "Conan"
    assert tx.events["NameAssigned"].values() == (1, barb, barb2)
    assert n1.summoner_to_name_id(barb) == 0
    assert n1.summoner_to_name_id(barb2) == 1
    assert n1.name_id_to_summoner(1) == barb2


def test_assign_fails(n1, barb, barb2, owner, accounts):
    with brownie.reverts("!owner or approved name"):
        n1.assign_name(1, barb2, {'from': accounts[4]})

    with brownie.reverts("to already named"):
        n1.assign_name(1, barb, {'from': owner})

    with brownie.reverts("sorry summoner 0"):
        n1.assign_name(1, 0, {'from': owner})

    with brownie.reverts():
        n1.assign_name(2, barb2, {'from': owner})

    with brownie.reverts("!owner or approved to"):
        n1.assign_name(1, 1, {'from': owner})


def test_clear(n1, barb, barb2, owner):
    tx = n1.clear_summoner_name(barb, {'from': owner})

    assert n1.summoner_name(barb) == ""
    assert n1.summoner_name(barb2) == ""
    assert tx.events["NameAssigned"].values() == (1, barb, 0)
    assert n1.summoner_to_name_id(barb) == 0
    assert n1.summoner_to_name_id(barb2) == 0
    assert n1.name_id_to_summoner(1) == 0


def test_clear_fails(n1, barb, barb2, owner, accounts):
    with brownie.reverts("!owner or approved"):
        n1.clear_summoner_name(barb, {'from': accounts[4]})
