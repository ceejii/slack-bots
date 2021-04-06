from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, process, on
import re

from base.slack import Slack
from utils.command_descriptions import Command, CommandDescriptions
from utils.bot_descriptions import Bot, BotDescriptions

class AnswerFAQPlugin(MachineBasePlugin):
   
    #TODO use message payload for the weblinks?

    commands = CommandDescriptions()

    def init(self):
        self.bots = BotDescriptions()
        faqBot = Bot("faqbot", "svarar på diverse frågor")
        self.bots.add(faqBot)

    #def init_final(self):
    @process('hello')
    def start(self, event):
        self.slackUtil = Slack(self)
        self.slackUtil.sendStatusMessage("FAQ bot started.")

    command = Command('faqbot', 'Beskrivning av faq botten')
    commands.add(command)
    @listen_to(regex=command.regex)
    def aboutFAQQuestion(self, msg):
        msgToSend="Faq botten svarar på diverse frågor\n Argument delas upp med :\n"+str(self.commands) #TODO fix : so it is in a settings file
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('about','Information om bottarna')
    commands.add(command)
    @listen_to(regex=command.regex)
    def aboutBotsQuestion(self, msg):
        msgToSend="Spacet har flera olika slack bottar.\n"+str(self.bots)
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('faq','Länk till Makerspace FAQ')
    commands.add(command)
    @listen_to(regex=command.regex)
    def faqQuestion(self, msg):
        msgToSend="Makerspace FAQ: https://wiki.makerspace.se/Makerspace_FAQ"
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('nyckel','Information om nyckelutlämningar')
    commands.add(command)
    @listen_to(regex=r'nyckelutlämning.*\?')
    @listen_to(regex=command.regex)
    def keyQuestion(self, msg):
        msgToSend=":key: Du vill nog ha info om nyckelutlämningar. TBC :)" #TODO
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('box','Information om hur det fungerar med labblåda')
    commands.add(command)
    @listen_to(regex=command.regex)
    def boxQuestion(self, msg):
        msgToSend="Labblådan ska vara SmartStore Classic 31, den säljs tex av Clas Ohlsson och Jysk. Tänk på att man inte får förvara lithiumbatterier för radiostyrt på spacet pga brandrisken. Kemikalier ska förvaras kemiskåpet, ej i lådan. Mer info om förvaring på spacet och exempel på lådor finns på: https://wiki.makerspace.se/Medlems_F%C3%B6rvaring"
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('sopor','Information om sophantering')
    commands.add(command)
    @listen_to(regex=command.regex)
    def garbageQuestion(self, msg):
        msgToSend="Nyckelkortet till soprummet finns i städskrubben. Soprummet ligger på lastkajen bakom huset. Mer info och karta till soprummet finns på: https://wiki.makerspace.se/Sophantering)"
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('wiki','Länkar till wiki sidan som motsvarar argumentet', 1)
    commands.add(command)
    @listen_to(regex=command.regex)
    def wikiQuestion(self, msg):
        argList = self.slackUtil.getArguments(msg)
        msgToSend="https://wiki.makerspace.se/"+argList[0]
        self.slackUtil.sendMessage(msgToSend, msg)

    @process('member_joined_channel')
    def newMemberJoinChannel(self, event):
        if event['channel'] == self.find_channel_by_name("botlog").id: #TODO change to general when we are done
            self.slackUtil.sendStatusMessage("new member joined botlog")
            slackUser = self.slackUtil.getSlackUserByID(event['user'])
            #TODO slack machine need to be fixed for this to work
            #self.slackUtil.sendDirectMessage("Hej du gick med i botlog kanalen", slackUser)

#TODO inköpsansvariga
