# Socratic Math Tutor

A modern web application that provides Socratic-style math tutoring using AI. The tutor asks guiding questions to help students discover solutions on their own, following the Socratic method of teaching.

## Features

- 🤖 AI-powered Socratic tutoring
- 💬 Modern chat interface
- 📱 Responsive design
- 🎯 Category-based responses
- ⚡ Real-time interaction
- 🔄 Conversation history
- 🎨 Clean, modern UI

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI**: OpenAI GPT-3.5 Turbo

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/socratic-app.git
cd socratic-app
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

5. Run the application:

```bash
uvicorn main:app --reload
```

6. Open your browser and navigate to:

```
http://localhost:8000
```

## Response Categories

The tutor categorizes each response into one of these types:

1. **General Interaction**: For greetings and non-math related inputs
2. **Conceptual Understanding**: For misunderstandings of mathematical concepts
3. **Procedural Difficulty**: For struggles with mathematical procedures
4. **Math Anxiety**: For emotional barriers or fear of math
5. **Problem Solving Strategy**: For help with approaching problems
6. **Real World Connection**: For questions about math's relevance

## Development

- Backend API is built with FastAPI and serves both the API endpoints and static files
- Frontend is built with vanilla JavaScript for lightweight performance
- Modern CSS with variables for easy theming
- Responsive design works on all device sizes

## API Endpoints

- `GET /`: Serves the main application
- `POST /api/chat`: Handles chat messages
  - Request body:
    ```json
    {
        "messages": [
            {
                "role": "user"|"assistant",
                "content": "string",
                "category": "string" (optional)
            }
        ],
        "new_message": "string"
    }
    ```
  - Response:
    ```json
    {
      "response": "string",
      "category": "string"
    }
    ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
