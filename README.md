The following instructions outline how to use our software for text analysis and data extraction. Please follow these steps:

Install Dependencies:

Open your terminal or command prompt.
Navigate to the project folder.
Run the command pip install -r requirements.txt to install all the required dependencies.
Server Setup:

Go to the server folder and install the dependencies specific to the server component.
bash
Copy code
cd server
pip install -r requirements.txt
Chrome Extension:

The chrome_extension folder contains the developed extension.
To attach the Chrome extension, follow the instructions in the following URL:
https://developer.chrome.com/docs/extensions/mv3/getstarted/development-basics/#:~:text=To%20load%20an%20unpacked%20extension,the%20bottom%20of%20the%20menu.
Login to CDL:

Open your web browser and navigate to https://textdata.org/.
Log in to the CDL (Connected Data Lab) platform.
Make any network call within the CDL platform.
Note down the auth_token and the origin from the network call.
Update Constants:

Open the constants.py file in the project.
Replace the auth_token and origin variables with the values obtained from your browser's network call to the CDL platform.
Run the Server:

In your terminal or command prompt, go back to the project's root directory.
Run the command python server.py to start the server.
Extract Text Data:

Once all the previous steps are completed, open any job description webpage.
Select and right-click on the job description text to be analyzed.
From the dropdown menu, select the option "Send the selected job description to textdata.org."
Go to the Chrome extension tab and click on our extension.
The relevant links will be populated in the extension's interface once the server sends a response.
