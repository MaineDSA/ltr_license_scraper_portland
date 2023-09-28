from re import search
from requests import Session
import pandas as pd

TESTMODE = False
PAGESIZE = 200
if TESTMODE: # Faster to test with 20
	PAGESIZE = 20

licensetypes = {
	'Multi Family': 'ddf09feb-ce7d-4437-839d-33296fd1c849_c7f4be57-4935-461c-bcf1-8d89c7973b81',
	'Single Family': 'ddf09feb-ce7d-4437-839d-33296fd1c849_5c7dadf7-db4e-4d4d-a1fa-c109dbf3c0c5',
	'Two Family': 'ddf09feb-ce7d-4437-839d-33296fd1c849_0b3794bb-b86f-467c-b6c0-6d473a8c6966',
}
headers = {
	'tenantId': '1',
	'tenantName': 'EnerGovProd',
	'Referer': 'https://selfservice.portlandmaine.gov/energov_prod/selfservice',
	'DNT': '1',
}
license_url = 'https://selfservice.portlandmaine.gov/energov_prod/selfservice/api/energov/customfields/data'
query_url = 'https://selfservice.portlandmaine.gov/energov_prod/selfservice/api/energov/search/search'

def license_details(license: str):

	def get_label(data: dict):
		return data['Label'] or data['FieldName'] or data['CustomField'] or str(data['Id']) or ''

	def get_value(licensedata: dict):
		if licensedata['CustomFieldTableRows'] is None:
			return licensedata['Value']
		elif licensedata['CustomFieldTableRows'] == []:
			return {}

		return {
			unit['Column0']['Value']: {
				get_label(unit[column]): unit[column]['Value']
				for column in unit
				if column.startswith("Column") and unit[column]
			}
			for unit in licensedata['CustomFieldTableRows']
		}

	payload = {
		"EntityId": license,
		"ModuleId": 8,
		"LayoutId": "b589c49c-cc17-435d-b2d8-43a1e10e5b6d",
		"OnlineLayoutId": "e7d5dda1-27cb-4d0d-8128-58e979697587"
	}

	print(f'Getting license details for {license}.')
	response_json = s.post(license_url, headers=headers, json=payload).json()['Result']['CustomGroups'][0]['CustomFields']
	return {get_label(licensedata): get_value(licensedata) for licensedata in response_json}

