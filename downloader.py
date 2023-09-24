import requests
import pandas as pd
import re

TESTMODE = False
PAGESIZE = 200

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

def license_details(license: str):
	print(f'Getting license details for {license}.')
	url = 'https://selfservice.portlandmaine.gov/energov_prod/selfservice/api/energov/customfields/data'
	payload = {
		"EntityId": license,
		"ModuleId": 8,
		"LayoutId": "b589c49c-cc17-435d-b2d8-43a1e10e5b6d",
		"OnlineLayoutId": "e7d5dda1-27cb-4d0d-8128-58e979697587"
	}
	response_json = requests.post(url, headers=headers, json=payload).json()['Result']['CustomGroups'][0]['CustomFields']

	def get_label(data: dict):
		if data['Label'] != '':
			return data['Label']
		elif data['FieldName'] != '':
			return data['FieldName']
		elif data['Id'] != '':
			return str(data['Id'])
		return ''

	def get_value(licensedata: dict):
		if licensedata['CustomFieldTableRows'] != None:
			if licensedata['CustomFieldTableRows'] != []:
				unitsdata = {}
				for unit in licensedata['CustomFieldTableRows']:
					unitdata = {}
					for column in unit:
						if re.search("^Column", column):
							if unit[column]:
								unitdata[unit[column]['CustomField']] = unit[column]['Value']
					unitsdata[unit['Column0']['Value']] = unitdata
				return unitsdata
			return {}
		return licensedata['Value']

	rent_data = {}
	for licensedata in response_json:
		rent_data[get_label(licensedata)] = get_value(licensedata)
	return rent_data

def license_compiler():
	url = 'https://selfservice.portlandmaine.gov/energov_prod/selfservice/api/energov/search/search'
	def license_query(licensetype: str, page_num:int):
		payload = {
			"Keyword": "",
			"ExactMatch": True,
			"SearchModule": 10,
			"FilterModule": 1,
			"SearchMainAddress": False,
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
				"PageSize": 50,
				"SortBy": "relevance",
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
			"PageNumber": 0,
			"PageSize": 0,
			"SortBy": "relevance",
			"SortAscending": True,
		}
		return requests.post(url, headers=headers, json=payload).json()

	def license_query_page_count(licensetype: str):
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
				"IssueDateFrom": None,
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
				"PageNumber": 1,
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
			"PlanSortList": [
				{"Key": "relevance", "Value": "Relevance"},
				{"Key": "PlanNumber.keyword", "Value": "Plan Number"},
				{"Key": "ProjectName.keyword", "Value": "Project"},
				{"Key": "MainAddress", "Value": "Address"},
				{"Key": "ApplyDate", "Value": "Apply Date"},
			],
			"PermitSortList": [
				{"Key": "relevance", "Value": "Relevance"},
				{"Key": "PermitNumber.keyword", "Value": "Permit Number"},
				{"Key": "ProjectName.keyword", "Value": "Project"},
				{"Key": "MainAddress", "Value": "Address"},
				{"Key": "IssueDate", "Value": "Issued Date"},
				{"Key": "FinalDate", "Value": "Finalized Date"},
			],
			"InspectionSortList": [
				{"Key": "relevance", "Value": "Relevance"},
				{"Key": "InspectionNumber.keyword", "Value": "Inspection Number"},
				{"Key": "MainAddress", "Value": "Address"},
				{"Key": "ScheduledDate", "Value": "Schedule Date"},
				{"Key": "RequestDate", "Value": "Request Date"},
			],
			"CodeCaseSortList": [
				{"Key": "relevance", "Value": "Relevance"},
				{"Key": "CaseNumber.keyword", "Value": "Code Case Number"},
				{"Key": "ProjectName.keyword", "Value": "Project"},
				{"Key": "MainAddress", "Value": "Address"},
				{"Key": "OpenedDate", "Value": "Opened Date"},
				{"Key": "ClosedDate", "Value": "Closed Date"},
			],
			"RequestSortList": [
				{"Key": "relevance", "Value": "Relevance"},
				{"Key": "RequestNumber.keyword", "Value": "Request Number"},
				{"Key": "ProjectName.keyword", "Value": "Project Name"},
				{"Key": "MainAddress", "Value": "Address"},
				{"Key": "EnteredDate", "Value": "Date Entered"},
				{"Key": "CompleteDate", "Value": "Completion Date"},
			],
			"LicenseSortList": [
				{"Key": "relevance", "Value": "Relevance"},
				{"Key": "LicenseNumber.keyword", "Value": "License Number"},
				{"Key": "CompanyName.keyword", "Value": "Company Name"},
				{"Key": "AppliedDate", "Value": "Applied Date"},
				{"Key": "MainAddress", "Value": "Address"},
			],
			"ProjectSortList": [
				{"Key": "relevance", "Value": "Relevance"},
				{"Key": "ProjectNumber.keyword", "Value": "Project Number"},
				{"Key": "ProjectName.keyword", "Value": "Project Name"},
				{"Key": "StartDate", "Value": "Start Date"},
				{"Key": "CompleteDate", "Value": "Completed Date"},
				{"Key": "ExpectedEndDate", "Value": "Expected End Date"},
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
		response_json = requests.post(url, headers=headers, json=payload).json()
		foundpages = 0
		if 'Result' in response_json:
			if 'TotalPages' in response_json['Result']:
				foundpages = response_json['Result']['TotalPages']
		return foundpages

	licenses = []
	for licensetype in licensetypes:
		license_pages_total = 0
		license_pages_current = 1
		print(f'Processing {licensetype} licenses.')
		license_pages_total = license_query_page_count(licensetype)
		print(f'Found {license_pages_total} pages.')
		if license_pages_total > 0:
			if TESTMODE:
				license_pages_total = 1
			for n in range(license_pages_current, license_pages_total + 1):
				print(f'Retrieving page {license_pages_current} of {licensetype}.')
				licenses_found_json = license_query(licensetype, license_pages_current)
				if 'Result' in licenses_found_json:
					if 'EntityResults' in licenses_found_json['Result']:
						for license_found in licenses_found_json['Result']['EntityResults']:
							licenses.append(license_found)
				license_pages_current = license_pages_current + 1
		if TESTMODE:
			break
	df = pd.DataFrame.from_dict(licenses)
	return df

# Get all licenses
df = license_compiler()
# Add detail from individual license pages
df['businessLicense'] = df['CaseId'].apply(license_details)
# Write it to CSV
df.to_csv(r'./saved.csv', encoding='utf-8', index=False)
