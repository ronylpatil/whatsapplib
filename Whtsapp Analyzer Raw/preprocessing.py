import re
import pandas as pd
from datetime import datetime



# def startsWithDateAndTime(s):
#     # regex pattern for date.
#     # pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9][0-9]), ([0-9]+):([0-9][0-9]) (AM|PM) -'
#     pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9][0-9]), ([0-9]+):([0-9][0-9]) (am|pm) - '
#
#     result = re.match(pattern, s)
#     if result:
#         return result
#     return False
#
#
# # Finds username of any given format.
# def FindAuthor(s):
#     patterns = [
#         '([\w]+):',  # First Name
#         '([\w]+[\s]+[\w]+):',  # First Name + Last Name
#         '([\w]+[\s]+[\w]+[\s]+[\w]+):',  # First Name + Middle Name + Last Name
#         '([+]\d{2} \d{5} \d{5}):',  # Mobile Number (India no.)
#         '([+]\d{2} \d{3} \d{3} \d{4}):',  # Mobile Number (US no.)
#         '([\w]+)[\u263a-\U0001f999]+:',  # Name and Emoji
#     ]
#     pattern = '^' + '|'.join(patterns)
#     result = re.match(pattern, s)
#     if result:
#         return result
#     return False
#
#
# def getDataPoint(line):
#     splitLine = line.split(' - ')
#     dateTime = splitLine[0]
#     date, time = dateTime.split(', ')
#     message = ' '.join(splitLine[1:])
#     if FindAuthor(message):
#         splitMessage = message.split(': ')
#         author = splitMessage[0]
#         message = ' '.join(splitMessage[1:])
#     else:
#         author = None
#
#     return date, time, author, message
#
# def get_date(file_path) :
#     file1 = open('whtsapp_analyzer//settings//config.txt', 'w')
#     file1.write(file_path)
#     file1.close()
#
#     return _processing(file_path)
#
# def _processing(file_path) :
#     parsedData = []  # List to keep track of data so it can be used by a Pandas dataframe
#     # Uploading exported chat file
#     # conversationPath = r'E:\DHL Project\WhatsApp Group Chat Lib\Samp.txt' # chat file
#     conversationPath = file_path
#     with open(conversationPath, encoding="utf-8") as fp:
#         # Skipping first line of the file because contains information related to something about end-to-end encryption
#         fp.readline()
#         messageBuffer = []
#         date, time, author = None, None, None
#         while True:
#             line = fp.readline()
#             if not line:
#                 break
#             line = line.strip()
#             if startsWithDateAndTime(line):
#                 if len(messageBuffer) > 0:
#                     parsedData.append([date, time, author, ' '.join(messageBuffer)])
#                 messageBuffer.clear()
#                 date, time, author, message = getDataPoint(line)
#                 messageBuffer.append(message)
#             else:
#                 messageBuffer.append(line)
#
#     df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message'])
#     df["Date"] = pd.to_datetime(df["Date"])
#     return df

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import *
import datetime as dt
from matplotlib.ticker import MaxNLocator
import regex
import emoji
from seaborn import *
from heatmap import heatmap
from wordcloud import WordCloud , STOPWORDS , ImageColorGenerator
from nltk import *
from plotly import express as px
import plotly.express as px
import operator

import whtsapp_analyzer.analysis
from whtsapp_analyzer.analysis import Preprocess1

