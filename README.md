# FieldMuseumImageToTextAndCsv
A Python Script To Take A folder of images and turn them into a text file and categorize into a csv file.

Setup:
Necessary imports include the openai Api, Pandas and Tesseract. You will also need a compiler for python. Visual Studio code and the python extension is what I used. 

Importing Pandas
```
pip install pandas
```
Installing OpenAi Api
```
pip install openai 
```
Installing Tesseract for Image Extraction
```
pip install openai pytesseract Pillow
```

What youll need to do when you opent the program:
Go in and change the following lines:
- Line 16: Change your API Key
- Line 103: Change to filepath of Images in ONE folder
- Line 107: Change To Path and Filename you want the text output to be. 
  EX: C:\\Users\\riley\\OneDrive\\Desktop\\Pictures (Make sure you have double // between each path)

- Line 136: This is your input for the csv file. Make it so it is the same as the output of the text file (look to Line 107 what you have)
- Line 138: Finally, this is your output for your csv (spreadsheet). Name it whatever you like and locate it wherever
