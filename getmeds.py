"""
getmeds.py
"""
import uuid
import json
import requests


def getmeds(smart):
    '''
    takes an patient ID and returns bundle of medicationrequests
    '''
    url = ('https://apporchard.epic.com/interconnect-aocurprd-username/api/FHIR/R4/MedicationRequest?patient=e.Rxkbv0HmfyDyboA-LtyRQ3')
    headers = {""}
    try:
        response = requests.get(url=url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    # create a temp file to hold the sequence record
    # f = NamedTemporaryFile(mode='w+', delete=False)
    # f.write(response.text)
    # f.close()
    print(json.dumps(bundle.as_json(), indent=4))
    


def main():
    """
    some tests
    """
    getmeds()


if __name__ == '__main__':
    main()