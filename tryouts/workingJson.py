import json

feed_data = {
	"event": [{
		"id": 1111,
		"source": "The Source",
		"param_name": "param_name",
		"param_value": "param_value"
	}, {
		"id": 2222,
		"source": "The Source",
		"param_name": "param_name",
		"param_value": "param_value"
	}]
}


feed_data2 = {
	"event": []
}

feed_data2['event'].append({
		"id": 33333,
		"source": "The Source",
		"param_name": "param_name",
		"param_value": "param_value"
	})

print(feed_data2['event'][0])

js = json.dumps(feed_data2)
print(js)