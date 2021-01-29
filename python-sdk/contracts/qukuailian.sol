pragma solidity>=0.4.24 <0.6.11;

contract qukuailian {
	struct Bill {
		string giver;
		string receiver;
    	string middle;
		uint Type;
		int money;
		uint createdate;
		uint repaydate;
	}

	struct Company {
		string name;
		int money;
		bool isused;
	}
	struct Bank {
		string name;
		int money;
		bool isused;
	}

	int lenCom;
	int lenBank;
	int lenBill;
	mapping(string => Company) Companys;
	mapping(string => Bank) Banks;
	mapping(int => Bill) Bills;

	constructor() public {
		lenCom = 0;
		lenBill = 0;
		lenBank = 0;
	}

	function isEqual(string a, string b) public returns(bool) {
		if (bytes(a).length != bytes(b).length) {
			return false;
        	}
		for (uint i=0; i< bytes(a).length; i++) {
			if (bytes(a)[i] != bytes(b)[i]) {
				return false;
            		}
		}
		return true;
	}

	function CreateBill(string giver, string receiver, string middle, int money, uint repaytime) public returns(int) {
		if (Companys[giver].isused && Companys[receiver].isused && !isEqual(giver, receiver)) {
			Bills[lenBill++] = Bill(giver, receiver, middle, 1, money, now, now + 60*repaytime);
			return lenBill-1;
		}
		return -1;
	}

	function CheckTransfer(string giver, string receiver) public returns(int) {
		int sum = 0;
		if(Companys[giver].isused && Companys[receiver].isused && !isEqual(giver, receiver)) {
			for (int i=0; i<lenBill; i++) {
				if ((Bills[i].Type == 1 || Bills[i].Type == 2) && isEqual(Bills[i].receiver, giver) && !isEqual(Bills[i].giver, receiver)) {
					sum += Bills[i].money;
					
				}
			}
			return sum;
		}
		return -1;
	}

	function Transfer(string giver, string receiver, int money) public returns(int) {
		int sum = money;
		if (CheckTransfer(giver, receiver) >= money) {
			for (int i=0; i<lenBill; i++) {
				if ((Bills[i].Type == 1 || Bills[i].Type == 2) && isEqual(Bills[i].receiver, giver) && !isEqual(Bills[i].giver, receiver)){
					if(Bills[i].money > sum){
						Bills[i].money -= sum;
						Bills[lenBill++] = Bill(Bills[i].giver, receiver,Bills[i].middle, 2, sum, Bills[i].createdate, Bills[i].repaydate);
						sum = 0;
					}
					else{
						Bills[i].receiver = receiver;
						Bills[i].Type = 2;
						sum -= Bills[i].money;
					}
					if(sum == 0)
						break;
				}
			}
			return 0;
		}
		return -1;
	}
	function CheckFinancing(string giver, string receiver) public returns(int) {
		int sum = 0;
		if(Companys[giver].isused && Banks[receiver].isused){
			for(int i=0;i<lenBill;i++){
				if ((Bills[i].Type == 1 || Bills[i].Type == 2) && isEqual(Bills[i].receiver,giver)){
					sum += Bills[i].money;
				}
			}
			return sum;
		}
		return -1;
	}
	function Financing(string giver, string receiver, int money) public returns(int) {
		int sum = money;
		if(CheckFinancing(giver,receiver) >= money) {
			for(int i=0;i<lenBill;i++){
				if ((Bills[i].Type == 1 || Bills[i].Type == 2) && isEqual(Bills[i].receiver,giver)){
					if(Bills[i].money > sum){
						Bills[i].money -= sum;
						Bills[lenBill++] = Bill(Bills[i].giver, receiver, Bills[i].middle, 3, sum, Bills[i].createdate, Bills[i].repaydate);
						sum = 0;
					}
					else{
						Bills[i].receiver=receiver;
						Bills[i].Type = 3;
						sum -= Bills[i].money;
					}
					if(sum == 0)
						break;
				}
			}
			Companys[giver].money += money;
			Banks[receiver].money -= money;
			return 0;
		}
		return -1;
	}

	function CheckRepay(string giver) public returns(int) {
		int sum = 0;
		if (Companys[giver].isused) {
			for (int i=0; i<lenBill; i++) {
				if (isEqual(Bills[i].giver, giver) && Bills[i].Type != 0 && now >= Bills[i].repaydate) {
					sum += Bills[i].money;
				}
			}
			return sum;
		}
		return -1;
	}

	function Repay(string giver) public returns(int) {
		int sum = 0;
		int m=CheckRepay(giver);
		if (m != -1 && m <= Companys[giver].money) {
			for (int i=0; i<lenBill; i++) {
				if (isEqual(Bills[i].giver, giver) && Bills[i].Type != 0 && now >= Bills[i].repaydate) {
					Bills[i].Type = 0;
					sum += Bills[i].money;
					Companys[Bills[i].receiver].money += Bills[i].money;
					Banks[Bills[i].receiver].money += Bills[i].money;
				}
			}
			Companys[giver].money -= sum;
			return sum;
		}
		return -1;
	}

	function RegisterCompany(string memory name, int money) public{
		Companys[name] = Company(name, money, true);
		lenCom++;
	}
	function RegisterBank(string memory name, int money) public{
		Banks[name] = Bank(name, money, true);
		lenBank++;
	}

	function GetCompany(string memory name) public view returns(string memory, int) {
		return (Companys[name].name, Companys[name].money);
	}
	function GetBank(string memory name) public view returns(string memory, int) {
		return (Banks[name].name, Banks[name].money);
	}
	function GetBill(int id) public view returns(string memory, string memory,string memory, uint, int, uint, uint) {
		return (Bills[id].giver, Bills[id].receiver,Bills[id].middle, Bills[id].Type, Bills[id].money, Bills[id].createdate, Bills[id].repaydate);
	}
}