def license_compiler():

	def license_query(licensetype: str, page_num:int):
		payload = {
			"Keyword": "",
			"ExactMatch": True,
			"SearchModule": 10,
			"FilterModule": 1,
			"SearchMainAddress": False,
			"PlanCriteria": {
				"PlanNumber": None,
				"PlanTypeId": None,
				"PlanWorkclassId": None,
				"PlanStatusId": None,
				"ProjectName": None,
				"ApplyDateFrom": None,
				"ApplyDateTo": None,
				"ExpireDateFrom": None,
				"ExpireDateTo": None,
				"CompleteDateFrom": None,
				"CompleteDateTo": None,
				"Address": None,
				"Description": None,
				"SearchMainAddress": False,
				"ContactId": None,
				"ParcelNumber": None,
				"TypeId": None,
				"WorkClassIds": None,
				"ExcludeCases": None,
				"EnableDescriptionSearch": False,
				"PageNumber": 0,
				"PageSize": 0,
				"SortBy": None,
				"SortAscending": False,
			},
			"PermitCriteria": {
				"PermitNumber": None,
				"PermitTypeId": None,
				"PermitWorkclassId": None,
				"PermitStatusId": None,
				"ProjectName": None,
				"IssueDateFrom": None,
				"IssueDateTo": None,
				"Address": None,
				"Description": None,
				"ExpireDateFrom": None,
				"ExpireDateTo": None,
				"FinalDateFrom": None,
				"FinalDateTo": None,
				"ApplyDateFrom": None,
				"ApplyDateTo": None,
				"SearchMainAddress": False,
				"ContactId": None,
				"TypeId": None,
				"WorkClassIds": None,
				"ParcelNumber": None,
				"ExcludeCases": None,
				"EnableDescriptionSearch": False,
				"PageNumber": 0,
				"PageSize": 0,
				"SortBy": None,
				"SortAscending": False,
			},
			"InspectionCriteria": {
				"Keyword": None,
				"ExactMatch": False,
				"Complete": None,
				"InspectionNumber": None,
				"InspectionTypeId": None,
				"InspectionStatusId": None,
				"RequestDateFrom": None,
				"RequestDateTo": None,
				"ScheduleDateFrom": None,
				"ScheduleDateTo": None,
				"Address": None,
				"SearchMainAddress": False,
				"ContactId": None,
				"TypeId": [],
				"WorkClassIds": [],
				"ParcelNumber": None,
				"DisplayCodeInspections": False,
				"ExcludeCases": [],
				"ExcludeFilterModules": [],
				"HiddenInspectionTypeIDs": None,
				"PageNumber": 0,
				"PageSize": 0,
				"SortBy": None,
				"SortAscending": False,
			},
			"CodeCaseCriteria": {
				"CodeCaseNumber": None,
				"CodeCaseTypeId": None,
				"CodeCaseStatusId": None,
				"ProjectName": None,
				"OpenedDateFrom": None,
				"OpenedDateTo": None,
				"ClosedDateFrom": None,
				"ClosedDateTo": None,
				"Address": None,
				"ParcelNumber": None,
				"Description": None,
				"SearchMainAddress": False,
				"RequestId": None,
				"ExcludeCases": None,
				"ContactId": None,
				"EnableDescriptionSearch": False,
				"PageNumber": 0,
				"PageSize": 0,
				"SortBy": None,
				"SortAscending": False,
			},
			"RequestCriteria": {
				"RequestNumber": None,
				"RequestTypeId": None,
				"RequestStatusId": None,
				"ProjectName": None,
				"EnteredDateFrom": None,
				"EnteredDateTo": None,
				"DeadlineDateFrom": None,
				"DeadlineDateTo": None,
				"CompleteDateFrom": None,
				"CompleteDateTo": None,
				"Address": None,
				"ParcelNumber": None,
				"SearchMainAddress": False,
				"PageNumber": 0,
				"PageSize": 0,
				"SortBy": None,
				"SortAscending": False,
			},
			"BusinessLicenseCriteria": {
				"LicenseNumber": None,
				"LicenseTypeId": None,
				"LicenseClassId": None,
				"LicenseStatusId": None,
				"BusinessStatusId": None,
				"LicenseYear": None,
				"ApplicationDateFrom": None,
				"ApplicationDateTo": None,
				"IssueDateFrom": None,
				"IssueDateTo": None,
				"ExpirationDateFrom": None,
				"ExpirationDateTo": None,
				"SearchMainAddress": False,
				"CompanyTypeId": None,
				"CompanyName": None,
				"BusinessTypeId": None,
				"Description": None,
				"CompanyOpenedDateFrom": None,
				"CompanyOpenedDateTo": None,
				"CompanyClosedDateFrom": None,
				"CompanyClosedDateTo": None,
				"LastAuditDateFrom": None,
				"LastAuditDateTo": None,
				"ParcelNumber": None,
				"Address": None,
				"TaxID": None,
				"DBA": None,
				"ExcludeCases": None,
				"TypeId": None,
				"WorkClassIds": None,
				"ContactId": None,
				"PageNumber": 0,
				"PageSize": 0,
				"SortBy": None,
				"SortAscending": False,
			},
			"ProfessionalLicenseCriteria": {
				"LicenseNumber": None,
				"HolderFirstName": None,
				"HolderMiddleName": None,
				"HolderLastName": None,
				"HolderCompanyName": None,
				"LicenseTypeId": None,
				"LicenseClassId": None,
				"LicenseStatusId": None,
				"IssueDateFrom": None,
				"IssueDateTo": None,
				"ExpirationDateFrom": None,
				"ExpirationDateTo": None,
				"ApplicationDateFrom": None,
				"ApplicationDateTo": None,
				"Address": None,
				"MainParcel": None,
				"SearchMainAddress": False,
				"ExcludeCases": None,
				"TypeId": None,
				"WorkClassIds": None,
				"ContactId": None,
				"PageNumber": 0,
				"PageSize": 0,
				"SortBy": None,
				"SortAscending": False,
			},
			"LicenseCriteria": {
				"LicenseNumber": None,
				"LicenseTypeId": licensetypes[licensetype],
				"LicenseClassId": "none",
				"LicenseStatusId": "none",
				"BusinessStatusId": "none",
				"ApplicationDateFrom": None,
				"ApplicationDateTo": None,
				"IssueDateFrom": '2022-01-01T05:00:00.000Z',
				"IssueDateTo": None,
				"ExpirationDateFrom": None,
				"ExpirationDateTo": None,
				"SearchMainAddress": False,
				"CompanyTypeId": "none",
				"CompanyName": None,
				"BusinessTypeId": "none",
				"Description": None,
				"CompanyOpenedDateFrom": None,
				"CompanyOpenedDateTo": None,
				"CompanyClosedDateFrom": None,
				"CompanyClosedDateTo": None,
				"LastAuditDateFrom": None,
				"LastAuditDateTo": None,
				"ParcelNumber": None,
				"Address": None,
				"TaxID": None,
				"DBA": None,
				"ExcludeCases": None,
				"TypeId": None,
				"WorkClassIds": None,
				"ContactId": None,
				"HolderFirstName": None,
				"HolderMiddleName": None,
				"HolderLastName": None,
				"MainParcel": None,
				"EnableDescriptionSearchForBLicense": False,
				"EnableDescriptionSearchForPLicense": False,
				"PageNumber": page_num,
				"PageSize": PAGESIZE,
				"SortBy": "relevance",
				"SortAscending": False,
			},
			"ProjectCriteria": {
				"ProjectNumber": None,
				"ProjectName": None,
				"Address": None,
				"ParcelNumber": None,
				"StartDateFrom": None,
				"StartDateTo": None,
				"ExpectedEndDateFrom": None,
				"ExpectedEndDateTo": None,
				"CompleteDateFrom": None,
				"CompleteDateTo": None,
				"Description": None,
				"SearchMainAddress": False,
				"ContactId": None,
				"TypeId": None,
				"ExcludeCases": None,
				"EnableDescriptionSearch": False,
				"PageNumber": 0,
				"PageSize": 0,
				"SortBy": None,
				"SortAscending": False,
			},
			"LicenseSortList": [
				{"Key": "relevance", "Value": "Relevance"},
				{"Key": "LicenseNumber.keyword", "Value": "License Number"},
				{"Key": "CompanyName.keyword", "Value": "Company Name"},
				{"Key": "AppliedDate", "Value": "Applied Date"},
				{"Key": "MainAddress", "Value": "Address"},
			],
			"ExcludeCases": None,
			"SortOrderList": [
				{"Key": True, "Value": "Ascending"},
				{"Key": False, "Value": "Descending"},
			],
			"HiddenInspectionTypeIDs": None,
			"PageNumber": 0,
			"PageSize": 0,
			"SortBy": "relevance",
			"SortAscending": True,
		}
		response = s.post(query_url, headers=headers, json=payload).json()
		licenses = response.get('Result', {}).get('EntityResults', [])
		foundpages = response.get('Result', {}).get('TotalPages', 0)
		return foundpages, licenses

	licenses = []
	for licensetype in licensetypes:
		license_pages_total, licenses_found = license_query(licensetype, 1)
		print(f'Retrieved page 1 of {license_pages_total} pages of {licensetype}.')
		licenses.extend(licenses_found)
		if TESTMODE: # 1 page is enough when testing
			break
		for n in range(2, license_pages_total + 1):
			license_pages_total, licenses_found = license_query(licensetype, n)
			print(f'Retrieved page {n} of {license_pages_total} pages of {licensetype}.')
			licenses.extend(licenses_found)
	return pd.DataFrame(data=licenses)

# Get all licenses
with Session() as s:
	df = license_compiler()
	# Add detail from individual license pages
	df['businessLicense'] = df['CaseId'].apply(license_details)
	# Write it to CSV
	df.to_csv(r'./saved.csv', encoding='utf-8', index=False)