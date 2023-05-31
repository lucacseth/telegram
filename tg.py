from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
import asyncio
import pandas as pd
from tqdm.asyncio import tqdm

async def main():

    seenUsers = []

    # Input your own API ID and API hash
    api_id = ''
    api_hash = ''

    # Input the title of the specific chat you want to fetch bios from
    target_chat_title = 'EnterName'

    # Create an empty DataFrame with columns 'Username' and 'Bio'
    user_data = pd.DataFrame(columns=['Username', 'Bio'])

    async with TelegramClient('anon', api_id, api_hash) as client:

        # Get the number of dialogs
        dialogs_count = len(await client.get_dialogs())

        # For each dialog
        async for dialog in tqdm(client.iter_dialogs(limit=None), total=dialogs_count, desc="Processing dialogs"):

            # Check if the chat title matches the target chat title
            if dialog.name == target_chat_title:

                # Get the number of participants
                participants_count = len(await client.get_participants(dialog))

                # For each participant
                async for user in tqdm(client.iter_participants(entity=dialog, limit=None, aggressive=True), total=participants_count, desc="Processing participants"):

                    # Prevent double
                    if user.username in seenUsers:
                        continue

                    if user.username:
                        seenUsers.append(user.username)
                    else:
                        continue

                    # Get full user
                    fullUser = await client(GetFullUserRequest(user))

                    # Log description
                    if fullUser.full_user.about:

                        # Add user information to the DataFrame
                        user_data.loc[len(user_data)] = [user.username, fullUser.full_user.about]

    # Sort the DataFrame by Username and Bio columns
    user_data = user_data.sort_values(by=['Username', 'Bio'])

    # Export the DataFrame to an Excel file
    user_data.to_excel('EnterName.xlsx', index=False)

asyncio.run(main())
