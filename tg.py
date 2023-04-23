from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
import asyncio
import pandas as pd

async def main():

    seenUsers = []

    # Input your own API ID and API hash
    api_id = '24181282'
    api_hash = '9d0e6ee58a2b249643737d97e55c843a'

    # Input the title of the specific chat you want to fetch bios from
    target_chat_title = 'Avalanche Summit (Official)'


    # Create an empty DataFrame with columns 'Username' and 'Bio'
    user_data = pd.DataFrame(columns=['Username', 'Bio'])

    async with TelegramClient('anon', api_id, api_hash) as client:

        # For each dialog
        async for dialog in client.iter_dialogs(limit=None):

            # Check if the chat title matches the target chat title
            if dialog.name == target_chat_title:

                # For each participant
                async for user in client.iter_participants(entity=dialog, limit=None, aggressive=True):

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
    user_data.to_excel('Avalanche_Summit.xlsx', index=False)

asyncio.run(main())
