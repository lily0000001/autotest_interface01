import json

result_interface = '{"status":201,"message":"APP被用户自己禁用，请在控制台解禁"}'
a= json.loads(result_interface)

print(a)