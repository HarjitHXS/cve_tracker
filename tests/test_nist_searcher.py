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
        nist_gitlab_entry = {'cve': {'id': 'CVE-2022-2185', 'sourceIdentifier': 'cve@gitlab.com', 'published': '2022-07-01T16:15:08.093', 'lastModified': '2022-07-19T20:15:11.193', 'vulnStatus': 'Undergoing Analysis', 'descriptions': [{'lang': 'en', 'value': 'A critical issue has been discovered in GitLab affecting all versions starting from 14.0 prior to 14.10.5.'}, {'lang': 'es', 'value': 'Se ha descubierto un problema crítico en GitLab que afecta a todas las versiones a partir de la 14.0 anterior a la 14.10.5, la 15.0 anterior a la 15.0.4 y la 15.1 anterior a la 15.1.1, en el que un usuario autenticado y autorizado a importar proyectos podría importar un proyecto malicioso que condujera a la ejecución remota de código'}], 'metrics': {'cvssMetricV31': [{'source': 'nvd@nist.gov', 'type': 'Primary', 'cvssData': {'version': '3.1', 'vectorString': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', 'attackVector': 'NETWORK', 'attackComplexity': 'LOW', 'privilegesRequired': 'NONE', 'userInteraction': 'NONE', 'scope': 'UNCHANGED', 'confidentialityImpact': 'HIGH', 'integrityImpact': 'HIGH', 'availabilityImpact': 'HIGH', 'baseScore': 9.8, 'baseSeverity': 'CRITICAL'}, 'exploitabilityScore': 3.9, 'impactScore': 5.9}, {'source': 'cve@gitlab.com', 'type': 'Secondary', 'cvssData': {'version': '3.1', 'vectorString': 'CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H', 'attackVector': 'NETWORK', 'attackComplexity': 'LOW', 'privilegesRequired': 'LOW', 'userInteraction': 'NONE', 'scope': 'CHANGED', 'confidentialityImpact': 'HIGH', 'integrityImpact': 'HIGH', 'availabilityImpact': 'HIGH', 'baseScore': 9.9, 'baseSeverity': 'CRITICAL'}, 'exploitabilityScore': 3.1, 'impactScore': 6.0}], 'cvssMetricV2': [{'source': 'nvd@nist.gov', 'type': 'Primary', 'cvssData': {'version': '2.0', 'vectorString': 'AV:N/AC:L/Au:N/C:P/I:P/A:P', 'accessVector': 'NETWORK', 'accessComplexity': 'LOW', 'authentication': 'NONE', 'confidentialityImpact': 'PARTIAL', 'integrityImpact': 'PARTIAL', 'availabilityImpact': 'PARTIAL', 'baseScore': 7.5, 'baseSeverity': 'HIGH'}, 'exploitabilityScore': 10.0, 'impactScore': 6.4, 'acInsufInfo': False, 'obtainAllPrivilege': False, 'obtainUserPrivilege': False, 'obtainOtherPrivilege': False, 'userInteractionRequired': False}]}, 'weaknesses': [{'source': 'nvd@nist.gov', 'type': 'Primary', 'description': [{'lang': 'en', 'value': 'CWE-732'}]}], 'configurations': [{'nodes': [{'operator': 'OR', 'negate': False, 'cpeMatch': [{'vulnerable': True, 'criteria': 'cpe:2.3:a:gitlab:gitlab:*:*:*:*:community:*:*:*', 'versionStartIncluding': '14.0.0', 'versionEndExcluding': '14.10.5', 'matchCriteriaId': 'D4B25A15-8656-43DE-B0DF-3493BB2F8FE8'}, {'vulnerable': True, 'criteria': 'cpe:2.3:a:gitlab:gitlab:*:*:*:*:enterprise:*:*:*', 'versionStartIncluding': '14.0.0', 'versionEndExcluding': '14.10.5', 'matchCriteriaId': '53A77E6E-918F-402B-8F8D-D3843794E45B'}, {'vulnerable': True, 'criteria': 'cpe:2.3:a:gitlab:gitlab:*:*:*:*:community:*:*:*', 'versionStartIncluding': '15.0.0', 'versionEndExcluding': '15.0.4', 'matchCriteriaId': '59BC7D90-71FE-4551-BC55-2CBDD7F037C3'}, {'vulnerable': True, 'criteria': 'cpe:2.3:a:gitlab:gitlab:*:*:*:*:enterprise:*:*:*', 'versionStartIncluding': '15.0.0', 'versionEndExcluding': '15.0.4', 'matchCriteriaId': '18F6B2F9-8BDA-41C7-8152-70D61CCCC0B8'}, {'vulnerable': True, 'criteria': 'cpe:2.3:a:gitlab:gitlab:15.1.0:*:*:*:community:*:*:*', 'matchCriteriaId': '0CE56232-8EF7-428C-90F2-85803A66B664'}, {'vulnerable': True, 'criteria': 'cpe:2.3:a:gitlab:gitlab:15.1.0:*:*:*:enterprise:*:*:*', 'matchCriteriaId': 'E07D39FA-8428-4585-9A4C-55D2A1799F9E'}]}]}], 'references': [{'url': 'https://gitlab.com/gitlab-org/cves/-/blob/master/2022/CVE-2022-2185.json', 'source': 'cve@gitlab.com', 'tags': ['Vendor Advisory']}, {'url': 'https://gitlab.com/gitlab-org/gitlab/-/issues/366088', 'source': 'cve@gitlab.com', 'tags': ['Broken Link']}, {'url': 'https://hackerone.com/reports/1609965', 'source': 'cve@gitlab.com', 'tags': ['Permissions Required', 'Third Party Advisory']}]}}

        source = 'Local Source Dependencies'
        module_name = 'gitlab'
        version_number = '14.9.2'

        test_entry_with_valid_resonse = NistCveSearcher()._make_cve_entry(source, module_name, version_number, nist_gitlab_entry)

        self.assertEqual(len(test_entry_with_valid_resonse), 9)
        self.assertEquals(test_entry_with_valid_resonse['MODULE_SOURCE'], 'Local Source Dependencies')
        self.assertEquals(test_entry_with_valid_resonse['ID'], 'CVE-2022-2185')
        self.assertEquals(test_entry_with_valid_resonse['ModuleName'], 'gitlab')
        self.assertEquals(test_entry_with_valid_resonse['Version'], '14.9.2')
        self.assertEquals(test_entry_with_valid_resonse['BaseScore'], '9.8')
        self.assertEquals(test_entry_with_valid_resonse['CVSSVector'], 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H')
        self.assertEquals(test_entry_with_valid_resonse['Description'],
                          'A critical issue has been discovered in GitLab affecting all versions starting from 14.0 prior to 14.10.5.')
        self.assertEquals(test_entry_with_valid_resonse['URL'], 'https://gitlab.com/gitlab-org/cves/-/blob/master/2022/CVE-2022-2185.json')


class RequestsErroredReturn():
    ok = False
    status_code = 500


if __name__ == '__main__':
    unittest.main()
