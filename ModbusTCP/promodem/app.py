from ModbusTCP.core.client import ModbusClient

def start():
    c = ModbusClient(host="192.168.1.42", port=502, auto_open=True, auto_close=True, timeout=1, debug=True)
    c.open()
    
    c.write_single_register(0, 0)
    c.close()
# c.write_single_register(0, 1)
# c.write_single_register(0, 0)
# c.write_single_register(0, 1)
# c.write_single_register(0, 0)
# c.write_single_register(0, 1)



# regs = c.read_holding_registers(0)
# if regs:
#     print(regs)
# else:
#     print("read error")

# regs = c.read_discrete_inputs(1)
# if regs:
#     print(regs)
# else:
#     print("read error")

# if c.write_single_register(0, 0):
#     print("write ok")
# else:
#     print("write error")
#
# c.close()

# if c.write_multiple_registers(10, [44,55]):
#     print("write ok")
# else:
#     print("write error")