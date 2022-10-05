
def get_channel(client, channel_name):
    """
    Retrieve the Discord channel object

    :param client:
    :param channel_name:
    :return:
    """

    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel_name == channel.name:
                return channel
    return False