# class Preprocess1 :
#     URLPATTERN = r'(https?://\S+)'
#     MEDIAPATTERN = r'<Media omitted>'
#
#     def __init__(self) :
#         pass
#
#     # extract date time pattern
#     def _startsWithDateAndTime(s):
#         # regex pattern for date.
#         # pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9][0-9]), ([0-9]+):([0-9][0-9]) (AM|PM) -'
#         pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9][0-9]), ([0-9]+):([0-9][0-9]) (am|pm) - '
#
#         result = re.match(pattern, s)
#         if result:
#             return result
#         return False
#
#     # extract user name pattern
#     def _FindAuthor(s):
#         patterns = [
#             '([\w]+):',  # First Name
#             '([\w]+[\s]+[\w]+):',  # First Name + Last Name
#             '([\w]+[\s]+[\w]+[\s]+[\w]+):',  # First Name + Middle Name + Last Name
#             '([+]\d{2} \d{5} \d{5}):',  # Mobile Number (India no.)
#             '([+]\d{2} \d{3} \d{3} \d{4}):',  # Mobile Number (US no.)
#             '([\w]+)[\u263a-\U0001f999]+:',  # Name and Emoji
#         ]
#         pattern = '^' + '|'.join(patterns)
#         result = re.match(pattern, s)
#         if result:
#             return result
#         return False
#
#     # extract date, time, author & message
#     def _getDataPoint(line):
#         splitLine = line.split(' - ')
#         dateTime = splitLine[0]
#         date, time = dateTime.split(', ')
#         message = ' '.join(splitLine[1:])
#         if Preprocess1._FindAuthor(message):
#             splitMessage = message.split(': ')
#             author = splitMessage[0]
#             message = ' '.join(splitMessage[1:])
#         else:
#             author = None
#
#         return date, time, author, message
#
#     def _processing(file_path, save_data) :
#         parsedData = []  # List to keep track of data so it can be used by a Pandas dataframe
#         # Uploading exported chat file
#         # conversationPath = r'E:\DHL Project\WhatsApp Group Chat Lib\Samp.txt' # chat file
#         conversationPath = file_path
#         with open(conversationPath, encoding="utf-8") as fp :
#             # Skipping first line of the file because contains information related to something about end-to-end
#             # encryption
#             fp.readline()
#             messageBuffer = []
#             date, time, author = None, None, None
#             while True :
#                 line = fp.readline()
#                 if not line :
#                     break
#                 line = line.strip()
#                 if Preprocess1._startsWithDateAndTime(line):
#                     if len(messageBuffer) > 0:
#                         parsedData.append([date, time, author, ' '.join(messageBuffer)])
#                     messageBuffer.clear()
#                     date, time, author, message = Preprocess1._getDataPoint(line)
#                     messageBuffer.append(message)
#                 else:
#                     messageBuffer.append(line)
#
#         df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message'])
#         df["Date"] = pd.to_datetime(df["Date"])
#         df['Media_Count'] = df.Message.apply(lambda x: re.findall(Preprocess1.MEDIAPATTERN, x)).str.len()
#         df['Url_Count'] = df.Message.apply(lambda x: re.findall(Preprocess1.URLPATTERN, x)).str.len()
#
#         weeks = {
#             0: 'Monday',
#             1: 'Tuesday',
#             2: 'Wednesday',
#             3: 'Thrusday',
#             4: 'Friday',
#             5: 'Saturday',
#             6: 'Sunday'
#         }
#         df['Day'] = df['Date'].dt.weekday.map(weeks)
#
#         if save_data == 'Y' or save_data == 'y' :
#             print('Save fig execute hua...')
#             df.to_csv('whatsapp_dataset.csv')
#             # df.to_pickle('data.pkl')
#         return df

class UserNotPresentException(Exception) :
    def __init__(self, args) :
        self.msg = args


