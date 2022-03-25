# iOS Trackers Detect
Easily detect which tracker libraries are used in a iOS app (`.ipa`).  
**iOS Trackers Detect** is a Python3 script that you can call to print (in your terminal) the list of third party tracker libraries shipped with the app.

## How to use
You need the IPA file of the app you want to check the tracker libraries.

 1. Clone or [download](https://github.com/octo-technology/ios-trackers-detect/archive/refs/heads/main.zip) the project.
 2. If you download the repo unzip it.
 3. With a terminal go inside this new folder (normally `cd ios-trackers-detect/` if you used `git clone`).
 4. And now you can run the Python script, like this:
 ```python
 python3 ipa_retrieve_dependencies.py --ipa_path ./YOUR_APPLICATION_NAME.ipa
 ```  
 **Info**: The `--ipa_path` argument can be relative `./` or `../`, or absolute `/` or `C:/`.
 
 5. If the program run without error(s) you now have the tracker list printed in your terminal, **enjoy**!

## How the script works
 1. Create a temp folder (`./temp`)
 2. Duplicate the ipa file you specified in the `--ipa_path` argument to this temp folder.
 3. Rename/change this ipa file extension from `.ipa` to `.zip`
 4. Unzip the archive.
 5. Go inside the un-archived subfolder `Frameworks/`.
 6. Filter the list of elements in that folder.
 7. Print the filtered list we created in the previous step.
