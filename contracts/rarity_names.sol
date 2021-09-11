// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

interface rarity_manifested {
    function getApproved(uint) external view returns (address);
    function ownerOf(uint) external view returns (address);
}

interface rarity_gold {
    function transferFrom(uint executor, uint from, uint to, uint amount) external returns (bool);
}

contract rarity_names is ERC721Enumerable {
    uint private next_name = 1;

    rarity_manifested constant _rm = rarity_manifested(0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb);
    rarity_gold constant _gold = rarity_gold(0x2069B76Afe6b734Fb65D1d099E7ec64ee9CC76B2);

    uint public immutable NAME_AUTHORITY = 1337;
    uint public immutable NAME_GOLD_PRICE = 200e18;

    mapping(uint => string) public names;  // token => name
    mapping(uint => uint) public summoner_to_name_id; // summoner => token
    mapping(uint => uint) public name_id_to_summoner; // token => summoner
    mapping(string => bool) public is_name_claimed;

    event Claimed(address indexed owner, uint indexed summoner, string name);
    event Changed(uint indexed previous_summoner, uint indexed new_summoner, string name);

    constructor() ERC721("Rarity Names", "names") {

    }

    function _isApprovedOrOwner(uint _summoner) internal view returns (bool) {
        return _rm.getApproved(_summoner) == msg.sender || _rm.ownerOf(_summoner) == msg.sender;
    }

    function summoner_name(uint summoner) public view returns (string memory name){
        name = names[summoner_to_name_id[summoner]];
    }

    // @dev Claim a name for a summoner. Summoner must hold the required gold.
    function claim(string memory name, uint summoner) public returns (uint name_id){
        require(_isApprovedOrOwner(summoner), '!owner');
        require(validate_name(name), 'invalid name');
        string memory lower_name = to_lower(name);
        require(!is_name_claimed[lower_name], 'name taken');
        _gold.transferFrom(NAME_AUTHORITY, summoner, NAME_AUTHORITY, NAME_GOLD_PRICE);
        _mint(msg.sender, next_name);
        name_id = next_name;
        next_name++;
        names[name_id] = name;
        is_name_claimed[lower_name] = true;
        transfer_name(name_id, summoner);
    }

    // @dev Transfer a name to a summoner
    function transfer_name(uint name_id, uint to) public {
        require(to > 0, "sorry summoner 0");
        require(_isApprovedOrOwner(msg.sender, name_id), "!owner or approved");
        require(summoner_to_name_id[to] > 0, "to already named");
        uint from = name_id_to_summoner[name_id];
        if (from > 0) {
            summoner_to_name_id[from] = 0;
        }
        summoner_to_name_id[to] = name_id;
        name_id_to_summoner[name_id] = to;
    }

    // @dev Unlink a name from a summoner without transferring it.
    //      Use transfer_name to reassign the name.
    function clear_summoner_name(uint summoner) public {
        uint name_id = summoner_to_name_id[summoner];
        require(_isApprovedOrOwner(summoner) || _isApprovedOrOwner(msg.sender, name_id), "!owner or approved");
        summoner_to_name_id[summoner] = 0;
        name_id_to_summoner[name_id] = 0;
    }

    // @dev Check if the name string is valid (Alphanumeric and spaces without leading or trailing space)
    function validate_name(string memory str) public pure returns (bool){
        bytes memory b = bytes(str);
        if(b.length < 1) return false;
        if(b.length > 25) return false; // Cannot be longer than 25 characters
        if(b[0] == 0x20) return false; // Leading space
        if (b[b.length - 1] == 0x20) return false; // Trailing space

        bytes1 last_char = b[0];

        for(uint i; i<b.length; i++){
            bytes1 char = b[i];

            if (char == 0x20 && last_char == 0x20) return false; // Cannot contain continous spaces

            if(
                !(char >= 0x30 && char <= 0x39) && //9-0
                !(char >= 0x41 && char <= 0x5A) && //A-Z
                !(char >= 0x61 && char <= 0x7A) && //a-z
                !(char == 0x20) //space
            )
                return false;

            last_char = char;
        }

        return true;
    }

    // @dev Converts the string to lowercase
    function to_lower(string memory str) public pure returns (string memory){
        bytes memory b_str = bytes(str);
        bytes memory b_lower = new bytes(b_str.length);
        for (uint i = 0; i < b_str.length; i++) {
            // Uppercase character
            if ((uint8(b_str[i]) >= 65) && (uint8(b_str[i]) <= 90)) {
                b_lower[i] = bytes1(uint8(b_str[i]) + 32);
            } else {
                b_lower[i] = b_str[i];
            }
        }
        return string(b_lower);
    }
}
