# run the web

from flask import Flask,request,render_template,redirect
import glob
from main import *

global client
global data_parser
app = Flask(__name__)
client=BcosClient()
abi_file = "contracts/qukuailian.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi
contract_address = '0x98bc6df6b170d66fb5de93cf69b1f8746908f6d5'

def hex_to_signed(source):
	if not isinstance(source,str):
		raise ValueError("string type required")
	if 0==len(source):
		raise ValueError("string is empty")
	source=source[2:]
	if source=="":
		return 0
	sign_bit_mask=1<<(len(source)*4-1)
	other_bits_mask=sign_bit_mask-1
	value=int(source,16)
	return -(value & sign_bit_mask) | (value & other_bits_mask)

@app.route('/',methods=['GET','POST'])
def choice():
	return render_template('choice.html')

@app.route('/registerCompany',methods=['GET','POST'])
def registerc():
	return render_template('registercompany.html')

@app.route('/registerCompany/result',methods=['GET','POST'])
def registerc_re():
	name=request.form['cname']
	money=request.form['money']
	receipt=registercompany(contract_address,contract_abi,name,money)
	res=hex_to_signed(receipt['output'])
	print(res)
	if res==0:
		result="succeed"
	else:
		result="failed"
	return render_template('registercompany_result.html',cname=name,money=money,result=result)

@app.route('/registerBank',methods=['GET','POST'])
def registerb():
	return render_template('registerbank.html')

@app.route('/registerBank/result',methods=['GET','POST'])
def registerb_re():
	name=request.form['bname']
	money=request.form['money']
	receipt=registerbank(contract_address,contract_abi,name,money)
	res=hex_to_signed(receipt['output'])
	print(res)
	if res==0:
		result="succeed"
	else:
		result="failed"
	return render_template('registerbank_result.html',bname=name,money=money,result=result)

@app.route('/getCompany',methods=['GET','POST'])
def getc():
	return render_template('getcompany.html')

@app.route('/getCompany/result',methods=['GET','POST'])
def getc_re():
	name=request.form['cname']
	receipt=getcompany(contract_address,contract_abi,name)
	money=receipt[1]
	return render_template('getcompany_result.html',cname=name,money=money)

@app.route('/getBank',methods=['GET','POST'])
def getb():
	return render_template('getbank.html')

@app.route('/getBank/result',methods=['GET','POST'])
def getb_re():
	name=request.form['bname']
	receipt=getbank(contract_address,contract_abi,name)
	money=receipt[1]
	return render_template('getbank_result.html',bname=name,money=money)

@app.route('/getBill',methods=['GET','POST'])
def getbi():
	return render_template('getBi.html')

@app.route('/getBill/result',methods=['GET','POST'])
def getbi_re():
	bid=request.form['bid']
	receipt=getbill(contract_address,contract_abi,bid)
	giver=receipt[0]
	receiver=receipt[1]
	middle=receipt[2]
	Type=receipt[3]
	money=receipt[4]
	createdate=receipt[5]
	repaydate=receipt[6]
	return render_template('getBi_result.html',bid=bid,giver=giver,receiver=receiver,middle=middle,Type=Type,money=money,createdate=createdate,repaydate=repaydate)

@app.route('/createBill',methods=['GET','POST'])
def createB():
	return render_template('createB.html')

@app.route('/createBill/result',methods=['GET','POST'])
def createB_re():
	giver=request.form['giver']
	receiver=request.form['receiver']
	middle=request.form['middle']
	money=request.form['money']
	repaytime=request.form['repaytime']
	receipt=createbill(contract_address,contract_abi,giver,receiver,middle,money,repaytime)
	bid=receipt[0]
	if bid==-1:
		result="failed"
	else:
		result="succeed"
	return render_template('createB_result.html',bid=bid,giver=giver,receiver=receiver,middle=middle,money=money,repaytime=repaytime,result=result)

@app.route('/transfer',methods=['GET','POST'])
def billtransfer():
	return render_template('transfer.html')

@app.route('/transfer/result',methods=['GET','POST'])
def billtransfer_re():
	giver=request.form['giver']
	receiver=request.form['receiver']
	money=request.form['money']
	receipt=transfer(contract_address,contract_abi,giver,receiver,money)
	result=receipt[0]
	if result==0:
		result="succeed"
	else:
		result="failed"
	return render_template('transfer_result.html',giver=giver,receiver=receiver,money=money,result=result)

@app.route('/financing',methods=['GET','POST'])
def billfinancing():
	return render_template('financing.html')

@app.route('/financing/result',methods=['GET','POST'])
def billfinancing_re():
	giver=request.form['giver']
	receiver=request.form['receiver']
	money=request.form['money']
	receipt=financing(contract_address,contract_abi,giver,receiver,money)
	result=receipt[0]
	if result==0:
		result="succeed"
	else:
		result="failed"
	return render_template('financing_result.html',giver=giver,receiver=receiver,money=money,result=result)

@app.route('/repay',methods=['GET','POST'])
def billrepay():
	return render_template('repay.html')

@app.route('/repay/result',methods=['GET','POST'])
def billrepay_re():
	giver=request.form['giver']
	receipt=repay(contract_address,contract_abi,giver)
	result=receipt[0]
	if result==0:
		result="succeed"
	else:
		result="failed"
	return render_template('repay_result.html',giver=giver,result=result)



if __name__ == '__main__':
	app.debug = False
	app.run(host="0.0.0.0",port=80)
