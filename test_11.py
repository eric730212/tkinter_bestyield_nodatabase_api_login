import json

text = json
text =" {""type"":""https://tools.ietf.org/html/rfc7231#section-6.5.1"",""title"":""One or more validation errors occurred."",""status"":400,""traceId"":""00-94c206c0b70a79ece83b717732844221-b7706e31cc33d4cf-00"",""errors"":{""file"":[""Minimum allowed file size is 400 KB.""]}}"
print(text.split("errors:{")[1].split("}")[0])
