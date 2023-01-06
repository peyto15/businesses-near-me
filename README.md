# businesses-near-me
Find up to 60 businesses near you!

This is a locally run Python tool that uses Google's Place & Address Validation APIs to find up to 60 businesses of a specific type (cafe, gas station, dentist, etc.) within a radius of 30 miles or less of a specific address. The limitations mentioned here come from the limitations of the APIs themselves, and that's probably a good thing considering how high of a bill these APIs can run someone.

You will need your own Google API key for this tool, and that requires a billing account set up in Google Cloud Platform. HOWEVER, you will get $200 in free credits per month. That should cover you for many runs of this tool. Further, when you set up a billing account it automatically sets up budget alerts for you. Read more about getting your own API key here: https://developers.google.com/maps/documentation/places/web-service/cloud-setup. You will only need to follow the "Enable Billing" and "Enable APIs" sections. All you will need from this is your API key itself. 

The output for this tool will be in the form of an Excel file named output.xslx in the folder that the executable is run from.

FUTURE IMPROVEMENTS
 - Build a better GUI with a more interactive dropdown and flexible pop up box
 - Build tool into GH Actions and host a clean interactive front end on GH pages
