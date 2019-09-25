pragma solidity ^0.5.0;

contract PathFinder {

  uint public markerCount = 0;
  uint public targetCount = 0;

  struct Marker {
    uint id;
    string description;
    string latitude;
    string longitude;
    string progress;
    string status;
    address user_address;
  }


  struct Target {
    uint id;
    string name;
    string latitude;
    string longitude;
  }

  mapping(uint => Target) public targets;

  mapping(uint => Marker) public markers;

  constructor() public {
    createTarget("C.I.A.M.", "38.189553", "15.552480");
    createTarget("Dipartimento di Ingegneria", "38.258698", "15.597270" );
  }

  function createMarker(string memory _description, string memory _latitude, string memory _longitude, string memory _progress, string memory _status, address _user) public {
    markerCount ++;
    markers[markerCount] = Marker(markerCount, _description, _latitude, _longitude, _progress, _status, _user);
  }

  function createTarget(string memory _name, string memory _latitude, string memory _longitude) public {
    targetCount ++;
    targets[targetCount] = Target(targetCount, _name, _latitude, _longitude);
  }

  function submitMarker(string memory _description, string memory _latitude, string memory _longitude, string memory _progress, string memory _status, bytes32 _hash, bytes memory sig) public {
    address user = recoverAddr(_hash, sig);
    createMarker(_description, _latitude, _longitude, _progress, _status, user);
  }

  function getMarker(uint _id) public view returns (uint, string memory, string memory, string memory, string memory, string memory, address) {
    return (
      markers[_id].id, markers[_id].description, markers[_id].latitude, markers[_id].longitude, markers[_id].progress, markers[_id].status, markers[_id].user_address
      );
  }

  function getTarget(uint _id) public view returns (uint, string memory, string memory, string memory) {
    return (
      targets[_id].id, targets[_id].name, targets[_id].latitude, targets[_id].longitude
      );
  }

  function updateMarker(uint _id, string memory _latitude, string memory _longitude) public {
    markers[_id].latitude = _latitude;
    markers[_id].longitude = _longitude;
  }

  function getMarkerCount() public view returns (uint) {
    return markerCount;
  }

  function getTargetCount() public view returns (uint) {
    return targetCount;
  }

  function recoverAddr(bytes32 hash, bytes memory sig) internal pure returns (address) {
    bytes32 r;
    bytes32 s;
    uint8 v;

    //Check the signature length
    if (sig.length != 65) {
      return (address(0));
    }

    // Divide the signature in r, s and v variables
    // ecrecover takes the signature parameters, and the only way to get them
    // currently is to use assembly.
    // solium-disable-next-line security/no-inline-assembly
    assembly {
      r := mload(add(sig, 32))
      s := mload(add(sig, 64))
      v := byte(0, mload(add(sig, 96)))
    }

    // Version of signature should be 27 or 28, but 0 and 1 are also possible versions
    if (v < 27) {
      v += 27;
    }

    // If the version is correct return the signer address
    if (v != 27 && v != 28) {
      return (address(0));
    } else {
      return ecrecover(hash, v, r, s);
    }
  }



}
