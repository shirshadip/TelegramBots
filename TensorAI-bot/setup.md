# 🤖 Tensor AI Bot - Setup Guide

## Overview

This is a Telegram bot powered by **NVIDIA Nemotron** models. The bot uses the NVIDIA Build API to generate intelligent responses to user queries.

---

## 🔧 Prerequisites

- Python 3.9+
- pip (Python package manager)
- A Telegram account
- An NVIDIA Build account with API access

---

## 📋 Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/start`
3. Send `/newbot`
4. Follow the prompts to create your bot
5. Copy the **API Token** (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
6. Save this token securely

---

## 🔑 Step 2: Get NVIDIA API Key

1. Go to [NVIDIA Build](https://build.nvidia.com/)
2. Sign up or log in with your account
3. Navigate to **API Keys** (usually in account settings)
4. Create a new API key or copy existing one
5. Your key will start with `nvapi-`
6. Save this key securely

### Finding Available Models

1. Go to NVIDIA Build Console
2. Look for **Available Models** or **Model Playground**
3. Check which Nemotron models are available for your account
4. Copy the exact model identifier (e.g., `nvidia/nemotron-3-super-128b-instruct-qwen`)

---

## 🚀 Step 3: Configure Environment

### Option A: Using `.env` file (Recommended)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials:
   ```
   BOT_TOKEN=your_telegram_token_here
   NVIDIA_API_KEY=nvapi-your_api_key_here
   MODEL=nvidia/nemotron-3-super-128b-instruct-qwen
   MAX_HISTORY=10
   ```

3. Save the file

### Option B: Using `config.json`

Create a `config.json` file:

```json
{
  "BOT_TOKEN": "your_telegram_token_here",
  "NVIDIA_API_KEY": "nvapi-your_api_key_here",
  "MODEL": "nvidia/nemotron-3-super-128b-instruct-qwen",
  "MAX_HISTORY": 10
}
```

---

## 📦 Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install python-telegram-bot httpx python-dotenv pylatexenc
```

---

## ▶️ Step 5: Run the Bot

```bash
python bot.py
```

You should see:
```
==================================================
🤖 Tensor AI Bot Starting...
📌 Primary Model: nvidia/nemotron-3-super-128b-instruct-qwen
==================================================
AI Bot Running...
```

---

## 🎯 Step 6: Test the Bot

1. Open Telegram and find your bot (search by name)
2. Send `/start`
3. Send a test message like:
   ```
   What is photosynthesis?
   ```

---

## ⚙️ Common Issues & Solutions

### Issue: `Error: NVIDIA_API_KEY is missing`

**Solution:** Check that your `.env` file exists and contains:
```
NVIDIA_API_KEY=nvapi-xxxxx
```

### Issue: `404 Not Found` error

**Solution:** 
1. Verify the model ID is correct
2. Check if the model is available in your NVIDIA Build account
3. Try a different model from the available list

### Issue: `401 Unauthorized`

**Solution:**
1. Verify your NVIDIA API key is correct
2. Make sure the key starts with `nvapi-`
3. Check that the key hasn't expired

### Issue: `429 Too Many Requests`

**Solution:**
1. You've hit the rate limit
2. Wait a few minutes before sending requests
3. Consider using a model with higher throughput limits

### Issue: Timeout errors

**Solution:**
1. Try a shorter/simpler question
2. Check your internet connection
3. Verify NVIDIA API is responding

---

## 📄 Configuration Options

### `BOT_TOKEN`
- **Required**: Yes
- **Description**: Your Telegram bot token from @BotFather
- **Example**: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

### `NVIDIA_API_KEY`
- **Required**: Yes
- **Description**: Your NVIDIA Build API key
- **Example**: `nvapi-xxx...`

### `MODEL`
- **Required**: Yes (if MODELS not set)
- **Description**: Single model to use
- **Example**: `nvidia/nemotron-3-super-128b-instruct-qwen`

### `MODELS`
- **Required**: No (use MODEL instead)
- **Description**: Comma-separated list of fallback models
- **Example**: `nvidia/nemotron-3-super-128b-instruct-qwen,nvidia/nemotron-4-340b-instruct`

### `MAX_HISTORY`
- **Required**: No
- **Default**: `10`
- **Description**: Number of recent messages to keep in conversation
- **Range**: 2-100

---

## 🌳 Available NVIDIA Models

Check NVIDIA Build for the latest available models. Common ones include:

- `nvidia/nemotron-3-super-128b-instruct-qwen`
- `nvidia/nemotron-4-340b-instruct`
- `nvidia/llama-3.3-nemotron-super-49b-v1`

---

## 🔒 Security Best Practices

1. **Never commit secrets** to version control
2. **Use `.env` files** instead of hardcoding credentials
3. **Keep your API keys private** - don't share them
4. **Use environment variables** in production
5. **Rotate API keys** periodically

---

## 📱 Bot Commands

- `/start` - Initialize bot and show greeting
- `/help` - Show available commands
- `/clear` - Clear conversation history and start fresh

---

## 🧠 System Prompt

The bot uses a comprehensive system prompt that makes it:
- An expert in science, math, AI, and engineering
- A patient educator who explains concepts clearly
- Rigorous in mathematical reasoning
- Able to provide code examples with explanations
- Professional and encouraging

You can modify `SYSTEM_PROMPT` in `bot.py` to customize behavior.

---

## 📊 Conversation Memory

- Each user has their own conversation history
- History is stored in RAM (lost on bot restart)
- Use `/clear` to reset a user's history
- Maximum messages kept is controlled by `MAX_HISTORY`

For persistence, you could modify the code to use a database like:
- SQLite
- PostgreSQL
- Redis

---

## 🐛 Troubleshooting

### Enable Debug Logging

Edit `bot.py` and change:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format="%(asctime)s | %(levelname)s | %(message)s"
)
```

### Check Request/Response

The bot logs:
- Which model is being tried
- HTTP status codes
- Full error details

Check the console output for diagnostic information.

---

## 📝 Example Interactions

**User:** What is the Doppler effect?

**Bot:** (Provides detailed explanation with physics, formulas, examples, and applications)

**User:** How do I sort an array in Python?

**Bot:** (Provides algorithm explanation, code examples, complexity analysis, and best practices)

**User:** Explain quantum entanglement

**Bot:** (Provides rigorous quantum mechanics explanation with intuitive examples)

---

## 🚀 Deployment Options

### Local Machine
```bash
python bot.py
```

### Cloud Services
- **Heroku** (free tier available)
- **AWS EC2** (cheap t2 instances)
- **Google Cloud Run**
- **DigitalOcean Droplets**

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
```

---

## 📚 Further Resources

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [NVIDIA Build Platform](https://build.nvidia.com/)
- [HTTPX Documentation](https://www.python-httpx.org/)

---

## ✅ Checklist Before Launch

- [ ] Created Telegram bot with @BotFather
- [ ] Got NVIDIA API key from build.nvidia.com
- [ ] Created `.env` file with credentials
- [ ] Installed all dependencies
- [ ] Tested bot locally
- [ ] Verified model is available in NVIDIA account
- [ ] Bot responds to test messages
- [ ] `/start`, `/help`, `/clear` commands work

---

## 💬 Support

If you encounter issues:

1. Check the console output for error messages
2. Verify all credentials are correct
3. Test the API key manually
4. Check NVIDIA Build dashboard for service status
5. Review the troubleshooting section above

---

**Happy botting! 🚀**