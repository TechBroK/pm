"""AI service using OpenRouter for project management tasks."""

import os
import json
import logging
from typing import Optional, Dict, Any
import httpx

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.io/api/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"


class AIService:
    """Service for AI interactions via OpenRouter."""

    @staticmethod
    def test_connection() -> Dict[str, Any]:
        """Test OpenRouter connection with a simple 2+2 prompt."""
        try:
            if not OPENROUTER_API_KEY:
                return {
                    "success": False,
                    "error": "OPENROUTER_API_KEY not configured in .env",
                    "response": None,
                }

            messages = [{"role": "user", "content": "What is 2 + 2? Reply with just the number."}]

            response = httpx.post(
                OPENROUTER_API_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODEL,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 100,
                },
                timeout=30.0,
            )

            if response.status_code != 200:
                error_detail = response.text
                try:
                    error_data = response.json()
                    error_detail = error_data.get("error", {}).get("message", error_detail)
                except:
                    pass

                logger.error(f"OpenRouter API error: {response.status_code} - {error_detail}")
                return {
                    "success": False,
                    "error": f"OpenRouter API error: {response.status_code}",
                    "detail": error_detail,
                    "response": None,
                }

            data = response.json()
            ai_response = data.get("choices", [{}])[0].get("message", {}).get("content", "")

            logger.info(f"OpenRouter test call successful. Response: {ai_response}")
            return {
                "success": True,
                "error": None,
                "response": ai_response,
                "model": MODEL,
            }

        except httpx.TimeoutException:
            logger.error("OpenRouter API request timed out")
            return {
                "success": False,
                "error": "Request timeout",
                "response": None,
            }
        except Exception as e:
            logger.error(f"OpenRouter API error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": None,
            }

    @staticmethod
    def ask_about_board(
        question: str, board_context: Dict[str, Any], user_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ask AI a question about the Kanban board.
        Returns structured response with text and optional board updates.
        """
        try:
            if not OPENROUTER_API_KEY:
                return {
                    "success": False,
                    "error": "OPENROUTER_API_KEY not configured",
                    "response": None,
                }

            # Format board context for the AI
            board_summary = AIService._format_board_context(board_context)

            system_prompt = f"""You are a project management assistant helping with a Kanban board.
Current board state:
{board_summary}

You can help by:
1. Answering questions about the board
2. Suggesting improvements
3. Creating, moving, or updating cards based on user requests

When responding, be concise and helpful. If the user asks you to modify the board, 
include specific instructions about what cards to create/move."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message or question},
            ]

            response = httpx.post(
                OPENROUTER_API_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODEL,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 500,
                },
                timeout=30.0,
            )

            if response.status_code != 200:
                error_detail = response.text
                try:
                    error_data = response.json()
                    error_detail = error_data.get("error", {}).get("message", error_detail)
                except:
                    pass

                logger.error(f"OpenRouter API error: {response.status_code} - {error_detail}")
                return {
                    "success": False,
                    "error": f"OpenRouter API error: {response.status_code}",
                    "response": None,
                }

            data = response.json()
            ai_response = data.get("choices", [{}])[0].get("message", {}).get("content", "")

            logger.info(f"OpenRouter board question response: {ai_response[:100]}...")
            return {
                "success": True,
                "error": None,
                "response": ai_response,
                "model": MODEL,
            }

        except Exception as e:
            logger.error(f"OpenRouter board question error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": None,
            }

    @staticmethod
    def _format_board_context(board: Dict[str, Any]) -> str:
        """Format board data for AI context."""
        summary = f"Board: {board.get('title', 'My Board')}\n\n"
        summary += "Columns and cards:\n"

        for col in board.get("columns", []):
            summary += f"\n{col['title']}:\n"
            for card in col.get("cards", []):
                details = f" - {card['details'][:50]}" if card.get("details") else ""
                summary += f"  - {card['title']}{details}\n"

        return summary
