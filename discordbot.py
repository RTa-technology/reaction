import discord
from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_message(message):
    """メンバー募集 (.rect@数字)"""
    if message.content.startswith(".rect"):
        mcount = int(message.content[6:len(message.content)])
        text= "あと{}人 参加待機中\n"
        revmsg = text.format(mcount)
        #friend_list 押した人のList
        frelist = []
        msg = await bot.send_message(message.channel, revmsg)

        #投票の欄
        await bot.add_reaction(msg, '\u21a9')
        await bot.add_reaction(msg, '⏫')
        await bot.pin_message(msg)

        #リアクションをチェックする
        while len(frelist) < int(message.content[6:len(message.content)]):
            target_reaction = await bot.wait_for_reaction(message=msg)
            #発言したユーザが同一でない場合 真
            if target_reaction.user != msg.author:
                #==============================================================
                #押された絵文字が既存のものの場合 >> 左　del
                if target_reaction.reaction.emoji == '\u21a9':
                    #==========================================================
                    #◀のリアクションに追加があったら反応 frelistにuser.nameがあった場合　真
                    if target_reaction.user.name in frelist:
                        frelist.remove(target_reaction.user.name)
                        mcount += 1
                        #リストから名前削除
                        await bot.edit_message(msg, text.format(mcount) +
                                                        '\n'.join(frelist))
                            #メッセージを書き換え

                    else:
                        pass
                #==============================================================
                #押された絵文字が既存のものの場合　>> 右　add
                elif target_reaction.reaction.emoji == '⏫':
                    if target_reaction.user.name in frelist:
                        pass

                    else:
                        frelist.append(target_reaction.user.name)
                        #リストに名前追加
                        mcount = mcount - 1
                        await bot.edit_message(msg, text.format(mcount) +
                                                        '\n'.join(frelist))


                elif target_reaction.reaction.emoji == '✖':
                        await bot.edit_message(msg, '募集終了\n'+ '\n'.join(frelist))
                        await bot.unpin_message(msg)
                        break
                await bot.remove_reaction(msg, target_reaction.reaction.emoji, target_reaction.user)
                #ユーザーがつけたリアクションを消す※権限によってはエラー
                #==============================================================
        else:
            await bot.edit_message(msg, '募集終了\n'+ '\n'.join(frelist))



bot.run(token)
