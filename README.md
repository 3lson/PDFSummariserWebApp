# PDF Summarizer Web Application

## Overview

The PDF Summarizer Web Application is a handy tool that lets users upload PDF documents or paste text to get quick summaries. The goal is to help users extract key points from long documents or text without having to read everything. The app includes a user-friendly interface and a loading indicator to enhance the experience, making it smooth and interactive.

## Context

This project uses Google’s PEGASUS model from Hugging Face’s transformer library, which is a powerful open-source NLP model designed for summarization.

## Technologies Used

- **HTML**: For structuring the web page.
- **CSS**: To style the app and make it visually appealing.
- **JavaScript**: For managing user interactions and making requests to the back-end.
- **FastAPI**: A modern Python framework used to build the API.
- **Fetch API**: For handling asynchronous requests to the back-end.
- **FormData**: To make file uploads and text submissions simple and efficient.

## Key Features

- **PDF Upload**: Users can upload a PDF, and the app summarizes its content based on the selected length (short, medium, or long). *Note: There's an issue with this feature that needs fixing*.
- **Text Input**: Users can paste text directly for summarization instead of uploading a file.
- **Loading Indicator**: While the app processes the request, a spinner shows to let users know it's working.
- **Responsive Design**: The app is designed to work smoothly on all devices, from desktops to mobile phones.

## What I Learned

Working on this project taught me several valuable lessons:

- **Front-End & Back-End Integration**: I learned how to effectively connect the front-end with a back-end API using JavaScript’s Fetch API.
- **User Experience (UX) Design**: Implementing a loading indicator taught me the importance of providing feedback to users to improve the overall experience.
- **Handling File Uploads**: I learned the best practices for handling file uploads and managing form data in a web environment.
- **Modular Code Structure**: I gained experience in organizing my code in a modular way, making it easier to maintain and scale.

## Issues Encountered and Solutions

### 1. Tokenization Errors During Summarization

**Issue**: The model initially had trouble tokenizing the input text, which caused errors during summarization. 

**Solution**: I switched to using the SentencePiece tokenizer, which handled the text better and significantly reduced errors.

### 2. Challenges with Multi-Part File Uploads in FastAPI

**Issue**: Uploading larger PDFs sometimes resulted in timeouts or incomplete reads.

**Solution**: I used FastAPI's `UploadFile` class for asynchronous file handling and adjusted the request size limits, improving file upload reliability.

### 3. CORS Errors Due to Different Domains

**Issue**: When the front-end and back-end ran on different domains, CORS (Cross-Origin Resource Sharing) errors prevented the app from working.

**Solution**: I added CORS middleware to FastAPI to allow cross-domain requests, resolving the issue.

### 4. Max Input Limit of 512 Tokens

**Issue**: The PEGASUS model only supports inputs up to 512 tokens, leading to truncated summaries for longer texts.

**Solution**: I implemented a strategy to split longer text into smaller chunks that fit within the token limit. After processing each chunk separately, I combined the results into one coherent summary.

## Future Improvements

There’s a lot of potential for making this app even better:

- **Better Error Handling**: Add more comprehensive error handling for cases like network failures or unsupported file types.
- **Improved Summary Quality**: Explore and integrate more advanced models to generate higher-quality summaries.
- **User Authentication**: Add a login feature so users can save and manage their summaries.
- **Mobile Optimization**: Further refine the design for an even better mobile experience.
- **Testing**: Implement unit and integration tests to ensure stability and reliability.
- **Deployment**: Deploy the app to a cloud platform (like Heroku or AWS) so it’s accessible to more users.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/3lson/pdf-summarizer.git
cd pdf-summarizer
```

2. Install FastAPI and other required packages: 
```bash
pip install fastapi uvicorn
```

3. Start the FastAPI server
```bash
uvicorn app:app --reload
```

4. Open your web browser and navigate to http://127.0.0.1:8000.

## Conclusion
The PDF Summarizer Web Application is a practical project that highlights the intersection of front-end and back-end development. It provides a solid foundation for further exploration into web applications, summarization techniques, and user experience design.

Feel free to explore the code, contribute, or suggest improvements!
