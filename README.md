# businesses-near-me
Find up to 60 businesses near you!

## What is this?
This is a Python tool run in GitHub Actions that uses Google's Place & Address Validation APIs to find up to 60 businesses of a specific type (cafe, gas station, dentist, etc.) within a radius of 30 miles or less of a specific address. The limitations mentioned here come from the limitations of the APIs themselves, and that's probably a good thing considering how high of a bill these APIs can run someone.

## How do I set this up for myself? (5 - 10 minutes)
### Get your Google API key
You will need your own Google API key for this tool, and that requires a billing account set up in Google Cloud Platform. HOWEVER, you get $200 in free credits per month. That should cover you for many runs of this tool. Further, when you set up a billing account it automatically sets up budget alerts for you. Read more about getting your own API key here: https://developers.google.com/maps/documentation/places/web-service/cloud-setup. You will only need to follow the "Enable Billing" and "Enable APIs" sections. All you will need from this is your API key itself. 
### Fork this repository 
Once you fork the repository, head over to the Actions tab. You will see a warning like this: <br /><br />
_"Because this repository contained workflow files when it was forked, we have disabled them from running on this fork. Make sure you understand the configured workflows and their expected usage before enabling Actions on this repository."_ <br /><br />
From there, press the green button that says _"I understand my workflows, go ahead and enable them."_
### Put your Google API key in the forked repository secrets
Go to the Settings tab for your forked repository. Once in Settings, scan the left menu and click on the downward facing carrot to the right of Secrets. Click on Actions. Once in Actions, click the green button in the top right corner that says _"New repository secret."_ Set the Name as **GOOGLE_API_KEY** and enter the Google API key in the body text below label Secret. Click the _"Add secret"_ button. 

## Finally, how do I run the tool?
Now that you're all set, go to the Actions tab and select the _"Run Script"_ option from the left menu.  
### Inputs
 - Business Type: A complete list of valid entries can be found here: https://developers.google.com/maps/documentation/places/web-service/supported_types. <br />
 - Address for Center of Radius: Street address and postal code 
 - Radius: How many miles to search from the address entered above

## Outputs
Once the workflow has run successfully, click on the _Summary_ option in the left menu of the run. You will see a bussinesses-output in the _Artifacts_ section towards the bottom of the page. That is your CSV file with up to 60 businesses near you. Hope you enjoy my little side project! 

## Future Updates/Development
 - Make business type input a dropdown menu with set values to avoid user error. This is important because the type is part of the API call and entering an invalid one will cause the tool to fail. 
 - Put this tool on GitHub Pages or GitHub Apps for ease of use. I'm thinking of a button that the user presses that kicks off a workflow that logs the user into GitHub. Once user is authenticated, workflow forks the repo and stores the Google API key as a secret in their forked repo. From there, the page would just ask for the 3 inputs mentioned above.    
