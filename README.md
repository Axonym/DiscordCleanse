# DiscordCleanse

## ⚠️ Warning! Use of this tool might result in account termination<sup>[1](https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots)</sup> <br> Use at your own risk.
## How to use?
1. Request Discord Data package using this [guide](https://support.discord.com/hc/en-us/articles/360004957991-Your-Discord-Data-Package)
2. Once you have the package unzip it
3. Install the required libraries by running the following command
   `pip install requests customtkinter`
4. Download the [discordcleanse.py](https://raw.githubusercontent.com/Axonym/discordcleanse/main/discordcleanse.py)
5. Run the file and locate the package folder and select it
6. Get authorization cookie value and paste it. ([Guide on how to get it](https://www.geeksforgeeks.org/how-to-get-discord-token/))
7. Paste the channel ID you want to delete messages from
8. Set delay and wait for it to finish

## 📝 How it works
The tool reads message IDs from messages file by using the given channel ID folder and adds those message IDs to a list. It then makes requests to specific API endpoints with those message IDs. It goes through the list  until there are no more message IDs.

## ✅ Pros
- Doesn't have to query message IDs using search -> faster deletion process(?)
- Doesn't have to have Discord opened (assuming you have auth token saved and know the correct message IDs)
## ❌ Cons
- You can only delete messages in the package. You can't delete messages sent after obtaining the package.
- Requires obtaining auth token
- Requires knowledge how to install pip packages

## 🔒 Security
You as a user have to trust the developer that there isn't any malicious code in the program. Thus making this program open-source ensures that you can take a look at the code at any time to ensure nothing malicious is happening in the code. **The program will only do requests to Discord API and no elsewhere.**
