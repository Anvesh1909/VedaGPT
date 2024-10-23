
---

# VedaGPT

Offline Large Language Models with Real-Time Communication

## 📖 About

Welcome to VedaGPT, your smart text companion! This project, developed during an internship, is designed to work offline, offering powerful text-based features like PDF summarization, answering questions, and generating content. VedaGPT uses secure offline models, making it ideal for users who need privacy and uninterrupted access. Whether you're a student, researcher, or just someone curious about knowledge, VedaGPT helps you understand and create content easily.

## ✨ Features

- **PDF Summarization:** Quickly summarize large PDF files into short, clear summaries for easier understanding.
- **Question Answering:** Get precise answers to your questions from large text documents without wasting time.
- **Text Generation:** Create meaningful and relevant text based on your input, helping with writing and idea generation.
- **Offline Security:** Since VedaGPT runs completely offline, your data is secure, and no internet connection is needed to use the models.
- **Real-Time Communication:** Experience real-time responses using Django Channels for smooth, instant interaction.
- **Easy-to-Use Interface:** Enjoy a simple and user-friendly design that makes navigation and interaction seamless.

## 🚀 Technologies Used

- **Python:** Core programming language for building the functionalities.
- **Hugging Face:** Using their transformer models offline to enable text processing.
- **ChromaDB:** Helps with extracting and summarizing content from PDFs.
- **Django:** Backend framework for building the web platform.
- **Channels:** Used to implement real-time communication within the application.
- **Bootstrap:** Provides a responsive and clean design for the frontend.

## 🛠 Installation

To get VedaGPT running on your local machine, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/vedagpt.git
cd vedagpt
```

### 2. Create a Virtual Environment

Set up a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install all required packages listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set Up Django

Apply migrations to initialize the database:

```bash
python manage.py migrate
```

### 5. Run the Server

Start the Django development server:

```bash
python manage.py runserver
```

The app will be accessible at `http://127.0.0.1:8000`.

## 🧩 Usage

After starting the application, you can use the following features:

- **PDF Summarization:** Upload a PDF and get a summarized version in seconds.
- **Question Answering:** Ask a question, and VedaGPT will search through the uploaded content to give a precise answer.
- **Text Generation:** Type in a prompt, and VedaGPT will generate meaningful text based on it.

## 💡 Contributing

Interested in contributing to VedaGPT? Here's how you can help:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Make your changes (`git commit -m "Add new feature"`).
4. Push the branch (`git push origin feature-branch`).
5. Open a pull request for review.

---
