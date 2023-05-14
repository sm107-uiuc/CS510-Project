### Use pip install -r requirements.txt
### install all dependencies from the server folder.
### The folder chrome_extension contains the extension that we developed. To attach the chrome_extension, please follow the following URL - https://developer.chrome.com/docs/extensions/mv3/getstarted/development-basics/#:~:text=To%20load%20an%20unpacked%20extension,the%20bottom%20of%20the%20menu.
### Login to CDL (https://textdata.org/) and make any network call. Note down the auth_token and the origin.
In constants.py, change the auth_token and origin from your own browser's network call for the CDL.
### Use python server.py to run the server
### Once all this is done, goto any job description, select and right click on it. In the dropdown, select the menu item - 'Send the selected job description to textdata.org'. 
### Click on the extension from the chrome's extension tab. You should see the relevant links populated once the server sends a response.

