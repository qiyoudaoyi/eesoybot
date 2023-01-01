from asyncio.log import logger
import random
from discord import app_commands as ac, Interaction, Message
from discord.app_commands import Group
from discord.ext.commands import Bot, Cog
from utils import get_lumberjack, Config
import aiohttp

logger = get_lumberjack('emomix')
emo_base_url = 'https://www.gstatic.com/android/keyboard/emojikitchen'
knownSupportedDates = [
    '20201001',
    '20210218',
    '20210521',
    '20210831',
    '20211115',
    '20220110',
    '20220203',
    '20220406',
    '20220506',
    '20220815',
    '20220823',
]

knownSupportedEmoji = {
    "1fa84",  # 🪄
    "1f600",  # 😀
    "1f603",  # 😃
    "1f604",  # 😄
    "1f601",  # 😁
    "1f606",  # 😆
    "1f605",  # 😅
    "1f602",  # 😂
    "1f923",  # 🤣
    "1f62d",  # 😭
    "1f609",  # 😉
    "1f617",  # 😗
    "1f619",  # 😙
    "1f61a",  # 😚
    "1f618",  # 😘
    "1f970",  # 🥰
    "1f60d",  # 😍
    "1f929",  # 🤩
    "1f973",  # 🥳
    "1f643",  # 🙃
    "1f642",  # 🙂
    "1f972",  # 🥲
    "1f979",  # 🥹
    "1f60b",  # 😋
    "1f61b",  # 😛
    "1f61d",  # 😝
    "1f61c",  # 😜
    "1f92a",  # 🤪
    "1f607",  # 😇
    "1f60a",  # 😊
    "263a-fe0f",  # ☺️
    "1f60f",  # 😏
    "1f60c",  # 😌
    "1f614",  # 😔
    "1f611",  # 😑
    "1f610",  # 😐
    "1f636",  # 😶
    "1fae1",  # 🫡
    "1f914",  # 🤔
    "1f92b",  # 🤫
    "1fae2",  # 🫢
    "1f92d",  # 🤭
    "1f971",  # 🥱
    "1f917",  # 🤗
    "1fae3",  # 🫣
    "1f631",  # 😱
    "1f928",  # 🤨
    "1f9d0",  # 🧐
    "1f612",  # 😒
    "1f644",  # 🙄
    "1f62e-200d-1f4a8",  # 😮‍💨
    "1f624",  # 😤
    "1f620",  # 😠
    "1f621",  # 😡
    "1f92c",  # 🤬
    "1f97a",  # 🥺
    "1f61f",  # 😟
    "1f625",  # 😥
    "1f622",  # 😢
    "2639-fe0f",  # ☹️
    "1f641",  # 🙁
    "1fae4",  # 🫤
    "1f615",  # 😕
    "1f910",  # 🤐
    "1f630",  # 😰
    "1f628",  # 😨
    "1f627",  # 😧
    "1f626",  # 😦
    "1f62e",  # 😮
    "1f62f",  # 😯
    "1f632",  # 😲
    "1f633",  # 😳
    "1f92f",  # 🤯
    "1f62c",  # 😬
    "1f613",  # 😓
    "1f61e",  # 😞
    "1f616",  # 😖
    "1f623",  # 😣
    "1f629",  # 😩
    "1f62b",  # 😫
    "1f635",  # 😵
    "1fae5",  # 🫥
    "1f634",  # 😴
    "1f62a",  # 😪
    "1f924",  # 🤤
    "1f31b",  # 🌛
    "1f31c",  # 🌜
    "1f31a",  # 🌚
    "1f31d",  # 🌝
    "1f31e",  # 🌞
    "1fae0",  # 🫠
    "1f636-200d-1f32b-fe0f",  # 😶‍🌫️
    "1f974",  # 🥴
    "1f975",  # 🥵
    "1f976",  # 🥶
    "1f922",  # 🤢
    "1f92e",  # 🤮
    "1f927",  # 🤧
    "1f912",  # 🤒
    "1f915",  # 🤕
    "1f637",  # 😷
    "1f920",  # 🤠
    "1f911",  # 🤑
    "1f60e",  # 😎
    "1f913",  # 🤓
    "1f978",  # 🥸
    "1f925",  # 🤥
    "1f921",  # 🤡
    "1f47b",  # 👻
    "1f4a9",  # 💩
    "1f47d",  # 👽
    "1f916",  # 🤖
    "1f383",  # 🎃
    "1f608",  # 😈
    "1f47f",  # 👿
    "1f525",  # 🔥
    "1f4ab",  # 💫
    "2b50",  # ⭐
    "1f31f",  # 🌟
    "1f4a5",  # 💥
    "1f4af",  # 💯
    "1fae7",  # 🫧
    "1f573-fe0f",  # 🕳️
    "1f38a",  # 🎊
    "2764-fe0f",  # ❤️
    "1f9e1",  # 🧡
    "1f49b",  # 💛
    "1f49a",  # 💚
    "1f499",  # 💙
    "1f49c",  # 💜
    "1f90e",  # 🤎
    "1f5a4",  # 🖤
    "1f90d",  # 🤍
    "2665-fe0f",  # ♥️
    "1f498",  # 💘
    "1f49d",  # 💝
    "1f496",  # 💖
    "1f497",  # 💗
    "1f493",  # 💓
    "1f49e",  # 💞
    "1f495",  # 💕
    "1f48c",  # 💌
    "1f49f",  # 💟
    "2763-fe0f",  # ❣️
    "2764-fe0f-200d-1fa79",  # ❤️‍🩹
    "1f494",  # 💔
    "1f48b",  # 💋
    "1f9e0",  # 🧠
    "1fac0",  # 🫀
    "1fac1",  # 🫁
    "1fa78",  # 🩸
    "1f9a0",  # 🦠
    "1f9b7",  # 🦷
    "1f9b4",  # 🦴
    "1f480",  # 💀
    "1f440",  # 👀
    "1f441-fe0f",  # 👁️
    "1fae6",  # 🫦
    "1f44d",  # 👍
    "1f937",  # 🤷
    "1f490",  # 💐
    "1f339",  # 🌹
    "1f33a",  # 🌺
    "1f337",  # 🌷
    "1f338",  # 🌸
    "1f4ae",  # 💮
    "1f3f5-fe0f",  # 🏵️
    "1f33b",  # 🌻
    "1f33c",  # 🌼
    "1f341",  # 🍁
    "1f344",  # 🍄
    "1f331",  # 🌱
    "1f33f",  # 🌿
    "1f343",  # 🍃
    "1f340",  # 🍀
    "1fab4",  # 🪴
    "1f335",  # 🌵
    "1f334",  # 🌴
    "1f333",  # 🌳
    "1f332",  # 🌲
    "1fab9",  # 🪹
    "1fab5",  # 🪵
    "1faa8",  # 🪨
    "26c4",  # ⛄
    "1f30a",  # 🌊
    "1f32c-fe0f",  # 🌬️
    "1f300",  # 🌀
    "1f32a-fe0f",  # 🌪️
    "1f30b",  # 🌋
    "1f3d6-fe0f",  # 🏖️
    "26c5",  # ⛅
    "2601-fe0f",  # ☁️
    "1f327-fe0f",  # 🌧️
    "1f329-fe0f",  # 🌩️
    "1f4a7",  # 💧
    "2602-fe0f",  # ☂️
    "26a1",  # ⚡
    "1f308",  # 🌈
    "2604-fe0f",  # ☄️
    "1fa90",  # 🪐
    "1f30d",  # 🌍
    "1f648",  # 🙈
    "1f435",  # 🐵
    "1f981",  # 🦁
    "1f42f",  # 🐯
    "1f431",  # 🐱
    "1f436",  # 🐶
    "1f43b",  # 🐻
    "1f428",  # 🐨
    "1f43c",  # 🐼
    "1f42d",  # 🐭
    "1f430",  # 🐰
    "1f99d",  # 🦝
    "1f437",  # 🐷
    "1f984",  # 🦄
    "1f422",  # 🐢
    "1f429",  # 🐩
    "1f410",  # 🐐
    "1f98c",  # 🦌
    "1f999",  # 🦙
    "1f9a5",  # 🦥
    "1f994",  # 🦔
    "1f987",  # 🦇
    "1f989",  # 🦉
    "1f426",  # 🐦
    "1f54a-fe0f",  # 🕊️
    "1f9a9",  # 🦩
    "1f427",  # 🐧
    "1f41f",  # 🐟
    "1f99e",  # 🦞
    "1f980",  # 🦀
    "1f419",  # 🐙
    "1fab8",  # 🪸
    "1f982",  # 🦂
    "1f577-fe0f",  # 🕷️
    "1f41a",  # 🐚
    "1f40c",  # 🐌
    "1f997",  # 🦗
    "1fab2",  # 🪲
    "1fab3",  # 🪳
    "1f41d",  # 🐝
    "1f41e",  # 🐞
    "1f98b",  # 🦋
    "1f43e",  # 🐾
    "1f353",  # 🍓
    "1f352",  # 🍒
    "1f349",  # 🍉
    "1f34a",  # 🍊
    "1f96d",  # 🥭
    "1f34d",  # 🍍
    "1f34c",  # 🍌
    "1f34b",  # 🍋
    "1f348",  # 🍈
    "1f350",  # 🍐
    "1f95d",  # 🥝
    "1fad2",  # 🫒
    "1fad0",  # 🫐
    "1f347",  # 🍇
    "1f965",  # 🥥
    "1f345",  # 🍅
    "1f336-fe0f",  # 🌶️
    "1f955",  # 🥕
    "1f360",  # 🍠
    "1f9c5",  # 🧅
    "1f33d",  # 🌽
    "1f966",  # 🥦
    "1f952",  # 🥒
    "1fad1",  # 🫑
    "1f951",  # 🥑
    "1f9c4",  # 🧄
    "1f954",  # 🥔
    "1fad8",  # 🫘
    "1f330",  # 🌰
    "1f95c",  # 🥜
    "1f35e",  # 🍞
    "1fad3",  # 🫓
    "1f950",  # 🥐
    "1f96f",  # 🥯
    "1f95e",  # 🥞
    "1f373",  # 🍳
    "1f9c0",  # 🧀
    "1f969",  # 🥩
    "1f356",  # 🍖
    "1f354",  # 🍔
    "1f32d",  # 🌭
    "1f96a",  # 🥪
    "1f968",  # 🥨
    "1f35f",  # 🍟
    "1fad4",  # 🫔
    "1f32e",  # 🌮
    "1f32f",  # 🌯
    "1f959",  # 🥙
    "1f9c6",  # 🧆
    "1f958",  # 🥘
    "1f35d",  # 🍝
    "1f96b",  # 🥫
    "1fad5",  # 🫕
    "1f963",  # 🥣
    "1f957",  # 🥗
    "1f372",  # 🍲
    "1f35b",  # 🍛
    "1f35c",  # 🍜
    "1f363",  # 🍣
    "1f364",  # 🍤
    "1f35a",  # 🍚
    "1f371",  # 🍱
    "1f359",  # 🍙
    "1f358",  # 🍘
    "1f365",  # 🍥
    "1f960",  # 🥠
    "1f367",  # 🍧
    "1f368",  # 🍨
    "1f366",  # 🍦
    "1f370",  # 🍰
    "1f382",  # 🎂
    "1f9c1",  # 🧁
    "1f36c",  # 🍬
    "1f36b",  # 🍫
    "1f369",  # 🍩
    "1f36a",  # 🍪
    "1f9c2",  # 🧂
    "1f37f",  # 🍿
    "1f9cb",  # 🧋
    "1f37c",  # 🍼
    "1f375",  # 🍵
    "2615",  # ☕
    "1f9c9",  # 🧉
    "1f379",  # 🍹
    "1f37d-fe0f",  # 🍽️
    "1f6d1",  # 🛑
    "1f6a8",  # 🚨
    "1f6df",  # 🛟
    "2693",  # ⚓
    "1f697",  # 🚗
    "1f3ce-fe0f",  # 🏎️
    "1f695",  # 🚕
    "1f68c",  # 🚌
    "1f682",  # 🚂
    "1f6f8",  # 🛸
    "1f680",  # 🚀
    "2708-fe0f",  # ✈️
    "1f3a2",  # 🎢
    "1f3a1",  # 🎡
    "1f3aa",  # 🎪
    "1f3db-fe0f",  # 🏛️
    "1f3df-fe0f",  # 🏟️
    "1f3e0",  # 🏠
    "1f3d5-fe0f",  # 🏕️
    "1f307",  # 🌇
    "1f3dd-fe0f",  # 🏝️
    "1f388",  # 🎈
    "1f380",  # 🎀
    "1f381",  # 🎁
    "1faa9",  # 🪩
    "1f397-fe0f",  # 🎗️
    "1f947",  # 🥇
    "1f948",  # 🥈
    "1f949",  # 🥉
    "1f3c5",  # 🏅
    "1f396-fe0f",  # 🎖️
    "1f3c6",  # 🏆
    "26bd",  # ⚽
    "26be",  # ⚾
    "1f94e",  # 🥎
    "1f3c0",  # 🏀
    "1f3d0",  # 🏐
    "1f3c8",  # 🏈
    "1f3c9",  # 🏉
    "1f3be",  # 🎾
    "1f945",  # 🥅
    "1f3f8",  # 🏸
    "1f94d",  # 🥍
    "1f3cf",  # 🏏
    "1f3d1",  # 🏑
    "1f3d2",  # 🏒
    "1f94c",  # 🥌
    "1f6f7",  # 🛷
    "1f3bf",  # 🎿
    "26f8-fe0f",  # ⛸️
    "1f6fc",  # 🛼
    "1fa70",  # 🩰
    "1f6f9",  # 🛹
    "26f3",  # ⛳
    "1f3af",  # 🎯
    "1f3f9",  # 🏹
    "1f94f",  # 🥏
    "1fa83",  # 🪃
    "1fa81",  # 🪁
    "1f93f",  # 🤿
    "1f3bd",  # 🎽
    "1f94b",  # 🥋
    "1f94a",  # 🥊
    "1f3b1",  # 🎱
    "1f3d3",  # 🏓
    "1f3b3",  # 🎳
    "265f-fe0f",  # ♟️
    "1fa80",  # 🪀
    "1f9e9",  # 🧩
    "1f3ae",  # 🎮
    "1f3b2",  # 🎲
    "1f3b0",  # 🎰
    "1f3b4",  # 🎴
    "1f004",  # 🀄
    "1f0cf",  # 🃏
    "1f4f7",  # 📷
    "1f3a8",  # 🎨
    "1f58c-fe0f",  # 🖌️
    "1f58d-fe0f",  # 🖍️
    "1faa1",  # 🪡
    "1f9f5",  # 🧵
    "1f9f6",  # 🧶
    "1f3b9",  # 🎹
    "1f3b7",  # 🎷
    "1f3ba",  # 🎺
    "1f3b8",  # 🎸
    "1fa95",  # 🪕
    "1f3bb",  # 🎻
    "1fa98",  # 🪘
    "1f941",  # 🥁
    "1fa97",  # 🪗
    "1f3a4",  # 🎤
    "1f3a7",  # 🎧
    "1f399-fe0f",  # 🎙️
    "1f4fa",  # 📺
    "1f39e-fe0f",  # 🎞️
    "1f3ac",  # 🎬
    "1f3ad",  # 🎭
    "1f39f-fe0f",  # 🎟️
    "1f4f1",  # 📱
    "260e-fe0f",  # ☎️
    "1f50b",  # 🔋
    "1faab",  # 🪫
    "1f4be",  # 💾
    "1f4bf",  # 💿
    "1f4b8",  # 💸
    "2696-fe0f",  # ⚖️
    "1f4a1",  # 💡
    "1f9fc",  # 🧼
    "1f9e6",  # 🧦
    "1f451",  # 👑
    "1f48e",  # 💎
    "1f6e0-fe0f",  # 🛠️
    "26d3-fe0f",  # ⛓️
    "1f5d1-fe0f",  # 🗑️
    "1f58a-fe0f",  # 🖊️
    "2712-fe0f",  # ✒️
    "270f-fe0f",  # ✏️
    "1f4da",  # 📚
    "1f5c3-fe0f",  # 🗃️
    "1f4f0",  # 📰
    "1f4e3",  # 📣
    "1f50e",  # 🔎
    "1f52e",  # 🔮
    "1f9ff",  # 🧿
    "1f5dd-fe0f",  # 🗝️
    "1f512",  # 🔒
    "2648",  # ♈
    "2649",  # ♉
    "264a",  # ♊
    "264b",  # ♋
    "264c",  # ♌
    "264d",  # ♍
    "264e",  # ♎
    "264f",  # ♏
    "2650",  # ♐
    "2651",  # ♑
    "2652",  # ♒
    "2653",  # ♓
    "26ce",  # ⛎
    "2757",  # ❗
    "2753",  # ❓
    "2049-fe0f",  # ⁉️
    "1f198",  # 🆘
    "1f4f4",  # 📴
    "1f508",  # 🔈
    "26a0-fe0f",  # ⚠️
    "267b-fe0f",  # ♻️
    "2705",  # ✅
    "1f195",  # 🆕
    "1f193",  # 🆓
    "1f199",  # 🆙
    "1f197",  # 🆗
    "1f192",  # 🆒
    "1f6ae",  # 🚮
    "262e-fe0f",  # ☮️
    "262f-fe0f",  # ☯️
    "267e-fe0f",  # ♾️
    "2716-fe0f",  # ✖️
    "2795",  # ➕
    "2796",  # ➖
    "2797",  # ➗
    "27b0",  # ➰
    "27bf",  # ➿
    "3030-fe0f",  # 〰️
    "00a9-fe0f",  # ©️
    "00ae-fe0f",  # ®️
    "2122-fe0f",  # ™️
    "2660-fe0f",  # ♠️
    "1f5ef-fe0f",  # 🗯️
    "1f4ac",  # 💬
}


