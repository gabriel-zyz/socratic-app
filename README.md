# Socratic Math Tutor

A modern, professional web application that provides Socratic-style math tutoring using AI. The tutor uses guiding questions to help primary school students discover solutions on their own, following the Socratic method of teaching. Features an optional AI co-learner that acts as a study buddy.

## ✨ Features

- 🧑‍🏫 **AI-Powered Socratic Tutor**: Never gives direct answers, always guides with questions
- 👦 **Optional Co-Learner**: Toggle-able AI study buddy that provides helpful hints and encouragement
- 🎨 **Modern Professional UI**: Clean indigo design with Space Grotesk typography
- 💬 **Intelligent Chat Interface**: Real-time conversation with typing indicators
- 📱 **Fully Responsive**: Optimized for desktop, tablet, and mobile devices
- 🎯 **Smart Categorization**: 7 response categories for targeted teaching approaches
- ⚡ **Smooth Interactions**: Auto-scrolling chat with elegant animations
- 🔄 **Conversation Memory**: Maintains context throughout the learning session
- 🎉 **Success Recognition**: Celebrates when students solve problems correctly

## 🛠 Technology Stack

- **Backend**: FastAPI (Python 3.8+)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript ES6+
- **AI**: OpenAI GPT-4.1 Nano
- **Styling**: Modern CSS with custom properties and gradients
- **Typography**: Space Grotesk + Inter font system
- **Deployment**: Uvicorn ASGI server

## 🚀 Quick Start

1. **Clone the repository:**

```bash
git clone https://github.com/gabriel-zyz/socratic-app.git
cd socratic-app
```

2. **Create and activate virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Run the application:**

```bash
python main.py
```

6. **Open in browser:**
   Navigate to `http://localhost:8000`

## 🎯 Response Categories

The AI tutor intelligently categorizes responses for optimal teaching:

| Category                     | Purpose               | Example Response                                          |
| ---------------------------- | --------------------- | --------------------------------------------------------- |
| **General Interaction**      | Greetings & redirects | "Hello! What math topic would you like to explore?"       |
| **Conceptual Understanding** | Concept confusion     | "What do you think happens when we multiply by zero?"     |
| **Procedural Difficulty**    | Step-by-step help     | "What should be our first step? Why?"                     |
| **Math Anxiety**             | Emotional support     | "Tell me about a time you solved a similar problem!"      |
| **Problem Solving Strategy** | Approach guidance     | "What information do we know? What are we finding?"       |
| **Real World Connection**    | Practical relevance   | "How might we use this when building something?"          |
| **Correct Answer**           | Success celebration   | "Excellent! You got it right! Ready for a new challenge?" |

## 🎨 Design Features

- **Color Palette**: Modern indigo (#6366f1) with gradient accents
- **Typography**: Space Grotesk headings, Inter body text
- **Layout**: Max-width 840px, 70% message width, 16px border radius
- **Animations**: Smooth slide-in effects, hover states, scale interactions
- **Accessibility**: Focus rings, semantic HTML, proper contrast ratios

## 🧠 AI Personalities

### Socratic Tutor

- Never gives direct answers
- Uses guiding questions exclusively
- Celebrates student success
- Maintains encouraging tone
- Redirects off-topic conversations to math

### Co-Learner (Optional)

- Acts as confused but helpful study buddy
- Provides hints without spoiling answers
- Makes learning fun and relatable
- Suggests different approaches
- Offers gentle encouragement

## 📡 API Documentation

### Endpoints

#### `GET /`

Serves the main application interface

#### `POST /api/chat`

Handles chat interactions

**Request:**

```json
{
  "messages": [
    {
      "role": "user" | "assistant",
      "content": "string",
      "category": "string"
    }
  ],
  "new_message": "string",
  "include_colearner": boolean
}
```

**Response:**

```json
{
  "response": "string",
  "category": "string",
  "colearner_response": "string" // Only if include_colearner is true
}
```

## 🏗 Project Structure

```
socratic-app/
├── main.py              # FastAPI application & AI logic
├── requirements.txt     # Python dependencies
├── static/
│   ├── index.html      # Main application interface
│   ├── styles.css      # Modern styling & animations
│   └── app.js          # Frontend logic & API calls
├── .env                # Environment variables (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🧪 Development

The application follows modern web development practices:

- **Separation of Concerns**: Clear separation between AI logic, API, and UI
- **Responsive Design**: Mobile-first CSS with proper breakpoints
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Performance**: Optimized API calls and smooth animations
- **Accessibility**: Semantic HTML and keyboard navigation support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4.1 Nano model
- FastAPI team for the excellent web framework
- The Socratic method for inspiring effective teaching approaches
