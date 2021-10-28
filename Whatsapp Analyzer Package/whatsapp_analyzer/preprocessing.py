import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import emoji
from wordcloud import WordCloud , STOPWORDS
from nltk import *
import plotly.express as px
from whatsapp_analyzer.analysis import Preprocess

class UserNotPresentException(Exception) :
    """
    This is user defined exception.
    """
    def __init__(self, args) :
        self.msg = args

class Analyzer(Preprocess) :
    """
    This class contains more than 15 methods which will help you to extract very very usefull insights from the chat. You need to do just one simple step.
    Only create object of Analyzer class and pass the location of txt file (chat file) and then use the object of Analyzer class to use different different
    interesting methods. Methods are listed below :

    * basicStats
    * wordCloud
    * mostActiveUsers
    * mostActiveDay
    * topMediaContributor
    * maxWordContributers
    * maxURLContributers
    * mostActiveTime
    * mostSuitableHours
    * wordCloud_in
    * highlyActiveDates
    * timeseriesAnalysis
    * activeMonthsB
    * maxEmojiUsers
    * trafficPerYear
    * activeMonthsT
    * weekdaysTraffic
    * topEmojis_G
    * topEmojis_I
    * saveDatframe

    For more detail checkout documentation of respective method, I have added short & beautiful doc of each method.

    Made with ❤ by ronil
    """
    def __init__(self, filepath, save_data = 'N') :
        self.df = Preprocess._processing(filepath, save_data)

    @classmethod
    def _preprocess_text(cls, df1) :
        """
        This method will preprocess the text for creating word cloud. It will remove impurity from text.

        :param df1: DataFrame from which we want to preprocess.
        :return: str
        """
        hindi = [chr(c) for c in range(0x0900, 0x097f)]
        df2 = df1[~(df1['Message'].str.contains('<Media omitted>')) &
                  ~(df1['Message'].str.contains('This message was deleted')) &
                  ~(df1['Message'].str.contains('https://')) &
                  ~(df1.Message.str.contains('|'.join(hindi)))]

        txt = " ".join(review for review in df2.Message)
        return txt

    def basicStats(self) :
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

    def wordCloud(self, save_fig = 'N') :
        """
        This method will create a word cloud, through which we can easily understand the most frequent words used in chat.

        :arg save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :returns: None
        """
        df1 = self.df
        text = Analyzer._preprocess_text(df1)
        wordcloud = WordCloud(width=1920, height=1080, background_color="white",
                              stopwords=STOPWORDS, random_state=42).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud)
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('wordcloud.png')
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

    def mostActiveUsers(self, save_fig = 'N') :
        """
        This method will create a bar chart for the top-10 most active members in the group.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
        df1 = self.df
        # Mostly Active Author in the Group
        plt.figure(figsize=(7, 5))
        mostly_active = df1['Author'].value_counts()
        # Top 10 peoples that are mostly active in our Group is :
        m_a = mostly_active.head(10)
        m_a = m_a.sort_values()
        m_a.plot.barh(color=['#696969', '#0ff1ce', '#ffd700', '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#8cff32'])
        plt.ylabel('Authors')
        plt.xlabel('No. of Messages')
        plt.title('Mostly Active Member\'s of Group', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Most Active Users.png', bbox_inches='tight')
        plt.show()

    def mostActiveDay(self, save_fig = 'N') :
        """
        This method will create a bar chart for traffic on whatsapp group on each weekdays.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
        df1 = self.df
        # Mostly Active day in the Group
        plt.figure(figsize=(7, 5))
        active_day = df1['Day'].value_counts()
        active_day = active_day.sort_values()
        active_day.plot.barh(color=['#8cff32', '#0ff1ce', '#ffd700', '#ffff00', '#ff0000', '#ac25e2', '#ff00ff'])
        plt.ylabel('Week Days')
        plt.xlabel('No. of Messages')
        plt.title('Mostly active day of Week in the Group', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Most Active Day.png', bbox_inches='tight')
        plt.show()

    def topMediaContributor(self, save_fig = 'N') :
        """
        This method will create bar chart to show top-10 media contributers in group.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return:
        """
        df1 = self.df
        # Top-10 Media Contributor of Group
        mm = df1[df1['Message'] == '<Media omitted>']
        mm1 = mm['Author'].value_counts()
        top10 = mm1.head(10)
        top10 = top10.sort_values()
        top10.plot.barh(color=['#696969', '#0ff1ce', '#ffd700', '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#8cff32'])
        plt.ylabel('Author\'s')
        plt.xlabel('No. of Media Messages')
        plt.title('Top-10 media contributor of Group', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Top Media Contributer.png', bbox_inches='tight')
        plt.show()

    def maxWordContributers(self, save_fig = 'N') :
        """
        It will create bar chart which will show top-10 authors who used max no. of words in their messages..

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
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
            plt.savefig('Max Word Contributers.png', bbox_inches='tight')
        plt.show()

    def maxURLContributers(self, save_fig = 'N') :
        """
        It will create bar chart which will show top-10 url contributers.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
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
            plt.savefig('Max URL Contributers.png', bbox_inches='tight')
        plt.show()

    def mostActiveTime(self, save_fig = 'N') :
        """
        It will create bar chart which will show time at which group was highly active.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
        df1 = self.df
        # Time whenever our group is mostly active
        plt.figure(figsize=(8, 5))
        t = df1['Time'].value_counts().head(20)
        tx = t.plot.bar(color=['#8cff32', '#0ff1ce', '#ffd700', '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#696969'])
        tx.yaxis.set_major_locator(MaxNLocator(integer=True))  # Converting y axis data to integer
        plt.xlabel('Time')
        plt.ylabel('No. of messages')
        plt.title('Analysis of time when Group was highly active.', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Most Active Time-Span.png', bbox_inches='tight')
        plt.show()

    def mostSuitableHours(self, save_fig = 'N') :
        """
        It will create a bar chart which will show a best time span at which there may be high chances getting responce from others.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
        df1 = self.df
        # Most suitable hour of day, whenever there will more chances of getting responce from group members.
        plt.figure(figsize=(8, 5))
        std_time = df1['Hours'].value_counts().head(15)
        s_T = std_time.plot.bar(color=['#8cff32', '#0ff1ce', '#ffd700', '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#696969'])
        s_T.yaxis.set_major_locator(MaxNLocator(integer=True))  # Converting y axis data to integer
        plt.xlabel('Hours (24-Hour)')
        plt.ylabel('No. of messages')
        plt.title('Most suitable hour of day.', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Most Suitable Hours.png', bbox_inches='tight')
        plt.show()

    def wordCloud_in(self, user, save_fig = 'N') :
        """
        If you want to create word cloud of particular individual then this method will help you, just pass user name and u will get desirable output.

        :param user: User whose word cloud you want to create.
        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
        df1 = self.df
        if user in self.df['Author'].dropna().unique() :
            text = Analyzer._preprocess_text(df1)
            wordcloud = WordCloud(width=1920, height=1080, background_color="white", stopwords=STOPWORDS,
                                  random_state=42).generate(text)
            plt.figure(figsize=(9, 4))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            if save_fig == 'Y' or save_fig == 'y':
                name = str(user) + ' Word Cloud' + '.png'
                plt.savefig(name, bbox_inches='tight')
            plt.show()
        else :
            raise UserNotPresentException('User is not a member of respective group.')

    def highlyActiveDates(self, save_fig = 'N') :
        """
        It will create a bar chart which will show highly active top-15 dates.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
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
            plt.savefig('Highly Active Dates.png', bbox_inches = 'tight')
        plt.show()

    def timeseriesAnalysis(self, save_fig = 'N') :
        """
        It will plot interactive time-series plot on traffic on respective group.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
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
            fig.write_html("Timeseries Plot.html")
        fig.show()

    def activeMonthsB(self, save_fig = 'N') :
        """
        It will create a bar chart of most active months on which group was highly active.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
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
            plt.savefig('Active Months.png', bbox_inches='tight')
        plt.show()

    @classmethod
    def _emoji_helper(cls, df):
        """
        This is a private method, help other methods to extract emojis from the chat.

        :param df: pandas dataframe
        :return: dictonary - It will return dictonary of enojis along with their respective count.
        """
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
        """
        This will plot a bar chart which will show top-15 users who used max no. of emojis in group.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
        df1 = self.df
        df = pd.DataFrame(Analyzer._emoji_helper(df1).items(), columns=['Users', 'No. of Emojies']).sort_values('No. of Emojies',
                            ascending=False).head(15).reset_index(drop=True)
        plt.rcParams["figure.figsize"] = [8, 5]
        users = df.sort_values('No. of Emojies', ascending=True).head(15)
        users.plot.barh(y='No. of Emojies', x='Users', color=['#8cff32', '#0ff1ce', '#ffd700',
                        '#ffff00', '#ff0000', '#ac25e2', '#ff00ff', '#00ced1', '#008080', '#696969'], legend=False)
        plt.ylabel('User\'s')
        plt.xlabel('No. of Emojies')
        plt.title('Member\'s who used Max. Emojies', fontdict={'fontsize': 13})
        if save_fig == 'Y' or save_fig == 'y' :
            plt.savefig('Emoji Users.png', bbox_inches='tight')
        plt.show()

    def trafficPerYear(self, save_fig = 'N') :
        """
        It will plot a bar chart, which will show traffic in group per year.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
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
            plt.savefig('Traffic Per Year.png', bbox_inches='tight')
        plt.show()

    def activeMonthsT(self, save_fig = 'N') :
        """
        This will create a timeseries plot, which will show traffic in group month wise.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
        df1 = self.df
        fig = px.line(data_frame=df1, x='Month_Year', y='Msg_count_monthly', template='none',
                      title='Analysis of Mostly Active Month',
                      labels={
                          "Month_Year": "Month-Year",
                          "Msg_count_monthly": "No of Messages",
                      })
        fig.update_traces(line_color='red', mode='markers+lines')
        if save_fig == 'y' or save_fig == 'Y' :
            fig.write_html("Timeseries Plot(Monthwise).html")
        fig.show()

    def weekdaysTraffic(self, save_fig = 'N') :
        """
        This is basically very interesting plot. It will create heat map which will basically show the weekdays traffic along with time span.

        :param save_fig: If you pass save_fig = Y or y, will save the plot. By default the value of save_fig is N.
        :return: None
        """
        df1 = self.df
        # if we want to transform data both column wise as well as row wise then we will preffer pivot table.
        htmp = pd.DataFrame(pd.pivot_table(df1, index=['Day'], values='id', columns='Hours', aggfunc='count')).replace(to_replace=np.NAN, value = 0)
        fig = px.imshow(htmp,
                        labels=dict(x="Hour(00:59) ", y="Weekday ", color='No. of messages '),
                        y=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday', 'Saturday'],
                        title='Weekdays VS Hours Chat Analysis',
                        color_continuous_scale='purples')
        fig.update_xaxes(side="top")
        fig.update_layout(width=990, height=505, coloraxis_colorbar=dict(
                        title="No. of Messages ", thicknessmode="pixels", thickness=30,
                        lenmode="pixels", len=305, yanchor="top", y=1,
                        ticks=None, ticksuffix=" Messages", dtick=50))
        if save_fig == 'y' or save_fig == 'Y' :
            fig.write_html("Weekdays Traffic.html")
        fig.show()

    # return top-20 emojies used by user's in this group
    @classmethod
    def _emoji_help(cls, df):
        """
        This is a private method which is basically used to extract emojis from messages.

        :param df: pandas dataframe
        :return: pandas dataframe
        """
        emojis = []
        for message in df['Message']:
            emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emojis', 'Count']).head(20).T

    def topEmojis_G(self) :
        """
        This method will return pandas dataframe of top-20 emojis used by users.

        :return: pandas dataframe
        """
        df1 = self.df
        return Analyzer._emoji_help(df1)

    # return top 10 emojies of particular user
    @classmethod
    def _emoji_extractor(cls, selected_user, df) :
        """
        This is private method which basically help other instance method to extract emojis from chat.

        :param selected_user: User whose top-10 emojis you want to extract.
        :param df: pandas dataframe
        :return: pandas dataframe
        """
        emojis = []
        for message in df[df['Author'] == selected_user]['Message']:
            emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emojis', 'Count']).head(10).T

    def topEmojis_I(self, user) :
        """
        This method will return top-10 emjois that are used by user.

        :param user: Here we need to pass user, whose top-10 emojis we want to extract.
        :return: pandas dataframe - It will return pandas dataframe which will contain top-10 emojis used user.
        """
        df1 = self.df
        if user in df1['Author'].unique() :
            return Analyzer._emoji_extractor(user, df1)
        else :
            raise UserNotPresentException('User is not a member of respective group.')

    def saveDatframe(self, name = 'whatsapp chat.csv') :
        """
        If you want to save the preprocesses data as csv file then this method is for u.

        :param name: Actually by default CSV file name is available, but if you want to give some different name to CSV file then you pass the name here.
        :return: None
        """
        self.df.to_csv(name)
