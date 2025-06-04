from telegram.ext import Updater, CommandHandler
import requests
import os

TOKEN = "7744035483:AAFYnyfwhN74kSveZBl7nXKjGgXKYWtnbw0"
port = int(os.environ.get('PORT', 8080))

def start(update, context):
    update.message.reply_text("Use /getemail to start")

def help(update, context):
    message = """
📌 TempMail Bot Help Guide

Main Commands:
📧 /getemail 
• Creates new temporary email
• Valid for 7 days
• Use for signups & testing

📨 /checkmails
• Shows all received emails
• Displays sender & content
• Updates in real-time

Other Commands:
🗑️ /clear 
• Resets current email
• Use before making new one

ℹ️ /about
• Shows bot information
• Contact details

Tips:
• Create email with /getemail
• Wait 10-15 seconds for emails
• Use /clear if you need new email

Need Help?
Contact: @packoa
"""
    update.message.reply_text(message)

def about(update, context):
    update.message.reply_text("TempMail Bot")

def clear(update, context):
    if 'inbox_id' in context.user_data:
        context.user_data.clear()
        update.message.reply_text("Email cleared")
    else:
        update.message.reply_text("No email")

def getemail(update, context):
    headers = {'x-api-key': "60a4ccffe457daa97f1fe94c0fe31786dc90946bbb8c3c981de3818ffec0c775", 'Content-Type': 'application/json'}
    response = requests.post("https://api.mailslurp.com/inboxes", headers=headers)
    if response.status_code == 201:
        data = response.json()
        email = data['emailAddress']
        inbox_id = data['id']
        context.user_data['inbox_id'] = inbox_id
        context.user_data['email'] = email
        update.message.reply_text("Your email: " + email)
    else:
        update.message.reply_text("Error")

def checkmails(update, context):
    if 'inbox_id' not in context.user_data:
        update.message.reply_text("Use /getemail first")
        return
    headers = {'x-api-key': "60a4ccffe457daa97f1fe94c0fe31786dc90946bbb8c3c981de3818ffec0c775", 'Content-Type': 'application/json'}
    response = requests.get("https://api.mailslurp.com/inboxes/" + context.user_data['inbox_id'] + "/emails", headers=headers)
    if response.status_code == 200:
        emails = response.json()
        if not emails:
            update.message.reply_text("No emails")
            return
        for email in emails:
            r = requests.get("https://api.mailslurp.com/emails/" + email['id'], headers=headers)
            if r.status_code == 200:
                full = r.json()
                update.message.reply_text("From: " + full['from'])
                update.message.reply_text("Subject: " + full['subject'])
                update.message.reply_text("Body: " + full['body'])
    else:
        update.message.reply_text("Error")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("getemail", getemail))
    dp.add_handler(CommandHandler("checkmails", checkmails))
    dp.add_handler(CommandHandler("clear", clear))
    
    # Add webhook mode for Render
    updater.start_webhook(listen="0.0.0.0",
                          port=port,
                          url_path=TOKEN,
                          webhook_url="https://your-app-name.onrender.com/" + TOKEN)
    print("Bot running")
    updater.idle()

if __name__ == "__main__":
    main()
