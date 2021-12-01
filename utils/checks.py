from discord.ext import commands

def is_in_guild(guild_id, is_decorator=True):
    def predicate(ctx):
        return ctx.bot.get_guild(guild_id).get_member(ctx.message.author.id)
        
    if is_decorator:
        return commands.check(predicate)

    return predicate

def is_mod(is_decorator=True):
    return is_in_guild(is_decorator)