def emo_to_code_converter(e: str):
    res = '-'.join([(f'{ord(c):X}').lower() for c in e])
    if res not in knownSupportedEmoji:
        raise ValueError('Not Supported')
        return None
    return f'u{res}'.replace('-', '-u')


async def get_mixed(code1: str, code2: str = None) -> str:
    if code2 is None:
        code2 = f'u{random.choice(list(knownSupportedEmoji))}'.replace(
            '-', '-u')

    combined_urls = [f'{code1}/{code1}_{code2}.png',
                     f'{code2}/{code2}_{code1}.png']

    async with aiohttp.ClientSession() as cs:
        for date in knownSupportedDates:
            url = f'{emo_base_url}/{date}'
            for combined_url in combined_urls:
                async with cs.get(f'{url}/{combined_url}') as resp:
                    if resp.status == 200:
                        return resp.url

    raise ValueError('Combination not found')


class EmoListeners(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, msg: Message):
        if not (msg.author.id == 618679878144753664 and .025 > random.random()):
            return

        while True:
            try:
                result_url = await get_mixed('u1f633')
                break
            except ValueError:
                pass

        await msg.reply(result_url)


@ac.guilds(*Config.guild_ids)
class EmomixGroup(Group, name='emo'):

    @ac.command(name='自己組合', description='唉唷欸欸表情可以自己組耶')
    @ac.describe(emo1='請輸入一個表情符號，勿輸入其他多餘字元！', emo2='請輸入一個表情符號，勿輸入其他多餘字元！')
    @ac.rename(emo1='第一個表情符號', emo2='第二個表情符號')
    async def emomix(self, interation: Interaction, emo1: str, emo2: str):
        try:
            codes = [emo_to_code_converter(emo1), emo_to_code_converter(emo2)]
        except ValueError:
            await interation.response.send_message(
                f'{emo1} or {emo2} is not supported emoji.\nPlease refer to https://emojikitchen.dev/ for all combinations.',
                ephemeral=True
            )
            return

        try:
            result_url = await get_mixed(*codes)
            await interation.response.send_message(result_url)
        except ValueError:
            await interation.response.send_message(
                f'{emo1} and {emo2} cannot be combined.\nPlease refer to https://emojikitchen.dev/ for all combinations.',
                ephemeral=True
            )

    @ac.command(name='度度', description='😳😳😳')
    async def dodo_emo(self, interation: Interaction):
        await interation.response.defer()
        while True:
            try:
                result_url = await get_mixed('u1f633')
                break
            except ValueError:
                pass

        await interation.followup.send(result_url)

    @ac.command(name='ㄨㄨㄒ', description='妳好漂亮')
    async def dodo_koala(self, interation: Interaction):
        await interation.response.defer()
        while True:
            try:
                result_url = await get_mixed('u1f428')
                break
            except ValueError:
                pass

        await interation.followup.send(result_url)


async def setup(bot: Bot) -> None:
    bot.tree.add_command(EmomixGroup())
    await bot.add_cog(EmoListeners(bot))
    logger.info('EmoMix Commands Added')
