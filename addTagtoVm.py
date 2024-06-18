from typing import Any
import requests, csv, locale, urllib3, json

# Set the locale for the application
locale.setlocale(locale.LC_ALL, '')
# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# define vars for API
host="XX.XX.XX.XXX" 
token="xxxxxxxxxxxxxxxxxxxxxxxxxxx"
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

# Function to add a tag to a Morpheus instance
def addTagtoVm(row: Any):
    # Initialize an empty list for tags
    atags =[]
    # Get the instance ID and list of tags from the row
    afunct = getInstancesIdByName(row[0])
    atags =afunct['tags']
    instanceid = afunct['id']
    url = f"https://{host}/api/instances/%s" % (instanceid)
    
    nextListId = str(len(atags) + 1)
    #Add a new tag to the existing list of metadata.
    newTag = {
        "name": "PIVA",
        "value": "%s" % row[1],
        "strict": False,
        "listId": nextListId, # the id would be the next in the list.
        "strictValue": ""
    }
    existPiva =0
    for x in range(0, len(atags)): 
        if atags[x]['name'] == 'PIVA':
            atags[x]['value'] = "%s" % row[1]
            existPiva =1
    if(existPiva==0):
        atags.append(newTag)
    
    payload = {"metadata": atags}
    body=json.dumps(payload)
    r = requests.put(url, headers=headers, data=body, verify=False)


# Function to get a server ID by name
def getInstancesIdByName(strName: Any):
    
    print("Get a id of server by Name")
    url=f"https://{host}/api/instances?name={strName}&vm=true&max=100" 
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    tagList = []
    for a in data['instances']:
        return a
        
#
# Main Method
#
with open('listvm.csv', newline='') as csvfile:
    # Create a CSV reader with a semicolon delimiter
    csvreader = csv.reader(csvfile, delimiter=';')
    i=0
    for row in csvreader:
        if i!=0:
            addTagtoVm(row)
        i=i+1
