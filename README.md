# Emotional AI Chatbot

This repository contains the implementation of an **Emotional AI Chatbot** that utilizes LangChain and OpenRouter to create a conversational agent capable of understanding and responding to user emotions. The chatbot integrates emotional parameters into its responses, enhancing the interaction quality by considering the user's emotional state.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
  - [Requirements](#requirements)
  - [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Starting the Backend](#starting-the-backend)
  - [Starting the Frontend](#starting-the-frontend)
- [Features](#features)
  - [Tasks Implemented](#tasks-implemented)
- [File Structure](#file-structure)
- [References](#references)

## Overview

The Emotional AI Chatbot uses a feedforward neural network and is designed for unsupervised learning. It incorporates a chatbot that can understand and respond to user inputs while considering emotional parameters such as valence and arousal. The key contributions of this implementation include:

- Utilizing **LangChain** for managing conversation context.
- Integrating **OpenRouter** as the language model for generating responses.
- Calculating emotional states and adapting responses accordingly.

## Setup

### Requirements

- Python 3.7+
- Flask
- Flask-CORS
- LangChain
- OpenAI's Python library
- Streamlit
- python-dotenv
- Requests

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/emotional_ai_chatbot.git
   cd emotional_ai_chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file in the root directory and add your OpenRouter API key:
   ```plaintext
   OPENROUTER_API_KEY=your_api_key_here
   ```

## Configuration

All configurable parameters are handled directly in the code or through environment variables. Adjust any necessary parameters directly as needed.

## Usage

### Starting the Backend
To run the Flask backend server, execute:
```bash
python app.py
```

### Starting the Frontend
In another terminal, run the Streamlit frontend:
```bash
streamlit run frontend/ui.py
```

## Features

### Tasks Implemented

1. **Emotional State Calculation**: Calculates anger and sadness levels based on user-defined emotional parameters.
2. **Chatbot Response**: Sends user messages to the backend and retrieves responses considering the emotional context.
3. **Interactive User Interface**: Built using Streamlit for a clean and engaging user experience.

## File Structure

```
emotional_ai_chatbot/
├── app.py                # Flask backend server
├── frontend/             # Frontend files
│   ├── ui.py             # Streamlit UI script
│   ├── config.yaml       # Configuration file (if applicable)
├── requirements.txt      # Dependency list
├── .env                  # Environment variables
└── README.md             # This README file
```
