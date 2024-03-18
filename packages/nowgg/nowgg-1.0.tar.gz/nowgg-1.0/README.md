# nowStudio App Upload - CLI

nowgg CLI is a command-line tool that enables you to upload your app builds to nowStudio.


##Prerequisites

+ App ID
    + Used to identify the App on nowStudio.
    + Your App ID can be found under the [App Details section](https://docs.now.gg/nowstudio/publish#app-details) of nowStudio.
+ Publisher token
    * Used to identify the publisher company.
    * Your Publisher token is available under the [Account Information](https://docs.now.gg/nowstudio/start-using-nowstudio#ac-info) section of nowStudio.

## Using nowgg CLI

Open any terminal on macOS or Windows.

Install nowgg CLI tool
```bash
  pip install nowgg
```
Initialize nowgg CLI
```bash
  nowgg init –token "<your_publisherToken_from_nowStudio>"
```
Upload App to nowStudio
```bash
  nowgg upload -app_id <your_app_id> -file_path "/directory/sample.apk" -apk_version <app_version_name> -version_code <app_version_code>

```

**Note**: Your app will be uploaded to the App Library within nowStudio.