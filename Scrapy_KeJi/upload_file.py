import requests
from urllib3 import encode_multipart_formdata
from tenacity import *


def if_retry(result):  # 当返回True时重试
	return result['msg'] != 'success'


@retry(stop=stop_after_attempt(3), retry=retry_if_result(if_retry))
def send_file(img_url, file_name, headers, **kwargs):
	upload_url = 'http://175.24.172.64:5000/upload'
	res = requests.get(img_url, headers=headers)

	file = {
		"file": (file_name, res.content)
	}

	encode_data = encode_multipart_formdata(file)
	file_data = encode_data[0]
	headers_form_data = {
		"Content-Type": encode_data[1]
	}

	response = requests.post(url=upload_url, headers=headers_form_data, data=file_data)
	return response.json()


result = send_file('https://www.cscline.com/uploads/allimg/191028/1053331031-0.png', 'text', None)
print(result)
