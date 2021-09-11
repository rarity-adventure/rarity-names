import brownie


def test_claim(names, barb, owner, authority, gold):
    assert names.balanceOf(owner) == 0
    initial_gold = gold.balanceOf(barb)
    gold.approve(barb, authority, 1000e18, {'from': owner})
    tx = names.claim("Conan", barb, {'from': owner})
    name_id = tx.return_value

    assert "NameClaimed" in tx.events
    assert "NameMoved" in tx.events
    assert tx.events["NameClaimed"].values() == (owner, barb, "Conan", name_id)
    assert tx.events["NameMoved"].values() == (name_id, 0, barb)

    assert gold.balanceOf(barb) == initial_gold - 200e18
    assert names.balanceOf(owner) == 1
    assert names.ownerOf(1) == owner
    assert names.ownerOf(1) == owner
    assert names.tokenOfOwnerByIndex(owner, 0) == 1
    assert names.totalSupply() == 1
    assert names.tokenByIndex(0) == 1

    assert names.summoner_name(barb) == "Conan"
    assert names.name_id_to_summoner(1) == barb
    assert names.summoner_to_name_id(barb) == 1
    assert names.is_name_claimed("Conan")
    assert names.is_name_claimed("coNan")
    assert not names.is_name_claimed("coNan1")


def test_mint_fails(names, barb, owner, authority, gold):
    gold.approve(barb, authority, 1000e18, {'from': owner})
    names.claim("Conan", barb, {'from': owner})

    with brownie.reverts("name taken"):
        names.claim("Conan", barb, {'from': owner})

    with brownie.reverts("to already named"):
        names.claim("Conan the Barbarian", barb, {'from': owner})


def test_mint_second(names, barb, owner, authority, gold):
    gold.approve(barb, authority, 1000e18, {'from': owner})
    names.claim("Conan", barb, {'from': owner})
    gold.approve(466591, authority, 1000e18, {'from': owner})
    names.claim("Conan2", 466591, {'from': owner})
    assert names.balanceOf(owner) == 2
    assert names.ownerOf(2) == owner
    assert names.tokenOfOwnerByIndex(owner, 1) == 2
    assert names.totalSupply() == 2
    assert names.tokenByIndex(1) == 2
    assert names.summoner_name(466591) == "Conan2"
    assert names.name_id_to_summoner(2) == 466591
    assert names.summoner_to_name_id(466591) == 2
    assert names.is_name_claimed("Conan2")
    assert names.is_name_claimed("coNan")

