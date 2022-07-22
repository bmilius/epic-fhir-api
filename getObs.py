#!/usr/bin/env python3
"""
getObs
Reads...
    - one or more files containing a list of Epic Patient FHIR IDs
    - tab delimited table of LOINC codes
For each patient, searches the Epic sandbox for any observations with any of the LOINC codes
"""
import json
import requests
import csv


def chunks(lst, n):
    """"Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def getAuthParams():
    """
    Reads a 'authparm.file containing Authorization and Epic-Client-ID parameters for header
    """
    with open('authparam.json', 'r') as infile:
        authparam = json.load(infile)

    authheaders = {'Authorization': authparam['Authorization'],
                   'Epic-Client-ID': authparam['Epic-Client-ID']
                   }
    return(authheaders)


def main():
    """
    """
    # fhirversion = "STU3"
    # fhirversion = "R4"
    fhirversion = "STU3"
    resource = "Observation"
    baseurl = 'https://apporchard.epic.com/interconnect-aocurprd-username/api/FHIR/'+fhirversion+'/'+resource+'?_format=json'   
    headers = getAuthParams()

    # patient FHIR IDs files from sheets in Epic spreadsheet, e.g., inpatient, oncology, surgery, etc
    # each group is a sheet in the Epic spreadsheet
    # file names are in the format "patients_[group].txt"
    # groups = {"transplant","inpatient","oncology","surgery","bmt"}
    # groups = {"inpatient_all"}
    groups = {"test2"}
    code_file = "priority_variables_fy22.txt"

    codelist = []
    with open(code_file,'r') as codefile:
        codes = csv.DictReader(codefile, delimiter='\t')
        for row in codes:
            codelist.append(row['Code'])
    
    # divide codelist into chunks of 140 because Epic doesn't allow more in search parameter
    codechunks = list(chunks(codelist, 140))

    for index, item in enumerate(codechunks):
        codestr = ",".join(item)
        for group in groups:
            print(group + " chunk " + str(index))
            # print(group, end='')
            patient_file = "patients_"+group+".txt"
            outfileprefix = "Observations_"+fhirversion+"/"+group+"_"+fhirversion+"_"+resource+"_"+str(index)+"_"
            with open(patient_file,'r') as infile:
                patients = infile.readlines()
            for patient in patients:
                patient = patient.strip()
                url = (baseurl + "&patient=" + patient 
                    # + "&category=laboratory" 
                    + "&code=http://loinc.org|" + codestr.strip() )
                response = requests.get(url=url, headers=headers)
                # print(response.status_code)
                if response.status_code == 200:
                    if json.loads(response.text)['total'] != 0:
                        fname = outfileprefix+patient+'.json'
                        with open(fname, 'w') as outfile:
                            json.dump(response.json(), outfile, indent=4)
                        # print(".", end='')
                else:
                    print(str(response.status_code) + " " + patient)
            print("")
    print("done")


if __name__ == '__main__':
    main()
