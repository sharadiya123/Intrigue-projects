import pandas as pd    
import datetime    #for working with dates
import smtplib		 #smtp library is used for sending the e-mail
import os    #for interacting with the operating system

curr_path = os.getcwd()    #fetches current working directory to ensure that the program is working in the expected directory, because we will be reading and writing files. 
print(curr_path)

os.chdir(curr_path)    # Change the directory to which we are currently working in 

MAIL_ID = input("Enter your email: ")
MAIL_PSWD = input("Enter your email password: ")


def sendEmail(to, sub, msg):
    print(f"HBD Email to {to} sent via Gmail! \nSubject: {sub} ,\nMessage: {msg}")    #the 'f'-string (formatted string literal) allows you to insert expressions inside curly braces, that will be replaced with their values at runtime.
    #creating the smtp server to send mail
    s = smtplib.SMTP('smtp.gmail.com', 587) #specifies smtp server address and port no. for gmail
  
    #starting a TLS session  #TLS (Transport Layer Security) is a protocol that ensures privacy between communicating applications and users on the Internet. 
    #TLS is used here for encryption and security during the email communication.
  
    s.starttls()
    #the function will login with your e-mail credentials
    s.login(MAIL_ID, MAIL_PSWD)
    #sending the mail
    s.sendmail(MAIL_ID, to, f"Subject: {sub} \n\n {msg}")
    s.quit() #closing the smtp server


if __name__ == "__main__":
    df = pd.read_excel("data.xlsx")    #in data.xlsx, the data of all the user's friends' Name, Birthday, Email and LastWishedYear is stored
    today = datetime.datetime.now().strftime("%d-%m")  #only today's date and month is stored
    yearNow = datetime.datetime.now().strftime("%Y")

    writeInd = []    #to store indices of friends already wished, currently no one has been wished yet
    for index, item in df.iterrows():   #iterated through different friends (stored in different rows of the dataframe)
        bday = item['Birthday']   #item is a series storing just one row of the dataframe df at a time
        bday = datetime.datetime.strptime(bday, "%d-%m-%Y")   #We are using strptime to parse the **birthday string** from the DataFrame (item['Birthday']) into a **datetime object** using the format "%d-%m-%Y".
        bday = bday.strftime("%d-%m")  #Here, bday is a datetime object that was obtained earlier using strptime. The strftime method is used to format this datetime object as a string according to the %d-%m format
      #now bday only stores dd-mm format so it becomes easier for us to compare today and bday variables as they both have the same dd-mm format now.


#NOTE: LastWishedYear Column has values of type LIST. So it contains a list of years where that friend has been wished HBD
      
        if (today == bday) and yearNow not in str(item['LastWishedYear']):  #if today matches with the current friend's birthday (date and month) AND the year where we last wished them was NOT this year, we go ahead and wish this person
            #we send the mail to wish HBD
            sendEmail(item['Email'], "Happy Birthday", item['Dialogue'])
            writeInd.append(index)   #storing CURRENTLY WISHED friend's index to this list.

    if writeInd != None:  #meaning we HAVE wished some people so far with this application
        for i in writeInd:  #updating the LastWishedYear in each friend's case
            temp = df.loc[i, 'LastWishedYear']  #storing all the last wished year list values in temp
            df.loc[i, 'LastWishedYear'] = str(temp) + ", " + str(yearNow)   #concatenating the old LastWishYear values with the current year as we wished this index i friend in the current year

    df.to_excel('data.xlsx', index=False)  #now we write the newly updated contents of the DataFrame df BACK to the original Excel data file 'data.xlsx'.
