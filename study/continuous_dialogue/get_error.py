error_message = "Error code:429 - {'error':{'message':'max request per minute reached:3,please try again after 1 seconds','type':'rate_limit_reached_error'}}"

# 从字符串中提取出字典信息
start_index = error_message.index('{')
end_index = error_message.rindex('}') + 1
error_dict_str = error_message[start_index:end_index]
print(start_index)
print(end_index)
# 将字典字符串转换为字典对象
error_dict = eval(error_dict_str)

# 提取错误消息和错误类型信息
error_message = error_dict['error']['message']
error_type = error_dict['error']['type']

# 输出对应的参数
print("Error message:",error_message)
print("Error type:",error_type)