class Preprocess(Preprocess1) :


    def __init__(self, filepath, save_data = 'N') :
        self.df = Preprocess1._processing(filepath, save_data)

    # def get_data(file_path):
    #     file1 = open('whtsapp_analyzer//settings//config.txt', 'w')
    #     file1.write(file_path)
    #     file1.close()
    #
    #     return Preprocess._processing(file_path)
    #
    # def load_file(filepath) :
    #
    #     file = open('settings//config.txt', 'r')
    #     path = file.readline()
    #     file.close()
    #     open("settings//config.txt", "w").close()


    # def save_data(self) :
    #     print(self.filepath)
    #     print('We are going to save the preprocessed data in the form of pickel file.')
    #     df = Preprocess._processing(self.filepath)   # it will return dataframe
    #     df.to_pickle("dummy.pkl")
    #     print('Data saved sucessfully...')
    #
    # def load_data(self) :
    #     df = pd.read_pickle("dummy.pkl")
    #     print('Shape of dataframe : ', df.shape)
    #     print('Task Completed!!!')


    # @classmethod
    # def _get_filepath(cls) :
    #     file = open('settings//config.txt', 'r')
    #     filepath = file.readline()
    #     file.close()
    #     open("settings//config.txt", "w").close()
    #     return filepath

    @classmethod
    def _preprocess_text(cls, df1) :
        hindi = [chr(c) for c in range(0x0900, 0x097f)]
        df2 = df1[~(df1['Message'].str.contains('<Media omitted>')) &
                  ~(df1['Message'].str.contains('This message was deleted')) &
                  ~(df1['Message'].str.contains('https://')) &
                  ~(df1.Message.str.contains('|'.join(hindi)))]

        txt = " ".join(review for review in df2.Message)
        return txt

    def word_cloud(self, save_fig = 'N') :
        """It will plot a word cloud, through which you can easily understand the most frequent words used in chat.

        :arg save_fig: It will save the plot.
        :returns: None
        """
        df1 = self.df
        # hindi = [chr(c) for c in range(0x0900, 0x097f)]
        #
        # df2 = df1[~(df1['Message'].str.contains('<Media omitted>')) &
        #           ~(df1['Message'].str.contains('This message was deleted')) &
        #           ~(df1['Message'].str.contains('https://')) &
        #           ~(df1.Message.str.contains('|'.join(hindi)))]
        #
        # text = " ".join(review for review in df2.Message)

        text = Preprocess._preprocess_text(df1)
        wordcloud = WordCloud(width=1920, height=1080, background_color="white",
                              stopwords=STOPWORDS, random_state=42).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud)
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('wordcloud.png')
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

    def basic_stats(self) :
        """
        It will return some basic stats of group. This method will return 4 args.
            1. total_users - Total No. of users in group.
            2. total_messages - Total No. of messages sent.
            3. media_messages - Total No. of media messages sent.
            4. links - Total No. of links shared in group.
        """
        df1 = self.df
        total_users = len(df1['Author'].unique())
        total_messages = df1.shape[0]
        media_messages = df1[df1['Message'] == '<Media omitted>'].shape[0]
        links = np.sum(df1.Url_Count)
        return total_users, total_messages, media_messages, links

    def most_active_members(self, save_fig = 'N') :
        df1 = self.df

        # Mostly Active Author in the Group
        plt.figure(figsize=(7, 5))
        mostly_active = df1['Author'].value_counts()
        # Top 10 peoples that are mostly active in our Group is :
        m_a = mostly_active.head(10)
        m_a = m_a.sort_values()
        m_a.plot.barh(color=['#696969', '#0ff1ce', '#ffd700',
                             '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#8cff32'])
        plt.ylabel('Authors')
        plt.xlabel('No. of Messages')
        plt.title('Mostly Active Member\'s of Group', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Most Active Members.png', bbox_inches='tight')
        plt.show()

    def most_active_day(self, save_fig = 'N') :
        df1 = self.df
        # Mostly Active day in the Group
        plt.figure(figsize=(7, 5))
        active_day = df1['Day'].value_counts()
        # Top 10 peoples that are mostly active in our Group is :
        a_d = active_day.head(10)
        a_d = a_d.sort_values()
        a_d.plot.barh(color=['#8cff32', '#0ff1ce', '#ffd700',
                             '#ffff00', '#ff0000', '#ac25e2', '#ff00ff'])
        plt.ylabel('Week Days')
        plt.xlabel('No. of Messages')
        plt.title('Mostly active day of Week in the Group', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Most Active Day.png', bbox_inches='tight')
        plt.show()

    def topMediaContributor(self, save_fig = 'N') :
        df1 = self.df
        # Top-10 Media Contributor of Group
        mm = df1[df1['Message'] == '<Media omitted>']
        mm1 = mm['Author'].value_counts()
        top10 = mm1.head(10)
        top10 = top10.sort_values()
        top10.plot.barh(color=['#696969', '#0ff1ce', '#ffd700',
                               '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#8cff32'])
        plt.ylabel('Author\'s')
        plt.xlabel('No. of Media Messages')
        plt.title('Top-10 media contributor of Group', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Media Contributer.png', bbox_inches='tight')
        plt.show()


    def maxwordContributers(self, save_fig = 'N') :
        df1 = self.df
        # Words are most powerful weapon in the world so lets check who has this powerful weapon in this Group
        max_words = df1[['Author', 'Word\'s']].groupby('Author').sum()
        m_w = max_words.sort_values('Word\'s', ascending=False).head(10)
        m_w = m_w.sort_values('Word\'s')
        m_w.plot.barh(color=['#0ff1ce'], legend = False)
        plt.ylabel('Authors')
        plt.xlabel('No. of Words')
        plt.title('Analysis of Members who has used Max. No of Words in their Messages')
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Max Word Contributer.png', bbox_inches='tight')
        plt.show()


    def maxURLContributers(self, save_fig = 'N') :
        df1 = self.df
        # Member who has shared max numbers of link in Group
        max_words = df1[['Author', 'Url_Count']].groupby('Author').sum()
        m_w = max_words.sort_values('Url_Count', ascending=False).head(10)
        # m_w
        m_w = m_w.sort_values('Url_Count')
        m_w.plot.barh(color='#ffd700', legend = False)
        plt.ylabel('Authors')
        plt.xlabel('No. of Link\'s Shared')
        plt.title('Analysis of member\'s who has shared max no. of link\'s in Group')
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('URL Contributer.png', bbox_inches='tight')
        plt.show()

    def mostActiveTime(self, save_fig = 'N') :
        df1 = self.df
        # Time whenever our group is mostly active
        plt.figure(figsize=(8, 5))
        t = df1['Time'].value_counts().head(20)
        tx = t.plot.bar(color=['#8cff32', '#0ff1ce', '#ffd700',
                               '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#696969'])
        tx.yaxis.set_major_locator(MaxNLocator(integer=True))  # Converting y axis data to integer
        plt.xlabel('Time')
        plt.ylabel('No. of messages')
        plt.title('Analysis of time when Group was highly active.', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Most Active Time Span.png', bbox_inches='tight')
        plt.show()

    def mostSuitableHours(self, save_fig = 'N') :
        df1 = self.df
        # Most suitable hour of day, whenever there will more chances of getting responce from group members.
        plt.figure(figsize=(8, 5))
        std_time = df1['Hours'].value_counts().head(15)
        s_T = std_time.plot.bar(color=['#8cff32', '#0ff1ce', '#ffd700',
                                       '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#696969'])
        s_T.yaxis.set_major_locator(MaxNLocator(integer=True))  # Converting y axis data to integer
        plt.xlabel('Hours (24-Hour)')
        plt.ylabel('No. of messages')
        plt.title('Most suitable hour of day.', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('mostActiveMembers.png', bbox_inches='tight')
        plt.show()

    def wordCloud_in(self, user, save_fig = 'N') :
        df1 = self.df
        if user in self.df['Author'].dropna().unique() :
            # hindi = [chr(c) for c in range(0x0900, 0x097f)]
            # # Filtering out messages of particular user
            # m_chat = df1[df1["Author"] == user]
            # # preprocessing the messages...
            # mcht2 = m_chat[~(m_chat['Message'].str.contains('<Media omitted>')) &
            #                ~(m_chat['Message'].str.contains('This message was deleted')) &
            #                ~(m_chat['Message'].str.contains('https://')) &
            #                ~(m_chat.Message.str.contains('|'.join(hindi)))
            #                ]


            # text = " ".join(review for review in mcht2.Message)

            text = Preprocess._preprocess_text(df1)
            wordcloud = WordCloud(width=1920, height=1080, background_color="white", stopwords=STOPWORDS,
                                  random_state=42).generate(text)
            plt.figure(figsize=(9, 4))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            if save_fig == 'Y' or save_fig == 'y':
                plt.savefig('mostActiveMembers.png', bbox_inches='tight')
            plt.show()
        else :
            raise UserNotPresentException('User is not a member of respective group.')


    def heavilyActiveDates(self, save_fig = 'N') :
        df1 = self.df

        # Date on which our Group was highly active.
        plt.figure(figsize=(8, 5))
        x = df1['Date'].value_counts().head(15).sort_values()
        x.plot.barh(color=['#8cff32', '#0ff1ce', '#ffd700',
                           '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#696969'])
        plt.ylabel('Date')
        plt.xlabel('No. of Messages')
        plt.title('Analysis of Date on which Group was highly active', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y':
            plt.savefig('mostActiveMembers.png', bbox_inches = 'tight')
        plt.show()


    def timeseriesAnalysis(self, save_fig = 'N') :
        df1 = self.df
        # Timeseries plot
        fig = px.line(x=df1['Date'], y=df1['Msg_count'], template='none',
                      labels={'x': "Month-Year", 'y': 'No. of Messages'})
        fig.update_layout(title='Analysis of number of message\'s using TimeSeries plot.',
                          xaxis_title='Month-Year',
                          yaxis_title='No. of Messages')
        fig.update_xaxes(nticks=20)
        fig.update_traces(line_color='red')
        if save_fig == 'y' or save_fig == 'Y' :
            fig.write_html("timeseries plot.html")
        fig.show()


    def activeMonthsB(self, save_fig = 'N') :
        df1 = self.df
        # Mostly Active month
        plt.figure(figsize=(12, 8))
        a_m = df1['Month_Year'].value_counts()
        a_m = a_m.sort_values()
        a_m.plot.barh(color=['#8cff32', '#0ff1ce', '#ffd700',
                             '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#696969'])
        plt.ylabel('Month')
        plt.xlabel('No. of messages')
        plt.title('Analysis of mostly active month.', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('mostActiveMembers.png', bbox_inches='tight')
        plt.show()

    @classmethod
    def _emoji_helper(cls, df):
        emoji_dict = {}
        for i in df['Author'].unique():
            emojis = []
            for message in df[df['Author'] == i]['Message']:
                emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
                if len(Counter(emojis).most_common(len(Counter(emojis)))) > 0:
                    emoji_dict.update({i: []})
                    emoji_dict[i] = len(Counter(emojis).most_common(len(Counter(emojis))))
        return emoji_dict

    def maxEmojiUsers(self, save_fig = 'N') :
        df1 = self.df
        df = pd.DataFrame(Preprocess._emoji_helper(df1).items(), columns=['Users', 'No. of Emojies']).sort_values('No. of Emojies',
                            ascending=False).head(15).reset_index(drop=True)

        plt.rcParams["figure.figsize"] = [8, 5]
        users = df.sort_values('No. of Emojies', ascending=True).head(15)
        users.plot.barh(y='No. of Emojies', x='Users', color=['#8cff32', '#0ff1ce', '#ffd700',
                        '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#696969'], legend=False)
        plt.ylabel('User\'s')
        plt.xlabel('No. of Emojies')
        plt.title('Member\'s who used Max. Emojies', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('mostActiveMembers.png', bbox_inches='tight')
        plt.show()


    def trafficPerYear(self, save_fig = 'N') :
        df1 = self.df
        # Total message per year
        # As we analyse that the group is created in mid 2019 thats why number of messages in 2019 is less.
        plt.figure(figsize=(7, 4))
        a_m = df1['Year'].value_counts()
        a_m.plot.bar(color=['#ffff00', '#ff0000', '#ac25e2'])
        plt.xlabel('years')
        # plt.xticks(rotation = 45)
        plt.ylabel('No. of Messages')
        plt.title('Analysis of Most Active Year', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('mostActiveMembers.png', bbox_inches='tight')
        plt.show()

    def activeMonthT(self, save_fig = 'N') :
        df1 = self.df

        fig = px.line(data_frame=df1, x='Month_Year', y='Msg_count_monthly', template='none',
                      title='Analysis of Mostly Active Month',
                      labels={
                          "Month_Year": "Month-Year",
                          "Msg_count_monthly": "No of Messages",
                      })
        fig.update_traces(line_color='red', mode='markers+lines')
        if save_fig == 'y' or save_fig == 'Y' :
            fig.write_html("timeseries plot(Monthwise).html")
        fig.show()

    def weekdaysTraffic(self, save_fig = 'N') :
        df1 = self.df
        # if we want to transform data both column wise as well as row wise then we will preffer pivot table.
        htmp = pd.DataFrame(pd.pivot_table(df1, index=['Day'], values='id', columns='Hours', aggfunc='count')).replace(to_replace=np.NAN, value = 0)
        # print(htmp)
        fig = px.imshow(htmp,
                        labels=dict(x="Hour(00:59) ", y="Weekday ", color='No. of messages '),
                        y=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday', 'Saturday'],
                        title='Weekdays VS Hours Chat Analysis',
                        color_continuous_scale='purples')

        fig.update_xaxes(side="top")
        fig.update_layout(width=990,
                          height=505, coloraxis_colorbar=dict(
                title="No. of Messages ",
                thicknessmode="pixels", thickness=30,
                lenmode="pixels", len=305,
                yanchor="top", y=1,
                ticks=None, ticksuffix=" Messages",
                dtick=50
            ))
        if save_fig == 'y' or save_fig == 'Y' :
            fig.write_html("timeseries plot(Monthwise).html")
        fig.show()

    # return top-20 emojies used by user's in this group
    @classmethod
    def _emoji_help(cls, df):
        emojis = []
        for message in df['Message']:
            emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emojis', 'Count']).head(20).T

    def topEmojis_G(self) :
        df1 = self.df
        return Preprocess._emoji_help(df1)

    # return top 10 emojies of particular user
    @classmethod
    def _emoji_extractor(cls, selected_user, df) :
        emojis = []
        for message in df[df['Author'] == selected_user]['Message']:
            emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emojis', 'Count']).head(10).T

    def topEmojis_I(self, user) :
        df1 = self.df
        if user in df1['Author'].unique() :
            return Preprocess._emoji_extractor(user, df1)
        else :
            raise UserNotPresentException('User is not a member of respective group.')


    def saveDatframe(self, name = 'whatsapp chat.csv') :
        self.df.to_csv(name)
