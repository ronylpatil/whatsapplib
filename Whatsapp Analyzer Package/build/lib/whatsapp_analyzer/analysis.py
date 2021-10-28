import re
from datetime import datetime
import pandas as pd

class Preprocess :
    URLPATTERN = r'(https?://\S+)'
    MEDIAPATTERN = r'<Media omitted>'

    def __init__(self) :
        pass

    # extract date-time pattern from chat
    def _startsWithDateAndTime(s):
        # regex pattern for date.
        # pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9][0-9]), ([0-9]+):([0-9][0-9]) (AM|PM) -'
        pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9][0-9]), ([0-9]+):([0-9][0-9]) (am|pm) - '

        result = re.match(pattern, s)
        if result:
            return result
        return False

    # regex pattern to extract user name from chat
    def _FindAuthor(s):
        patterns = [
            '([\w]+):',  # First Name
            '([\w]+[\s]+[\w]+):',  # First Name + Last Name
            '([\w]+[\s]+[\w]+[\s]+[\w]+):',  # First Name + Middle Name + Last Name
            '([+]\d{2} \d{5} \d{5}):',  # Mobile Number (India no.)
            '([+]\d{2} \d{3} \d{3} \d{4}):',  # Mobile Number (US no.)
            '([\w]+)[\u263a-\U0001f999]+:',  # Name and Emoji
        ]
        pattern = '^' + '|'.join(patterns)
        result = re.match(pattern, s)
        if result:
            return result
        return False

    # regrex pattern extract date, time, author & message
    def _getDataPoint(line) :
        splitLine = line.split(' - ')
        dateTime = splitLine[0]
        date, time = dateTime.split(', ')
        message = ' '.join(splitLine[1:])
        if Preprocess._FindAuthor(message):
            splitMessage = message.split(': ')
            author = splitMessage[0]
            message = ' '.join(splitMessage[1:])
        else:
            author = None
        return date, time, author, message

    # it will use all above methods and preprocess the data and at the end return dataframe
    def _processing(file_path, save_data, name = 'whatsapp_dataset.csv') :
        parsedData = []  # List to keep track of data so it can be used by a Pandas dataframe
        # Uploading exported chat file
        # conversationPath = r'E:\DHL Project\WhatsApp Group Chat Lib\Samp.txt' # chat file
        conversationPath = file_path
        with open(conversationPath, encoding="utf-8") as fp :
            # Skipping first line of the file because contains information related to something about end-to-end
            # encryption
            fp.readline()
            messageBuffer = []
            date, time, author = None, None, None
            while True :
                line = fp.readline()
                if not line :
                    break
                line = line.strip()
                if Preprocess._startsWithDateAndTime(line):
                    if len(messageBuffer) > 0:
                        parsedData.append([date, time, author, ' '.join(messageBuffer)])
                    messageBuffer.clear()
                    date, time, author, message = Preprocess._getDataPoint(line)
                    messageBuffer.append(message)
                else:
                    messageBuffer.append(line)
        df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message'])
        df = df.dropna()
        df = df.reset_index(drop=True)
        df['Letter\'s'] = df['Message'].apply(lambda s: len(s))  # Count number of letters in each message
        df['Word\'s'] = df['Message'].apply(lambda s: len(s.split(' ')))  # Count number of word's in each message
        df["Date"] = pd.to_datetime(df["Date"])
        df['Media_Count'] = df.Message.apply(lambda x: re.findall(Preprocess.MEDIAPATTERN, x)).str.len()
        df['Url_Count'] = df.Message.apply(lambda x: re.findall(Preprocess.URLPATTERN, x)).str.len()
        weeks = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thrusday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }
        df['Day'] = df['Date'].dt.weekday.map(weeks)
        # Converting 12 hour formate to 24 hour.
        lst = []
        for i in df['Time']:
            out_time = datetime.strftime(datetime.strptime(i, "%I:%M %p"), "%H:%M")
            lst.append(out_time)
        df['24H_Time'] = lst
        df['Hours'] = df['24H_Time'].apply(lambda x: x.split(':')[0])
        df['Msg_count'] = df['Date'].map(df['Date'].value_counts().to_dict())
        df['Year'] = df['Date'].dt.year
        df['Mon'] = df['Date'].dt.month
        months = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
        }
        df['Month'] = df['Mon'].map(months)
        df.drop('Mon', axis=1, inplace=True)
        df["Month_Year"] = df.apply(lambda x: x["Month"] + " " + str(x["Year"]), axis=1)
        df['Msg_count_monthly'] = df['Month_Year'].map(df['Month_Year'].value_counts().to_dict())
        df['id'] = df.index
        if save_data == 'Y' or save_data == 'y' :
            df.to_csv(name)
        return df