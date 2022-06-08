from typing import Container
import unittest
from unittest.mock import patch
from src.cve_tracker import NistCveSearcher


class TestNistSearcher(unittest.TestCase):

    @patch('requests.get')
    def test_nist_api_returns_error(self, mock_get_call):
        mock_get_call.return_value = RequestsErroredReturn()

        cves = NistCveSearcher()._query_nvd_for_module_cves('fake_module', 'token')

        self.assertIsInstance(cves, Container)
        self.assertFalse(cves)

    def test_version_start_end_check(self):
        matched_version_number = ' 7.11.3'
        unmatched_version_number = '7.10.0'
        cpe_uri = {'vulnerable': True, 'cpe23Uri': 'cpe:2.3:a:jfrog:artifactory:*:*:*:*:enterprise\\+:*:*:*',
                   'versionStartIncluding': '7.11.0', 'versionEndExcluding': '7.11.8', 'cpe_name': []}

        test_with_matching_version_number = NistCveSearcher._version_start_end_check(matched_version_number, cpe_uri)
        test_with_unmatching_version_number = NistCveSearcher._version_start_end_check(unmatched_version_number, cpe_uri)

        self.assertTrue(test_with_matching_version_number)
        self.assertFalse(test_with_unmatching_version_number)

    def test_make_cve_entry(self):
        nist_cereal_entry = {'cve': {'data_type': 'CVE', 'data_format': 'MITRE', 'data_version': '4.0', 'CVE_data_meta':
            {'ID': 'CVE-2020-11104', 'ASSIGNER': 'cve@mitre.org'}, 'problemtype':
            {'problemtype_data': [{'description': [{'lang': 'en', 'value': 'CWE-908'}]}]},
                                'references': {'reference_data': [
                                    {'url': 'https://github.com/USCiLab/cereal/issues/625',
                                     'name': 'https://github.com/USCiLab/cereal/issues/625',
                                     'refsource': 'MISC', 'tags': ['Exploit', 'Third Party Advisory']}]},
                                'description': {'description_data': [
                                    {'lang': 'en',
                                     'value': 'An issue was discovered in USC iLab cereal through 1.3.0.'}]}},
                        'configurations': {'CVE_data_version': '4.0', 'nodes': [{'operator': 'OR', 'children': [],
                                                                                 'cpe_match': [{'vulnerable': True,
                                                                                                'cpe23Uri': 'cpe:2.3:a:usc:cereal:*:*:*:*:*:*:*:*',
                                                                                                'versionEndIncluding': '1.3.0',
                                                                                                'cpe_name': []}]}]},
                        'impact': {'baseMetricV3': {
                            'cvssV3': {'version': '3.1', 'vectorString': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N',
                                       'attackVector': 'NETWORK', 'attackComplexity': 'LOW',
                                       'privilegesRequired': 'NONE',
                                       'userInteraction': 'NONE', 'scope': 'UNCHANGED', 'confidentialityImpact': 'LOW',
                                       'integrityImpact': 'NONE', 'availabilityImpact': 'NONE', 'baseScore': 5.3,
                                       'baseSeverity': 'MEDIUM'}, 'exploitabilityScore': 3.9, 'impactScore': 1.4},
                            'baseMetricV2': {
                                'cvssV2': {'version': '2.0', 'vectorString': 'AV:N/AC:L/Au:N/C:P/I:N/A:N',
                                           'accessVector': 'NETWORK', 'accessComplexity': 'LOW',
                                           'authentication': 'NONE', 'confidentialityImpact': 'PARTIAL',
                                           'integrityImpact': 'NONE', 'availabilityImpact': 'NONE',
                                           'baseScore': 5.0}, 'severity': 'MEDIUM', 'exploitabilityScore': 10.0,
                                'impactScore': 2.9, 'acInsufInfo': False, 'obtainAllPrivilege': False,
                                'obtainUserPrivilege': False, 'obtainOtherPrivilege': False,
                                'userInteractionRequired': False}}, 'publishedDate': '2020-03-30T22:15Z',
                        'lastModifiedDate': '2021-07-21T11:39Z'}
        source = 'bazel'
        module_name = 'cereal'
        version_number = '1.3.0'

        test_entry_with_valid_resonse = NistCveSearcher()._make_cve_entry(source, module_name, version_number, nist_cereal_entry)

        self.assertEqual(len(test_entry_with_valid_resonse), 9)
        self.assertEquals(test_entry_with_valid_resonse['MODULE_SOURCE'], 'bazel')
        self.assertEquals(test_entry_with_valid_resonse['ID'], 'CVE-2020-11104')
        self.assertEquals(test_entry_with_valid_resonse['ModuleName'], 'cereal')
        self.assertEquals(test_entry_with_valid_resonse['Version'], '1.3.0')
        self.assertEquals(test_entry_with_valid_resonse['BaseScore'], '5.3')
        self.assertEquals(test_entry_with_valid_resonse['CVSSVector'], 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N')
        self.assertEquals(test_entry_with_valid_resonse['Description'],
                          'An issue was discovered in USC iLab cereal through 1.3.0.')
        self.assertEquals(test_entry_with_valid_resonse['URL'], 'https://github.com/USCiLab/cereal/issues/625')


class RequestsErroredReturn():
    ok = False
    status_code = 500


if __name__ == '__main__':
    unittest.main()
