import requests
import json

url = "https://google.serper.dev/search"

payload = json.dumps({
  "q": "张学友演唱会门票是多少",
  "gl": "cn",
  "hl": "zh-cn"
})
headers = {
  'X-API-KEY': 'b0853795d4b9c4a282d639c31919d72d53943a66',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

import json
context = json.loads(response.text)
print(context)

