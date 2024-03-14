"""
fuyao debug app
通过命令行执行debug需求的功能，目前支持：
1. 检查所有的node的log，是否有exception，分析exception
2. 检查所有worker是否完成初始化
3. 检查是否有worker process 退出
4. 自动收集所有rank的stack
5. 自动收集火焰图
6. 自动检查设备是否出现异常；分析是否存在硬件告警及报错（syslog）
"""