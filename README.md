
# VedaGPT

Unlocking the Power of Offline Large Language Models

## 📖 About

Welcome to VedaGPT, your intelligent text companion! VedaGPT leverages the power of offline Large Language Models (LLMs) to provide a plethora of text-related functionalities, including PDF summarization, question answering, and text generation. Whether you're a student, researcher, or knowledge enthusiast, VedaGPT is your go-to tool for extracting insights and generating content effortlessly.

## ✨ Features

- **PDF Summarization:** Summarize lengthy PDF documents into concise and informative summaries, enabling quick understanding and analysis.
- **Question Answering:** Seamlessly extract answers to your questions from vast textual sources, empowering efficient information retrieval.
- **Text Generation:** Generate coherent and contextually relevant text based on user prompts, facilitating content creation and idea generation.
- **Offline Capabilities:** Enjoy uninterrupted access to LLM-powered features without reliance on internet connectivity, ensuring privacy and accessibility.
- **Intuitive Interface:** Navigate through VedaGPT's user-friendly interface, designed for ease of use and seamless interaction.

## 🚀 Technologies Used

- **Python:** The primary programming language for implementing VedaGPT's functionalities.
- **Hugging Face:** Utilizes Hugging Face's transformer models for offline LLM capabilities.
- **ChromaDB:** Efficient PDF parsing and text extraction.
- **Django:** Framework for building the web application.
- **Bootstrap:** For responsive and visually appealing user interfaces.

## 🛠 Installation

To run the VedaGPT project locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/vedagpt.git
cd vedagpt
```

### 2. Set Up a Virtual Environment

Create a virtual environment to isolate the dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install the Dependencies

Install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set Up the Django Application

Before running the Django application, apply the migrations:

```bash
python manage.py migrate
```

### 5. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000`.

## 🧩 Usage

Once the application is running:

- **PDF Summarization:** Upload a PDF file, and VedaGPT will generate a concise summary.
- **Question Answering:** Enter a question, and VedaGPT will search the uploaded documents for relevant answers.
- **Text Generation:** Provide a prompt, and VedaGPT will generate a coherent response based on the provided context.

## 💡 Contributing

We welcome contributions! To contribute to VedaGPT:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
