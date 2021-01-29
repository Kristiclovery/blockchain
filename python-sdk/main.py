import sys,os,json,traceback
from client.datatype_parser import DatatypeParser
from client.common.compiler import Compiler
from client_config import client_config
from client.bcosclient import BcosClient
from run import client,data_parser

def registercompany(contract_address,contract_abi,name,money):
    money=int(money)
    receipt=client.sendRawTransactionGetReceipt(contract_address,contract_abi,"RegisterCompany",[name,money])
    print("receipt:",receipt['output'])
    return receipt
    
def registerbank(contract_address,contract_abi,name,money):
    money=int(money)
    receipt=client.sendRawTransactionGetReceipt(contract_address,contract_abi,"RegisterBank",[name,money])
    print("receipt:",receipt['output'])
    return receipt

def getcompany(contract_address,contract_abi,name):
    receipt=client.sendRawTransactionGetReceipt(contract_address,contract_abi,"GetCompany",[name])
    txhash=receipt['transactionHash']
    txresponse=client.getTransactionByHash(txhash)
    inputresult=data_parser.parse_transaction_input(txresponse['input'])
    outputresult=data_parser.parse_receipt_output(inputresult['name'],receipt['output'])
    return outputresult

def getbank(contract_address,contract_abi,name):
    receipt=client.sendRawTransactionGetReceipt(contract_address,contract_abi,"GetBank",[name])
    txhash=receipt['transactionHash']
    txresponse=client.getTransactionByHash(txhash)
    inputresult=data_parser.parse_transaction_input(txresponse['input'])
    outputresult=data_parser.parse_receipt_output(inputresult['name'],receipt['output'])
    return outputresult

def getbill(contract_address,contract_abi,name):
    name=int(name)
    receipt=client.sendRawTransactionGetReceipt(contract_address,contract_abi,"GetBill",[name])
    txhash=receipt['transactionHash']
    txresponse=client.getTransactionByHash(txhash)
    inputresult=data_parser.parse_transaction_input(txresponse['input'])
    outputresult=data_parser.parse_receipt_output(inputresult['name'],receipt['output'])
    return outputresult

def createbill(contract_address,contract_abi,giver,receiver,middle,money,repaytime):
    money=int(money)
    repaytime=int(repaytime)
    receipt=client.sendRawTransactionGetReceipt(contract_address,contract_abi,"CreateBill",[giver,receiver,middle,money,repaytime])
    print("receipt:",receipt['output'])
    txhash=receipt['transactionHash']
    txresponse=client.getTransactionByHash(txhash)
    inputresult=data_parser.parse_transaction_input(txresponse['input'])
    outputresult=data_parser.parse_receipt_output(inputresult['name'],receipt['output'])
    return outputresult

def transfer(contract_address,contract_abi,giver,receiver,money):
    money=int(money)
    receipt=client.sendRawTransactionGetReceipt(contract_address,contract_abi,"Transfer",[giver,receiver,money])
    print("receipt:",receipt['output'])
    txhash=receipt['transactionHash']
    txresponse=client.getTransactionByHash(txhash)
    inputresult=data_parser.parse_transaction_input(txresponse['input'])
    outputresult=data_parser.parse_receipt_output(inputresult['name'],receipt['output'])
    return outputresult

def financing(contract_address,contract_abi,giver,receiver,money):
    money=int(money)
    receipt=client.sendRawTransactionGetReceipt(contract_address,contract_abi,"Financing",[giver,receiver,money])
    print("receipt:",receipt['output'])
    txhash=receipt['transactionHash']
    txresponse=client.getTransactionByHash(txhash)
    inputresult=data_parser.parse_transaction_input(txresponse['input'])
    outputresult=data_parser.parse_receipt_output(inputresult['name'],receipt['output'])
    return outputresult

def repay(contract_address,contract_abi,giver):
    receipt=client.sendRawTransactionGetReceipt(contract_address,contract_abi,"Repay",[giver])
    print("receipt:",receipt['output'])
    txhash=receipt['transactionHash']
    txresponse=client.getTransactionByHash(txhash)
    inputresult=data_parser.parse_transaction_input(txresponse['input'])
    outputresult=data_parser.parse_receipt_output(inputresult['name'],receipt['output'])
    return outputresult

def run():
    abi_file = "contracts/qukuailian.abi"
    data_parser = DatatypeParser()
    data_parser.load_abi_file(abi_file)
    contract_abi = data_parser.contract_abi
    contract_address = '0x83592a3cf1af302612756b8687c8dc7935c0ad1d'
    while(True):
        print("--------------------供应链金融平台--------------------")
        print("1.注册公司 2.注册银行 3.查询公司 4.查询银行 5.查询收据")
        print("6.采购     7.转让     8.融资     9.结算     10.退出")
        n=input()
        if n=='1':
            registercompany(contract_address,contract_abi)
        elif n=='2':
            registerbank(contract_address,contract_abi)
        elif n=='3':
            receipt=getcompany(contract_address,contract_abi)
            txhash=receipt['transactionHash']
            txresponse=client.getTransactionByHash(txhash)
            inputresult=data_parser.parse_transaction_input(txresponse['input'])
            outputresult=data_parser.parse_receipt_output(inputresult['name'],receipt['output'])
            print("output:",outputresult)
        elif n=='4':
            receipt=getbank(contract_address,contract_abi)
            txhash=receipt['transactionHash']
            txresponse=client.getTransactionByHash(txhash)
            inputresult=data_parser.parse_transaction_input(txresponse['input'])
            outputresult=data_parser.parse_receipt_output(inputresult['name'],receipt['output'])
            print("output:",outputresult)
        elif n=='5':
            receipt=getbill(contract_address,contract_abi)
            txhash=receipt['transactionHash']
            txresponse=client.getTransactionByHash(txhash)
            inputresult=data_parser.parse_transaction_input(txresponse['input'])
            outputresult=data_parser.parse_receipt_output(inputresult['name'],receipt['output'])
            print("output:",outputresult)
        elif n=='6':
            createbill(contract_address,contract_abi)
        elif n=='7':
            transfer(contract_address,contract_abi)
        elif n=='8':
            financing(contract_address,contract_abi)
        elif n=='9':
            repay(contract_address,contract_abi)
        elif n=='10':
            return

if __name__ == "__main__":
    client=BcosClient()
    run()
    client.finish()
