from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    # Run both Flask app and the Telegram bot
    from threading import Thread

    def run_bot():
        main()  # Start your Telegram bot (defined in your script)

    # Start Flask server in a thread
    Thread(target=run_bot).start()

    # Bind to the PORT environment variable provided by Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



# Replace with your bot token
TOKEN = "8191348054:AAEcRjlqf5U0hbQvKU4KOfBEOxVw84Y6IV4"

# Global dictionary to store user data
user_data = {}

# Grading scale based on marks
def get_earned_grade_points(marks, credits):
    if marks >= 90:
        grade_points = credits * 1  # A+ -> 100% of credits
        grade = 'A+'
    elif marks >= 80:
        grade_points = credits * 0.9  # A -> 90% of credits
        grade = 'A'
    elif marks >= 71:
        grade_points = credits * 0.8  # A- -> 80% of credits
        grade = 'A-'
    elif marks >= 61:
        grade_points = credits * 0.7  # B+ -> 70% of credits
        grade = 'B+'
    elif marks >= 56:
        grade_points = credits * 0.6  # B -> 60% of credits
        grade = 'B'
    elif marks >= 50:
        grade_points = credits * 0.5  # B- -> 50% of credits
        grade = 'B-'
    elif marks >= 40:
        grade_points = credits * 0.4  # C -> 40% of credits
        grade = 'C'
    else:
        grade_points = 0  # NI -> No Earned Grade Points
        grade = 'NI'
    return grade_points, grade

# Function to format data into a table
def format_subject_table(subjects):
    table_header = "📚 **Subject Details:**\n\n"
    table_header += f"{'Subject':<15} {'Credits':<8} {'Marks':<8} {'Grade':<6} {'Grade Points':<12}\n"
    table_header += "-" * 50 + "\n"
    table_rows = [
        f"{s['subject']:<15} {s['credits']:<8.2f} {s['marks']:<8.2f} {s['grade']:<6} {s['earned_grade_points']:<12.2f}"
        for s in subjects
    ]
    return table_header + "\n".join(table_rows)

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = []  # Reset user data on start
    await update.message.reply_text(
        "🎓 Welcome to the SGPA Calculator Bot!\n\n"
        "Here's how I can help you:\n"
        "1️⃣ Enter subject details one by one.\n"
        "2️⃣ I will calculate your SGPA based on the data.\n\n"
        "👉 **Input Format:**\n"
        "Use the command:\n"
        "`/collect_subject_details <subject_name> <credits> <marks_out_of_100>`\n\n"
        "📝 **Example:**\n"
        "`/collect_subject_details Math 4 85`\n\n"
        "📌 Type `/calculate_sgpa` to compute your SGPA after entering all subjects.\n"
        "Type `/cancel` at any time to restart."
    )

# Handler to collect subject details (name, credits, marks)
async def collect_subject_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if len(context.args) != 3:
        await update.message.reply_text(
            "⚠️ Incorrect input format. Please enter the details like this:\n"
            "`/collect_subject_details <subject_name> <credits> <marks_out_of_100>`\n\n"
            "📝 **Example:**\n"
            "`/collect_subject_details Math 4 85`"
        )
        return

    subject_name = context.args[0]
    try:
        credits = float(context.args[1])
        marks = float(context.args[2])

        # Get Earned Grade Points based on marks and credits
        grade_points, grade = get_earned_grade_points(marks, credits)

        # Store the subject data for the user
        user_data[user_id].append({
            'subject': subject_name,
            'credits': credits,
            'marks': marks,
            'grade': grade,
            'earned_grade_points': grade_points
        })

        # Create and send the updated table
        table_message = format_subject_table(user_data[user_id])
        await update.message.reply_text(
            f"✅ Subject Added Successfully:\n\n{table_message}\n\n"
            "Add another subject or type `/calculate_sgpa` to calculate your SGPA."
        )

    except ValueError:
        await update.message.reply_text(
            "⚠️ Please ensure credits and marks are numeric values. Try again."
        )

# Handler to calculate SGPA
async def calculate_sgpa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_data or not user_data[user_id]:
        await update.message.reply_text(
            "⚠️ No subjects added yet. Use `/collect_subject_details` to add subjects."
        )
        return

    total_grade_points = 0
    total_credits = 0

    # Calculate total earned grade points and total credits
    for subject in user_data[user_id]:
        total_grade_points += subject['earned_grade_points']
        total_credits += subject['credits']

    # Calculate SGPA
    sgpa = (total_grade_points / total_credits if total_credits else 0)*10

    # Create and send the final table with SGPA
    table_message = format_subject_table(user_data[user_id])
    await update.message.reply_text(
        f"{table_message}\n\n🏆 **Your SGPA:** {sgpa:.2f}\n"
        "🎓 Formula: Total Earned Grade Points ÷ Total Credits"
    )

# Handler to cancel the subject entry process
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data:
        user_data[user_id] = []  # Clear user data if cancel is requested
    await update.message.reply_text(
        "🔄 Process canceled. You can start again by typing /start."
    )

# Main function
def main():
    # Initialize the application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("collect_subject_details", collect_subject_details))
    application.add_handler(CommandHandler("calculate_sgpa", calculate_sgpa))
    application.add_handler(CommandHandler("cancel", cancel))

    # Start the bot
    print("SGPA Calculation Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
