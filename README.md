| From / To     | Terra                    | Gen3                     | Dockstore                | Seven Bridges            | PIC-SURE                 | HeLx |
| ------------- |:------------------------:|:------------------------:|:------------------------:|:------------------------:|:------------------------:| ----:|
| Terra         | :heavy_multiplication_x: | :heavy_check_mark:       | :heavy_check_mark:       | :heavy_multiplication_x: | Future                   |      |
| Gen3          | TBD                      | :heavy_multiplication_x: | TBD?                     | TBD?                     |                          |      |
| Dockstore     |                          |                          | :heavy_multiplication_x: |                          |                          |      |
| Seven Bridges | :heavy_multiplication_x: | TBD?                     | TBD?                     | :heavy_multiplication_x: | Future                   |      |
| PIC-SURE      |                          | TBD?                     |                          |                          | :heavy_multiplication_x: |      |
| HeLx          | TBD?                     | TBD?                     |                          | TBD?                     |                          | :heavy_multiplication_x: |

 - :heavy_check_mark: : Implemented
 - :heavy_multiplication_x: : Not Applicable
 - TBD : To Be Done
 - Future : Tests will be needed, but the features have not been built yet


Current tests (all are run in each component's Staging environment):

API Test 1:
 - Create Terra workspace
 - Import static PFB from Gen3 into workspace
 - Check for success of PFB import into Terra workspace
 - Delete workspace

API Test 2:
 - Import from Dockstore workflow to Terra workspace
 - Check presence of Dockstore workflow in Terra workspace
 - Delete Dockstore workflow from terra workspace

API Test 3:
 - Run DRS URI in md5sum workflow in Terra
 - Check workflow run success

Test are here: https://github.com/DataBiosphere/bdcat-integration-tests/blob/master/test/test_basic_submission.py
