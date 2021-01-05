pragma solidity ^0.5.0;

contract GUID {
    string private ID;
    mapping(string => string) private grades;


    constructor(string memory _ID) public {
        ID = _ID;
    }

    function setGrade(string memory _grade, string memory _class_name) public {
        grades[_class_name] = _grade;
    }

    function getGrade(string memory _class_name) view public returns (string memory) {
        return grades[_class_name];
    }

    function getID() view public returns (string memory) {
        return ID;
    }

}