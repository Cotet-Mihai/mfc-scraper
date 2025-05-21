import asyncio
from core.scrap import ProfileInfo
from datetime import datetime

curent_date = datetime.now().strftime("%d-%m-%Y")

if __name__ == '__main__':
    async def main():
        profile = ProfileInfo('PatyBlack', 'prietenabianca123', curent_date)
        await profile.get_information()

        print(profile.tokens)

    asyncio.run(main())