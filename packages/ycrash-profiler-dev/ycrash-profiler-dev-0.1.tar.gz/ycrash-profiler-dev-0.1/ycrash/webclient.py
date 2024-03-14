import requests

def upload_json_data(contentType, apiKey, url, data):
    # Set the Content-Type header to application/json
    headers = {'Content-Type': contentType,
               'Authorization': apiKey}
    print(f"\n*****************************************************************************************")
    print(f" \nHTTP post to  {url}  with headers {headers}")
    print(f" DATA: ")
    print(f" {data}")
    print(f"\n*****************************************************************************************")
    # Send the POST request with JSON data
    #response = requests.post(url, data=data, headers=headers)

    # Check if the request was successful
    #if response.status_code == 200:
    #  print('Data uploaded successfully!')
    #else:
    #  print('Error uploading data:', response.status_code)
