# gitcommitlogger

A Python package that logs the details of a specific set of events made to a GitHub repository. Logs are saved into a `CSV` file and can optionally be sent in a request to a web app, such as a Google Apps Script attached to a Google Sheet where the data can be stored.

## GitHub Actions integration

This package is designed to be used in a GitHub Actions workflow, where the workflow is triggered by a push or pull request to the repository. Details of the commits included in the push will then be logged.

A sample GitHub Actions workflow is included in `.github/workflows/`[`event-logger.yml`](https://github.com/bloombar/gitcommitlogger/blob/main/.github/workflows/event-logger.yml). This example stores the logs into a Google Sheet by first posting them as `JSON` data to a web app attached to the Google Sheet. The URL of the web app is presumed be stored in a GitHub Actions Secret named `COMMIT_LOG_API`.

## Google Apps Scripts integration

In order to save the logs into a Google Sheet, the following steps are required:

- Create a Google Sheet.
- Attach an Apps Script to the sheet by clicking the `Extensions`->`Apps Scripts` menu option in Google Sheets.
- Copy/paste the example Apps Script in `apps-script-example`/[`code.js`](https://github.com/bloombar/gitcommitlogger/blob/main/apps-script-example/code.js) into the Apps Script editor and save. This sets up the script [as a web app](https://developers.google.com/apps-script/guides/web) so it can respond to `GET` or `POST` requests.
- Click the buton to `Deploy`->`New Deployment` in the Apps Scripts editor. Note the web app URL that is generated once deployed.
- Add the URL of the Apps Script web app to the GitHub repository [as a secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets) named `COMMIT_LOG_API`.
- The `gitcommitlogger` command in the example GitHub Action will send a `POST` request to the Google Sheet web app whenever a push or pull request is made on the repository.
- The web app will then add a row to the Google Sheet with the details of the commit, including the commit id, author, number of files changed in the commit, number of lines added and deleted.
