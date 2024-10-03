import random
import time
from utils.core import logger
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
import asyncio
from urllib.parse import unquote, quote
from data import config
import aiohttp
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector


class CatsGang:
    def __init__(self, thread: int, session_name: str, phone_number: str, proxy: [str, None]):
        self.account = session_name + '.session'
        self.thread = thread
        self.ref = random.choice(config.REFS)
        self.proxy = f"{config.PROXY['TYPE']['REQUESTS']}://{proxy}" if proxy is not None else None
        connector = ProxyConnector.from_url(self.proxy) if proxy else aiohttp.TCPConnector(verify_ssl=False)

        if proxy:
            proxy = {
                "scheme": config.PROXY['TYPE']['TG'],
                "hostname": proxy.split(":")[1].split("@")[1],
                "port": int(proxy.split(":")[2]),
                "username": proxy.split(":")[0],
                "password": proxy.split(":")[1].split("@")[0]
            }

        self.client = Client(
            name=session_name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            workdir=config.WORKDIR,
            proxy=proxy,
            lang_code='ru'
        )

        headers = {
            'User-Agent': UserAgent(os='android', browsers='chrome').random,
        }
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=connector)

    async def stats(self):
        await self.login()

        user = await self.user()
        # balance = str(user.get('totalRewards'))
        referral_link = f"https://t.me/catsgang_bot/join?startapp={user.get('referrerCode')}"

        r = await (await self.session.get('https://api.catshouse.club/user')).json()
        balance = r.get('totalRewards')

        await self.logout()

        await self.client.connect()
        me = await self.client.get_me()
        phone_number, name = "'" + me.phone_number, f"{me.first_name} {me.last_name if me.last_name is not None else ''}"
        await self.client.disconnect()

        proxy = self.proxy.replace('http://', "") if self.proxy is not None else '-'

        return [phone_number, name, balance, referral_link, proxy]

    async def user(self):
        resp = await self.session.get('https://cats-backend-cxblew-prod.up.railway.app/user')
        return await resp.json()

    async def logout(self):
        await self.session.close()

    async def check_task(self, task_id: int):
        try:
            resp = await self.session.post(f'https://api.catshouse.club/tasks/{task_id}/check')
            return (await resp.json()).get('completed')
        except:
            return False
        
    async def subs_for_tasks(self):
        try:
            await self.client.connect()
            await self.client.join_chat('seedupdates')
            await asyncio.sleep(1)
            await self.client.join_chat('starsmajor')
            await asyncio.sleep(2)
            await self.client.join_chat('okx_ru')
            await asyncio.sleep(1)
            await self.client.join_chat('memeficlub')
            await asyncio.sleep(1)
            await self.client.join_chat('baks_ton')
            await asyncio.sleep(1)
            await self.client.join_chat('activitylauncher_offical')
            await asyncio.sleep(2)
            await self.client.join_chat('Cats_housewtf')
            await asyncio.sleep(1)
            await self.client.join_chat('baks_ton')
            await self.client.disconnect()
        except:
            logger.error(f"Cats | Thread {self.thread} | {self.account} | error")

    async def complete_task(self, task_id: int, task):
        
        try:
            if task['type'] == 'YOUTUBE_WATCH':
                try:
                    if task['id'] == 141:
                        json_data = {}
                        response = await self.session.post(f'https://api.catshouse.club/tasks/141/complete?answer=dildo', json=json_data)
                        resp = await response.json()
                        if resp['success']:
                            logger.success(f"do_task | Thread {self.thread} | {self.account} | Claim task (dildo) YOUTUBE")
                        else:
                            logger.error(f"do_task | Thread {self.thread} | {self.account} | task (dildo) YOUTUBE {resp}")
                            
                    elif task['id'] == 153:
                        json_data = {}
                        response = await self.session.post(f'https://api.catshouse.club/tasks/153/complete?answer=ABSTRACT', json=json_data)
                        resp = await response.json()
                        if resp['success']:
                            logger.success(f"do_task | Thread {self.thread} | {self.account} | Claim task (ABSTRACT) YOUTUBE")
                        else:
                            logger.error(f"do_task | Thread {self.thread} | {self.account} | task (ABSTRACT) YOUTUBE {resp}")
                        
                    elif task['id'] == 146:
                        json_data = {}
                        response = await self.session.post(f'https://api.catshouse.club/tasks/146/complete?answer=dip', json=json_data)
                        resp = await response.json()
                        if resp['success']:
                            logger.success(f"do_task | Thread {self.thread} | {self.account} | Claim task (dip) YOUTUBE")
                        else:
                            logger.error(f"do_task | Thread {self.thread} | {self.account} | task (dip) YOUTUBE {resp}")
                    
                    elif task['id'] == 148:
                        json_data = {}
                        response = await self.session.post(f'https://api.catshouse.club/tasks/148/complete?answer=AIRNODE', json=json_data)
                        resp = await response.json()
                        if resp['success']:
                            logger.success(f"do_task | Thread {self.thread} | {self.account} | Claim task (AIRNODE) YOUTUBE")
                        else:
                            logger.error(f"do_task | Thread {self.thread} | {self.account} | task (AIRNODE) YOUTUBE {resp}")
                    
                    elif task['id'] == 149:
                        json_data = {}
                        response = await self.session.post(f'https://api.catshouse.club/tasks/149/complete?answer=WEI', json=json_data)
                        resp = await response.json()
                        if resp['success']:
                            logger.success(f"do_task | Thread {self.thread} | {self.account} | Claim task (WEI) YOUTUBE")
                        else:
                            logger.error(f"do_task | Thread {self.thread} | {self.account} | task (WEI) YOUTUBE {resp}")
                except Exception as err:
                    logger.error(f"tasks | Thread {self.thread} | {self.account} | {err} TASK_ID : {task['id']}")      
            else:
                if '?' in task['params']['linkUrl']:
                    app = task['params']['linkUrl'].split('?')[0].split('/')[3]
                    short = task['params']['linkUrl'].split('?')[1].split('=')[0]
                    ref = task['params']['linkUrl'].split('?')[1].split('=')[1]
                    await self.join_app_task(app,short,ref)
                    await asyncio.sleep(1)
                try:
                    json_data = {}
                    response = await self.session.post(f'https://api.catshouse.club/tasks/{task["id"]}/complete', json=json_data)
                    resp = await response.json()
                    if resp['success']:
                        logger.success(f"do_task | Thread {self.thread} | {self.account} | Claim task {task['title']}")
                    else:
                        logger.error(f"do_task | Thread {self.thread} | {self.account} | task {task['id']} {resp}")
                except Exception as err:
                    logger.error(f"tasks | Thread {self.thread} | {self.account} | {err} TASK_ID : {task['id']}")
            resp = await self.session.post(f'https://api.catshouse.club/tasks/{task_id}/complete')
            return (await resp.json()).get('success')
        except:
            logger.error(f"Thread {self.thread} | {self.account} | Can't complete task {task_id}, error")
            return False
        
    async def change_Nickname(self):
        try:
            await self.client.connect()
            user = await self.client.get_me()
            
            if '🐈‍⬛' not in user.first_name:
                await self.client.update_profile(first_name=f"{user.first_name}🐈‍⬛")
            
            await self.client.disconnect()
        except:
            return None
        
    async def nickname_task(self):
        try:
            resp = await self.session.post("https://api.catshouse.club/tasks/104/check")
            resp = await self.session.post("https://api.catshouse.club/tasks/104/complete")

            logger.success(f"Thread {self.thread} | {self.account} | Complete task «Change nickname» + 300")
        except:
            logger.warning(f"Thread {self.thread} | {self.account} | Couldn't complete task «Change nickname»")
        

    async def get_tasks(self):
        status = False
        while status == False:
            resp = await self.session.get('https://api.catshouse.club/tasks/user?group=cats')
            if resp.status != 200:    
                logger.warning(f"Thread {self.thread} | {self.account} | Couldn't get task list, error {resp.status}, trying again...")
                await asyncio.sleep(2)
            else:
                status = True
        return (await resp.json()).get('tasks')

    async def register(self):
        resp = await self.session.post(f'https://api.catshouse.club/user/create?referral_code={self.ref}')
        return resp.status == 200

    async def login(self):
        await asyncio.sleep(random.uniform(*config.DELAYS['ACCOUNT']))
        self.ref = self.ref
        query = await self.get_tg_web_data()

        if query is None:
            logger.error(f"Thread {self.thread} | {self.account} | Session {self.account} invalid")
            await self.logout()
            return None, None

        self.session.headers['Authorization'] = 'tma ' + query

        r = await (await self.session.get('https://api.catshouse.club/user')).text()
        if r == '{"name":"Error","message":"User was not found"}':
            if await self.register():
                logger.success(f"Thread {self.thread} | {self.account} | Register")

    async def join_app_task(self, app, short, ref):
        try:
            await self.client.connect()

            web_view = await self.client.invoke(RequestAppWebView(
                peer=await self.client.resolve_peer(app),
                app=InputBotAppShortName(bot_id=await self.client.resolve_peer(app), short_name=short),
                platform='android',
                write_allowed=True,
                start_param=ref
            ))
            await self.client.disconnect()
        except:
            return None

    async def get_tg_web_data(self):
        try:
            await self.client.connect()

            web_view = await self.client.invoke(RequestAppWebView(
                peer=await self.client.resolve_peer('catsgang_bot'),
                app=InputBotAppShortName(bot_id=await self.client.resolve_peer('catsgang_bot'), short_name="join"),
                platform='android',
                write_allowed=True,
                start_param=self.ref
            ))
            await self.client.disconnect()

            auth_url = web_view.url
            query = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
            return query

        except:
            return None
