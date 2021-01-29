## Suppy Chain Finance System

| 学号     | 姓名   | 分工       | 占比 |
| -------- | ------ | ---------- | ---- |
| 18340084 | 赖韵恬 | 报告、代码 | 50%  |
| 18340101 | 李芷阳 | 报告、代码 | 50%  |

#### 运行方式

1. 启动节点 
   `bash ~/fisco/nodes/127.0.0.1/start_all.sh`
2. 部署[Python SDK](https://github.com/FISCO-BCOS/python-sdk)
3. 编译并部署合约 
   `python3 console.py deploy qukuailian save`
4. 将run.py中的`contract_address`赋值为上一步部署的智能合约的地址
5. `python3 run.py`
