
# 🎓 SGPA Calculator Bot

A Telegram bot to calculate SGPA (Semester Grade Point Average) based on subject details provided by the user. This bot is live and deployed on Render!

---

## 🚀 Features

- Add subject details with credits and marks.
- Automatically calculates the SGPA based on a custom grading scale.
- Easy-to-use commands to add, compute, or restart the process.
- Hosted on Render with webhook integration for seamless operation.

---

## 📋 Commands

- **`/start`**  
  Welcomes the user and provides instructions on how to use the bot.

- **`/collect_subject_details <subject_name> <credits> <marks_out_of_100>`**  
  Adds details of a subject, including its name, credits, and marks obtained.

  **Example:**  
  `/collect_subject_details Math 4 85`

- **`/calculate_sgpa`**  
  Computes the SGPA based on the entered subject details and grading scale.

- **`/cancel`**  
  Cancels the current session and resets all subject data.

---

## 🛠️ Deployment

This bot is deployed on Render and uses webhook integration for communication with Telegram.

### Steps to Deploy:

1. Clone the repository:
   ```bash
   git clone https://github.com/zelssorathiya2615/NUV-SGPA-Calculator.git
   cd NUV-SGPA-Calculator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - `TELEGRAM_TOKEN`: Your Telegram bot token.
   - `WEBHOOK_URL`: The webhook URL where the bot is hosted.

4. Run locally for testing:
   ```bash
   python bot.py
   ```

5. Deploy using Render or any hosting platform of your choice.

---

## 📊 Grading Scale

| Marks (%) | Grade  | Grade Points (GP) |
|-----------|--------|-------------------|
| 90 - 100  | A+     | 100% of Credits   |
| 80 - 89   | A      | 90% of Credits    |
| 71 - 79   | A-     | 80% of Credits    |
| 61 - 70   | B+     | 70% of Credits    |
| 56 - 60   | B      | 60% of Credits    |
| 50 - 55   | B-     | 50% of Credits    |
| 40 - 49   | C      | 40% of Credits    |
| Below 40  | NI     | 0% of Credits     |

---

## 🌐 Example Interaction

**User:**  
`/start`

**Bot:**  
```
🎓 Welcome to the SGPA Calculator Bot!

Here's how I can help you:
1️⃣ Enter subject details one by one.
2️⃣ I will calculate your SGPA based on the data.

👉 Input Format:
Use the command:
/collect_subject_details <subject_name> <credits> <marks_out_of_100>

📝 Example:
/collect_subject_details Math 4 85

📌 Type /calculate_sgpa to compute your SGPA after entering all subjects.
Type /cancel at any time to restart.
```

**User:**  
`/collect_subject_details Math 4 85`

**Bot:**  
```
✅ Subject Added Successfully:

📚 **Subject Details:**

Subject         Credits  Marks    Grade  Grade Points 
--------------------------------------------------
Math            4.00     85.00    A      3.60

Add another subject or type `/calculate_sgpa` to calculate your SGPA.
```

**User:**  
`/calculate_sgpa`

**Bot:**  
```
📚 **Subject Details:**

Subject         Credits  Marks    Grade  Grade Points 
--------------------------------------------------
Math            4.00     85.00    A      3.60

🏆 **Your SGPA:** 9.00
🎓 Formula: Total Earned Grade Points ÷ Total Credits
```

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b my-new-feature`.
3. Commit your changes: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin my-new-feature`.
5. Submit a pull request.

---

## 🛡️ Security

If you discover any security-related issues, please report them via email at `sorathiyazels@gmail.com`.

---

## Contact

For any inquiries, feedback, or support, feel free to reach out to me via my portfolio website:

[Zels Sorathiya](https://zelssorathiya2615.github.io/Zels-Sorathiya/)


---

### ⭐ Show your support

Give a ⭐️ if you found this project useful!
