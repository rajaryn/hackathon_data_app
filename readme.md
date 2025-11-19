
# Hackathon Participation Tracker

A Python-based web application designed to track student participation in hackathons. This tool allows users to register their teams and tracks participation details, utilizing Google Sheets as a real-time database.

## Features

- **Student Registration:** Simple form for students to input their details.
- **Google Sheets Backend:** Automatically saves all data to a Google Sheet for easy management and export.
- **Real-time Updates:** Data is reflected instantly in the connected sheet.
- **Responsive Design:** Works on mobile and desktop.
- **Vercel Ready:** Configured for serverless deployment on Vercel.

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** Google Sheets API (`gspread`,`google-auth`)
- **Frontend:** HTML, CSS (Jinja2 templates)
- **Hosting:** Vercel

## ⚙️ Local Setup

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/rajaryn/hackathon_participation_app.git](https://github.com/rajaryn/hackathon_participation_app.git)
cd hackathon_participation_app
````

### 2\. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Google Sheets Configuration

To make the backend work, you need a Google Service Account:

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project and enable the **Google Sheets API** and **Google Drive API**.
3.  Create a **Service Account**, generate a JSON key, and download it.
4.  **Important:** Share your Google Sheet with the `client_email` found in your JSON key file (give "Editor" access).
5.  Rename your JSON key file to `credentials.json` and place it in the root directory (ensure this file is in your `.gitignore`\!).

### 5\. Run the App

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## 🚀 Deployment on Vercel

This project includes a `vercel.json` configuration for easy deployment.

1.  Push your code to GitHub.
2.  Go to [Vercel](https://vercel.com/) and import your repository.
3.  **Environment Variables:** If you are using Google Sheets, you cannot upload `credentials.json` to GitHub. You must add the contents of that JSON file as Environment Variables in Vercel (e.g., `GOOGLE_CREDENTIALS`).
4.  Click **Deploy**.

## 📂 Project Structure

```
hackathon_participation_app/
│
├── templates/           # HTML files
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel configuration
└── README.md            # Project documentation
```

## 🤝 Contributing

Contributions are welcome\! Please open an issue or submit a pull request.

1.  Fork the repo.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

-----

*Built by Raj Aryan*

```

### Key things to check before you push:
1.  **`credentials.json`:** If you are using the Google Sheets API, make sure `credentials.json` is inside your `.gitignore` file so you don't accidentally publish your API keys to GitHub.
2.  **Requirements:** Make sure your `requirements.txt` includes `gspread` and `oauth2client` if you are using the Sheets integration.
```