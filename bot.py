from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Constants
TOKEN = "8191348054:AAEcRjlqf5U0hbQvKU4KOfBEOxVw84Y6IV4"
WEBHOOK_URL = "https://nuv-sgpa-calculator.onrender.com"

# Global dictionary to store user data
user_data = {}

# Grading scale based on marks
def get_earned_grade_points(marks, credits):
    if marks >= 90:
        grade_points = credits * 1
        grade = 'A+'
    elif marks >= 80:
        grade_points = credits * 0.9
        grade = 'A'
    elif marks >= 71:
        grade_points = credits * 0.8
        grade = 'A-'
    elif marks >= 61:
        grade_points = credits * 0.7
        grade = 'B+'
    elif marks >= 56:
        grade_points = credits * 0.6
        grade = 'B'
    elif marks >= 50:
        grade_points = credits * 0.5
        grade = 'B-'
    elif marks >= 40:
        grade_points = credits * 0.4
        grade = 'C'
    else:
        grade_points = 0
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

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = []
    await update.message.reply_text(
        "🎓 Welcome to the SGPA Calculator Bot!\n\n"
        "Use `/collect_subject_details <subject_name> <credits> <marks_out_of_100>` to add subject details.\n"
        "Type `/calculate_sgpa` to compute your SGPA.\n"
        "Type `/cancel` to restart."
    )

async def collect_subject_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if len(context.args) != 3:
        await update.message.reply_text("⚠️ Incorrect input format. Use `/collect_subject_details <subject_name> <credits> <marks_out_of_100>`.")
        return

    subject_name = context.args[0]
    try:
        credits = float(context.args[1])
        marks = float(context.args[2])

        grade_points, grade = get_earned_grade_points(marks, credits)
        user_data[user_id].append({
            'subject': subject_name,
            'credits': credits,
            'marks': marks,
            'grade': grade,
            'earned_grade_points': grade_points
        })

        table_message = format_subject_table(user_data[user_id])
        await update.message.reply_text(f"✅ Subject Added:\n\n{table_message}\n\nAdd more or type `/calculate_sgpa`.")
    except ValueError:
        await update.message.reply_text("⚠️ Credits and marks must be numeric.")

async def calculate_sgpa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data or not user_data[user_id]:
        await update.message.reply_text("⚠️ No subjects added. Use `/collect_subject_details` first.")
        return

    total_grade_points = sum(s['earned_grade_points'] for s in user_data[user_id])
    total_credits = sum(s['credits'] for s in user_data[user_id])
    sgpa = (total_grade_points / total_credits if total_credits else 0) * 10

    table_message = format_subject_table(user_data[user_id])
    await update.message.reply_text(f"{table_message}\n\n🏆 **Your SGPA:** {sgpa:.2f}")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = []
    await update.message.reply_text("🔄 Process canceled. Use /start to restart.")

# Main function
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("collect_subject_details", collect_subject_details))
    application.add_handler(CommandHandler("calculate_sgpa", calculate_sgpa))
    application.add_handler(CommandHandler("cancel", cancel))

    # Set webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=8443,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )
    print("Webhook configured and bot is running...")

if __name__ == "__main__":
    main()
