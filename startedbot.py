import os
import time
import re
from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient('xoxb-1281610146097-2213715121378-yWzg5daaSFtGyekMqZqxWt6X')
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

# logger
import logging
logging.basicConfig(filename="/tmp/slackbot.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith('report'):
        logger.info("found below command : %s" %command)
        build = str(command.split(':')[1])
        #areas = command.split(':')[2].split(',')
        print(build)
        #print(type(areas))
        from get_cibot_info import GetCIBot
        cibot = GetCIBot()
        my_data = cibot.get_suite_result_per_area(int(build))
        print(my_data)
        logger.info("cibot.get_suite_result_per_area retured below data: %s" %my_data)
        response = my_data

    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    while True:
        #try:
            if slack_client.rtm_connect(with_team_state=False):
                print("Starter Bot connected and running!")
                logger.info("Starter Bot connected and running!")
                # Read bot's user ID by calling Web API method `auth.test`
                starterbot_id = slack_client.api_call("auth.test")["user_id"]
                while True:
                    command, channel = parse_bot_commands(slack_client.rtm_read())
                    if command:
                        handle_command(command, channel)
                    time.sleep(RTM_READ_DELAY)
            else:
                print("Connection failed. Exception traceback printed above.")
                logger.warning("Connection failed. Exception traceback printed above.")
        #except:
        #    logger.error("slackbot disconected, will try to start again ")
