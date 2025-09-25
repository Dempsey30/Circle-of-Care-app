from fastapi import FastAPI, APIRouter, HTTPException, Header, Cookie, Response, WebSocket, WebSocketDisconnect, Request, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import requests
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json
import asyncio

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# WebSocket connection manager for live chat
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[Dict] = []

    async def connect(self, websocket: WebSocket, user_id: str, user_name: str, community_id: str = "general"):
        await websocket.accept()
        connection_info = {
            "websocket": websocket,
            "user_id": user_id,
            "user_name": user_name,
            "community_id": community_id,
            "connected_at": datetime.now(timezone.utc)
        }
        self.active_connections.append(connection_info)
        
        # Notify others that user joined
        await self.broadcast_to_community(community_id, {
            "type": "user_joined",
            "user_name": user_name,
            "message": f"{user_name} joined the chat",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }, exclude_user=user_id)

    def disconnect(self, websocket: WebSocket):
        connection = next((conn for conn in self.active_connections if conn["websocket"] == websocket), None)
        if connection:
            self.active_connections.remove(connection)
            return connection
        return None

    async def broadcast_to_community(self, community_id: str, message: dict, exclude_user: str = None):
        """Broadcast message to all users in a specific community"""
        disconnected_connections = []
        for connection in self.active_connections:
            if connection["community_id"] == community_id and connection["user_id"] != exclude_user:
                try:
                    await connection["websocket"].send_text(json.dumps(message))
                except:
                    disconnected_connections.append(connection)
        
        # Clean up disconnected connections
        for conn in disconnected_connections:
            self.active_connections.remove(conn)

    async def send_personal_message(self, user_id: str, message: dict):
        """Send private message to specific user"""
        connection = next((conn for conn in self.active_connections if conn["user_id"] == user_id), None)
        if connection:
            try:
                await connection["websocket"].send_text(json.dumps(message))
                return True
            except:
                self.active_connections.remove(connection)
        return False

manager = ConnectionManager()

# Pydantic Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: str
    picture: Optional[str] = None
    is_anonymous: bool = False
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    health_conditions: List[str] = []
    bio: Optional[str] = None
    privacy_level: str = "private"  # private, community, public
    is_veteran: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_banned: bool = False
    warning_count: int = 0

class UserSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Community(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    category: str  # ptsd, chronic-pain, cancer, veterans, general-wellness, etc.
    is_private: bool = True
    member_count: int = 0
    created_by: str
    moderators: List[str] = []
    rules: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Post(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    community_id: str
    author_id: str
    title: str
    content: str
    is_anonymous: bool = False
    support_type: str = "general"  # general, seeking-help, offering-support, milestone
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_flagged: bool = False
    flag_count: int = 0

class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    message: str
    response: str
    session_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LiveChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    community_id: str
    user_id: str
    user_name: str
    message: str
    is_anonymous: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_moderated: bool = False

class PanicButtonRequest(BaseModel):
    user_id: str
    trigger_description: Optional[str] = None
    severity: str = "moderate"  # mild, moderate, severe

class ModerationReport(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    reporter_id: str
    reported_user_id: str
    reported_content_id: Optional[str] = None
    report_type: str  # harassment, inappropriate, politics, spam
    description: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_resolved: bool = False

# Create Models
class UserCreate(BaseModel):
    email: str
    name: str
    picture: Optional[str] = None

class CommunityCreate(BaseModel):
    name: str
    description: str
    category: str

class PostCreate(BaseModel):
    title: str
    content: str
    is_anonymous: bool = False
    support_type: str = "general"

class ChatRequest(BaseModel):
    message: str
    is_panic: bool = False

class LiveChatMessageCreate(BaseModel):
    community_id: str
    message: str
    is_anonymous: bool = False

# Helper Functions
def prepare_for_mongo(data: dict) -> dict:
    """Prepare data for MongoDB storage by converting dates to ISO strings"""
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return data

def parse_from_mongo(item: dict) -> dict:
    """Parse data from MongoDB by converting ISO strings back to datetime objects"""
    for key, value in item.items():
        if key in ['created_at', 'updated_at', 'expires_at', 'last_active'] and isinstance(value, str):
            try:
                item[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                pass
    return item

async def moderate_content(content: str) -> Dict[str, Any]:
    """Basic content moderation using AI"""
    try:
        system_message = """You are a content moderator for a mental health support platform. Check if this message violates our community guidelines:

        BANNED CONTENT:
        - Politics or government discussions
        - Harassment, bullying, or personal attacks
        - Excessive profanity or inappropriate language
        - Spam or promotional content
        - Content that could trigger trauma without warning
        - Hate speech or discrimination

        Respond with JSON: {"is_appropriate": true/false, "reason": "explanation", "severity": "low/medium/high"}"""
        
        chat = LlmChat(
            api_key=os.environ['EMERGENT_LLM_KEY'],
            session_id=f"moderation_{uuid.uuid4()}",
            system_message=system_message
        ).with_model("openai", "gpt-5")
        
        user_message = UserMessage(text=content)
        response = await asyncio.wait_for(chat.send_message(user_message), timeout=10.0)
        
        # Try to parse JSON response
        import json
        try:
            moderation_result = json.loads(response)
            return moderation_result
        except:
            # Fallback if AI doesn't return proper JSON
            if any(word in content.lower() for word in ['politics', 'government', 'election', 'president', 'congress']):
                return {"is_appropriate": False, "reason": "Political content not allowed", "severity": "medium"}
            return {"is_appropriate": True, "reason": "Content appears appropriate", "severity": "low"}
            
    except Exception as e:
        logging.error(f"Moderation error: {e}")
        # Conservative fallback - flag suspicious content
        suspicious_words = ['politics', 'government', 'damn', 'shit', 'fuck', 'asshole']
        if any(word in content.lower() for word in suspicious_words):
            return {"is_appropriate": False, "reason": "Potentially inappropriate content", "severity": "medium"}
        return {"is_appropriate": True, "reason": "Content check completed", "severity": "low"}

async def get_current_user(request: Request = None) -> Optional[User]:
    """Get current user from session token in cookie"""
    if not request:
        return None
        
    session_token = request.cookies.get("session_token")
    if not session_token:
        return None
    
    try:
        # Check session in database
        session_data = await db.sessions.find_one({"session_token": session_token})
        if not session_data or datetime.now(timezone.utc) > datetime.fromisoformat(session_data['expires_at'].replace('Z', '+00:00')):
            return None
        
        # Get user data
        user_data = await db.users.find_one({"id": session_data['user_id']})
        if user_data and not user_data.get('is_banned', False):
            return User(**parse_from_mongo(user_data))
        return None
    except Exception as e:
        logging.error(f"Error getting current user: {e}")
        return None

# Authentication Endpoints
@api_router.post("/auth/session")
async def process_session(x_session_id: Optional[str] = Header(None, alias="X-Session-ID")):
    """Process session ID from Emergent Auth"""
    if not x_session_id:
        raise HTTPException(status_code=400, detail="X-Session-ID header required")
    
    try:
        # Get session data from Emergent Auth
        response = requests.get(
            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
            headers={"X-Session-ID": x_session_id}
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        session_data = response.json()
        
        # Check if user exists
        existing_user = await db.users.find_one({"email": session_data["email"]})
        
        if not existing_user:
            # Create new user
            new_user = User(
                email=session_data["email"],
                name=session_data["name"],
                picture=session_data.get("picture"),
                display_name=session_data["name"]
            )
            user_dict = prepare_for_mongo(new_user.dict())
            await db.users.insert_one(user_dict)
            user = new_user
        else:
            user = User(**parse_from_mongo(existing_user))
        
        # Check if user is banned
        if user.is_banned:
            raise HTTPException(status_code=403, detail="Account suspended. Contact circleofcaresupport@pm.me")
        
        # Create session
        session_token = f"st_{uuid.uuid4()}"
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        new_session = UserSession(
            user_id=user.id,
            session_token=session_token,
            expires_at=expires_at
        )
        session_dict = prepare_for_mongo(new_session.dict())
        await db.sessions.insert_one(session_dict)
        
        # Return response with cookie
        response_data = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture": user.picture,
            "session_token": session_token
        }
        
        response = JSONResponse(content=response_data)
        response.set_cookie(
            key="session_token",
            value=session_token,
            max_age=7 * 24 * 60 * 60,  # 7 days
            httponly=True,
            secure=True,
            samesite="none",
            path="/"
        )
        
        return response
        
    except Exception as e:
        logging.error(f"Session processing error: {e}")
        raise HTTPException(status_code=500, detail="Session processing failed")

@api_router.post("/auth/logout")
async def logout(request: Request):
    """Logout user and clear session"""
    session_token = request.cookies.get("session_token")
    if session_token:
        await db.sessions.delete_one({"session_token": session_token})
    
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie("session_token", path="/")
    return response

@api_router.get("/auth/me")
async def get_current_user_info(request: Request):
    """Get current user information"""
    current_user = await get_current_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user

# Community Endpoints
@api_router.get("/communities", response_model=List[Community])
async def get_communities():
    """Get all communities"""
    communities = await db.communities.find().to_list(length=None)
    return [Community(**parse_from_mongo(community)) for community in communities]

@api_router.post("/communities", response_model=Community)
async def create_community(community_data: CommunityCreate, request: Request):
    """Create a new community"""
    current_user = await get_current_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    new_community = Community(
        name=community_data.name,
        description=community_data.description,
        category=community_data.category,
        created_by=current_user.id,
        moderators=[current_user.id],
        rules=[
            "Be respectful and supportive to all members",
            "No politics or government discussions allowed",
            "Keep profanity to a minimum",
            "No harassment, bullying, or personal attacks",
            "This is a safe space - be kind and understanding"
        ]
    )
    community_dict = prepare_for_mongo(new_community.dict())
    await db.communities.insert_one(community_dict)
    return new_community

@api_router.get("/communities/{community_id}/posts", response_model=List[Post])
async def get_community_posts(community_id: str):
    """Get posts for a specific community"""
    posts = await db.posts.find({"community_id": community_id, "is_flagged": False}).to_list(length=None)
    return [Post(**parse_from_mongo(post)) for post in posts]

@api_router.post("/communities/{community_id}/posts", response_model=Post)
async def create_post(community_id: str, post_data: PostCreate, request: Request = None):
    """Create a new post in a community - Allow anonymous posting for broader access"""
    
    # Try to get current user, but allow anonymous posting
    current_user = None
    if request:
        try:
            current_user = await get_current_user(request)
        except:
            pass
    
    # For anonymous users, create a temporary author ID
    author_id = current_user.id if current_user else f"anonymous_{uuid.uuid4().hex[:8]}"
    
    # Basic content validation - no AI moderation to avoid timeouts
    if not post_data.title.strip() or not post_data.content.strip():
        raise HTTPException(status_code=400, detail="Title and content are required")
    
    # Simple content filter for inappropriate content
    blocked_words = ["politics", "trump", "biden", "election", "government", "fuck", "shit", "damn"]
    content_to_check = f"{post_data.title} {post_data.content}".lower()
    
    if any(word in content_to_check for word in blocked_words):
        raise HTTPException(status_code=400, detail="Content violates community guidelines: No politics or excessive profanity allowed")
    
    new_post = Post(
        community_id=community_id,
        author_id=author_id,
        title=post_data.title,
        content=post_data.content,
        is_anonymous=post_data.is_anonymous if current_user else True,
        support_type=post_data.support_type
    )
    post_dict = prepare_for_mongo(new_post.dict())
    await db.posts.insert_one(post_dict)
    return new_post

# Live Chat WebSocket - At app level for proper routing
@app.websocket("/api/ws/chat/{community_id}")
async def websocket_chat_endpoint(websocket: WebSocket, community_id: str):
    """WebSocket endpoint for live chat - accessible to all users"""
    # Generate a temporary user identifier
    temp_user_id = f"user_{uuid.uuid4().hex[:8]}"
    temp_user_name = f"Member{uuid.uuid4().hex[:4]}"
    
    try:
        await manager.connect(websocket, temp_user_id, temp_user_name, community_id)
        
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                
                # Basic message validation
                if "message" in message_data and message_data["message"].strip():
                    # Simple content filter
                    message_content = message_data["message"]
                    
                    # Block obvious inappropriate content
                    blocked_words = ["politics", "trump", "biden", "election", "government"]
                    if any(word.lower() in message_content.lower() for word in blocked_words):
                        await websocket.send_text(json.dumps({
                            "type": "warning",
                            "message": "Political content is not allowed in our healing community."
                        }))
                        continue
                    
                    # Store message in database
                    chat_message = LiveChatMessage(
                        community_id=community_id,
                        user_id=temp_user_id,
                        user_name=message_data.get("user_name", temp_user_name),
                        message=message_content,
                        is_anonymous=message_data.get("is_anonymous", True)
                    )
                    chat_dict = prepare_for_mongo(chat_message.dict())
                    await db.live_chat.insert_one(chat_dict)
                    
                    # Broadcast to community
                    broadcast_message = {
                        "type": "message",
                        "id": chat_message.id,
                        "user_name": chat_message.user_name if not chat_message.is_anonymous else f"Anonymous{temp_user_id[-4:]}",
                        "message": chat_message.message,
                        "timestamp": chat_message.created_at.isoformat(),
                        "is_anonymous": chat_message.is_anonymous
                    }
                    await manager.broadcast_to_community(community_id, broadcast_message)
                    
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid message format"
                }))
                
    except WebSocketDisconnect:
        connection = manager.disconnect(websocket)
        if connection:
            await manager.broadcast_to_community(community_id, {
                "type": "user_left",
                "user_name": connection["user_name"],
                "message": f"{connection['user_name']} left the chat",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
        await websocket.close()

# AI Companion Endpoints
@api_router.post("/ai/chat")
async def chat_with_ai(chat_request: ChatRequest, request: Request):
    """Chat with AI mental health companion"""
    current_user = await get_current_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Initialize AI chat with trauma-sensitive system message
        system_message = """You are a compassionate mental health companion for Circle of Care, a trauma-sensitive support platform created by Brent Dempsey. You specialize in PTSD, chronic pain, cancer recovery, veteran support, and general wellness. 

        Key guidelines:
        - Always be gentle, understanding, and non-judgmental
        - Use trauma-informed language
        - Provide practical coping strategies and grounding techniques
        - Encourage professional help when needed
        - Never diagnose or provide medical advice
        - Validate emotions and experiences
        - Offer hope and encouragement
        - If this is a panic/crisis situation, prioritize immediate safety and calming techniques
        - Remember that veterans may have unique trauma experiences
        - Cancer patients may need both physical and emotional support
        
        Remember: You're here to support, not replace professional therapy or medical care. For urgent support, users can contact circleofcaresupport@pm.me or call 250-902-9869."""
        
        # Add panic-specific guidance if this is a panic button request
        if chat_request.is_panic:
            system_message += """
            
            PANIC BUTTON ACTIVATED: This user is in distress. Priority:
            1. Immediate grounding and calming techniques
            2. Validate their courage in reaching out
            3. Provide simple, clear coping strategies
            4. Encourage them they are safe right now
            5. Suggest breathing exercises or grounding techniques
            """
        
        chat = LlmChat(
            api_key=os.environ['EMERGENT_LLM_KEY'],
            session_id=f"user_{current_user.id}_{uuid.uuid4()}",
            system_message=system_message
        ).with_model("openai", "gpt-5")
        
        user_message = UserMessage(text=chat_request.message)
        response = await chat.send_message(user_message)
        
        # Store chat in database (don't block on this)
        try:
            chat_message = ChatMessage(
                user_id=current_user.id,
                message=chat_request.message,
                response=response,
                session_id=f"user_{current_user.id}_{uuid.uuid4()}"
            )
            chat_dict = prepare_for_mongo(chat_message.dict())
            await db.chat_history.insert_one(chat_dict)
        except Exception as e:
            logging.warning(f"Failed to store chat message: {e}")
        
        return {"response": response, "is_panic_response": chat_request.is_panic}
        
    except Exception as e:
        logging.error(f"AI chat error: {e}")
        raise HTTPException(status_code=500, detail="AI companion temporarily unavailable")

@api_router.post("/ai/panic-button")
async def panic_button(panic_request: PanicButtonRequest):
    """Emergency panic button with immediate AI support"""
    try:
        # Immediate trauma-informed response based on severity
        immediate_responses = {
            "mild": "I hear you, and you're safe right now. Let's breathe together. Try the 4-7-8 breathing: breathe in for 4, hold for 7, out for 8. You're going to be okay.",
            "moderate": "You reached out, and that takes tremendous courage. You are safe in this moment. Let's ground together: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.",
            "severe": "You are incredibly brave for reaching out. You are safe right now. Focus on this: place both feet firmly on the ground, take slow deep breaths, and know that this feeling will pass. You are not alone."
        }
        
        immediate_response = immediate_responses.get(panic_request.severity, immediate_responses["moderate"])
        
        # Emergency contacts and grounding techniques (always available)
        emergency_response = {
            "immediate_response": immediate_response,
            "emergency_contacts": [
                {"name": "Circle of Care Support", "contact": "circleofcaresupport@pm.me"},
                {"name": "Circle of Care Phone", "contact": "250-902-9869"},
                {"name": "Crisis Text Line", "contact": "Text HOME to 741741"},
                {"name": "National Suicide Prevention Lifeline", "contact": "988"},
                {"name": "Veterans Crisis Line", "contact": "1-800-273-8255"},
                {"name": "PTSD Foundation of America", "contact": "1-877-717-PTSD"}
            ],
            "grounding_techniques": [
                "5-4-3-2-1 grounding: Name 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste",
                "Box breathing: Breathe in for 4, hold for 4, out for 4, hold for 4",
                "Progressive muscle relaxation: Tense and release each muscle group"
            ]
        }
        
        # Try to get AI guidance with timeout protection
        try:
            system_message = f"""CRISIS SUPPORT MODE: A user with {panic_request.severity} distress has activated the panic button. They described: {panic_request.trigger_description or 'general distress'}.

            Your response should:
            1. Acknowledge their courage
            2. Provide immediate grounding techniques
            3. Offer specific coping strategies
            4. Reassure them of safety
            5. Be calm, clear, and supportive
            6. Remind them they can contact Brent at circleofcaresupport@pm.me or 250-902-9869 for personal support
            
            Keep response under 150 words for immediate consumption."""
            
            chat = LlmChat(
                api_key=os.environ['EMERGENT_LLM_KEY'],
                session_id=f"panic_{panic_request.user_id}_{uuid.uuid4()}",
                system_message=system_message
            ).with_model("openai", "gpt-5")
            
            user_message = UserMessage(text=f"I'm feeling {panic_request.severity} distress. {panic_request.trigger_description or ''}")
            
            # Set a short timeout for AI response to ensure immediate help
            ai_response = await asyncio.wait_for(
                chat.send_message(user_message), 
                timeout=3.0  # Reduced from 5 to 3 seconds
            )
            emergency_response["ai_guidance"] = ai_response
            
        except asyncio.TimeoutError:
            logging.warning("AI response timeout during panic button - using fallback")
            emergency_response["ai_guidance"] = "You are safe. Focus on your breathing. This moment will pass. You are stronger than you know. If you need personal support, contact Brent at circleofcaresupport@pm.me"
        except Exception as ai_error:
            logging.error(f"AI error during panic: {ai_error}")
            emergency_response["ai_guidance"] = "You are safe. Focus on your breathing. This moment will pass. You are stronger than you know. Contact support at circleofcaresupport@pm.me"
        
        return emergency_response
        
    except Exception as e:
        logging.error(f"Critical panic button error: {e}")
        # Always return immediate help even if everything fails
        return {
            "immediate_response": "You are safe. Take slow, deep breaths. This moment will pass. You are stronger than you know.",
            "ai_guidance": "Focus on grounding yourself. You reached out for help, and that shows incredible strength. Contact support at circleofcaresupport@pm.me",
            "emergency_contacts": [
                {"name": "Circle of Care Support", "contact": "circleofcaresupport@pm.me"},
                {"name": "Circle of Care Phone", "contact": "250-902-9869"},
                {"name": "Crisis Text Line", "contact": "Text HOME to 741741"},
                {"name": "National Suicide Prevention Lifeline", "contact": "988"}
            ],
            "grounding_techniques": [
                "5-4-3-2-1 grounding: Name 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste",
                "Box breathing: Breathe in for 4, hold for 4, out for 4, hold for 4"
            ]
        }

# Moderation Endpoints
@api_router.post("/moderation/report")
async def report_content(report_data: Dict, request: Request):
    """Report inappropriate content or behavior"""
    current_user = await get_current_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    report = ModerationReport(
        reporter_id=current_user.id,
        reported_user_id=report_data["reported_user_id"],
        reported_content_id=report_data.get("reported_content_id"),
        report_type=report_data["report_type"],
        description=report_data["description"]
    )
    
    report_dict = prepare_for_mongo(report.dict())
    await db.moderation_reports.insert_one(report_dict)
    
    return {"message": "Report submitted successfully. Our 24/7 moderation team will review it."}

# User Profile Endpoints
@api_router.get("/profile")
async def get_profile(request: Request):
    """Get current user's profile"""
    current_user = await get_current_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user

@api_router.patch("/profile")
async def update_profile(profile_data: dict, request: Request):
    """Update user profile"""
    current_user = await get_current_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Update allowed fields
    allowed_fields = ['display_name', 'bio', 'health_conditions', 'privacy_level', 'avatar_url', 'is_veteran']
    update_data = {k: v for k, v in profile_data.items() if k in allowed_fields}
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    await db.users.update_one({"id": current_user.id}, {"$set": update_data})
    return {"message": "Profile updated successfully"}

# Health endpoints for basic checks
@api_router.get("/")
async def root():
    return {"message": "Circle of Care API by Brent Dempsey", "status": "healthy", "security": "24/7 monitoring active"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat(), "monitoring": "active"}

@api_router.get("/contact-info")
async def get_contact_info():
    return {
        "creator": "Brent Dempsey",
        "email": "circleofcaresupport@pm.me",
        "phone": "250-902-9869",
        "support": "24/7 monitoring and support available",
        "security": "Platform monitored 24/7 for safety and security"
    }

@api_router.get("/ws-test/{community_id}")
async def test_ws_route(community_id: str):
    """Test endpoint to verify routing is working"""
    return {"message": f"WebSocket route test for community {community_id}", "status": "routing_works"}

# Initialize default communities
async def setup_default_communities():
    """Create default communities if they don't exist"""
    default_communities = [
        {
            "name": "PTSD Recovery Room",
            "description": "A safe space for PTSD survivors to share experiences and support each other in healing",
            "category": "ptsd",
            "rules": [
                "Be respectful and supportive to all members",
                "No politics or government discussions allowed", 
                "Keep profanity to a minimum",
                "No harassment, bullying, or personal attacks",
                "Trigger warnings required for sensitive content",
                "This is a safe space - be kind and understanding"
            ]
        },
        {
            "name": "Chronic Pain Warriors",
            "description": "Support and understanding for those managing chronic pain conditions and invisible illnesses",
            "category": "chronic-pain",
            "rules": [
                "Be respectful and supportive to all members",
                "No medical advice - share experiences only",
                "No politics or government discussions allowed",
                "Keep profanity to a minimum", 
                "Celebrate small victories together",
                "This is a safe space - be kind and understanding"
            ]
        },
        {
            "name": "Cancer Fighters & Survivors",
            "description": "Community for cancer patients, survivors, and their families to find hope and support",
            "category": "cancer",
            "rules": [
                "Be respectful and supportive to all members",
                "No medical advice - share experiences only",
                "Celebrate milestones and victories",
                "Support during difficult times",
                "No politics or government discussions allowed",
                "This is a safe space - be kind and understanding"
            ]
        },
        {
            "name": "Veterans Support Network",
            "description": "Dedicated space for veterans to connect, share experiences, and support each other",
            "category": "veterans",
            "rules": [
                "Respect all branches of service",
                "No politics or government discussions allowed",
                "Support your fellow veterans",
                "Keep profanity to a minimum",
                "Share resources and experiences",
                "This is a safe space - be kind and understanding"
            ]
        },
        {
            "name": "Anxiety & Depression Support",
            "description": "Community for those dealing with anxiety, depression, and other mental health challenges",
            "category": "mental-health",
            "rules": [
                "Be gentle and understanding",
                "No judgment zone",
                "Share coping strategies that work",
                "Celebrate progress, no matter how small",
                "No politics or government discussions allowed",
                "This is a safe space - be kind and understanding"
            ]
        },
        {
            "name": "General Wellness Circle",
            "description": "Open community for general mental health, wellness, and self-care support for everyone",
            "category": "general-wellness",
            "rules": [
                "Welcome everyone with open arms",
                "Share wellness tips and strategies",
                "Support each other's journey",
                "No politics or government discussions allowed",
                "Keep profanity to a minimum",
                "This is a safe space - be kind and understanding"
            ]
        }
    ]
    
    for community_data in default_communities:
        existing = await db.communities.find_one({"name": community_data["name"]})
        if not existing:
            new_community = Community(
                name=community_data["name"],
                description=community_data["description"],
                category=community_data["category"],
                created_by="system",
                moderators=["system"],
                rules=community_data["rules"]
            )
            community_dict = prepare_for_mongo(new_community.dict())
            await db.communities.insert_one(community_dict)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    await setup_default_communities()
    logger.info("Circle of Care API started - 24/7 monitoring active")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()