from fastapi import FastAPI, APIRouter, HTTPException, Header, Cookie, Response
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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
    category: str  # ptsd, chronic-pain, cancer, general-wellness, etc.
    is_private: bool = True
    member_count: int = 0
    created_by: str
    moderators: List[str] = []
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

class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    message: str
    response: str
    session_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PanicButtonRequest(BaseModel):
    user_id: str
    trigger_description: Optional[str] = None
    severity: str = "moderate"  # mild, moderate, severe

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
    community_id: str
    title: str
    content: str
    is_anonymous: bool = False
    support_type: str = "general"

class ChatRequest(BaseModel):
    message: str
    is_panic: bool = False

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

async def get_current_user(session_token: Optional[str] = Cookie(None, alias="session_token")) -> Optional[User]:
    """Get current user from session token in cookie"""
    if not session_token:
        return None
    
    try:
        # Check session in database
        session_data = await db.sessions.find_one({"session_token": session_token})
        if not session_data or datetime.now(timezone.utc) > datetime.fromisoformat(session_data['expires_at'].replace('Z', '+00:00')):
            return None
        
        # Get user data
        user_data = await db.users.find_one({"id": session_data['user_id']})
        if user_data:
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
async def logout(session_token: Optional[str] = Cookie(None, alias="session_token")):
    """Logout user and clear session"""
    if session_token:
        await db.sessions.delete_one({"session_token": session_token})
    
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie("session_token", path="/")
    return response

@api_router.get("/auth/me")
async def get_current_user_info(current_user: Optional[User] = None):
    """Get current user information"""
    # Manual check since dependency injection isn't working
    current_user = await get_current_user()
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
async def create_community(community_data: CommunityCreate):
    """Create a new community"""
    current_user = await get_current_user()
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    new_community = Community(
        name=community_data.name,
        description=community_data.description,
        category=community_data.category,
        created_by=current_user.id,
        moderators=[current_user.id]
    )
    community_dict = prepare_for_mongo(new_community.dict())
    await db.communities.insert_one(community_dict)
    return new_community

@api_router.get("/communities/{community_id}/posts", response_model=List[Post])
async def get_community_posts(community_id: str):
    """Get posts for a specific community"""
    posts = await db.posts.find({"community_id": community_id}).to_list(length=None)
    return [Post(**parse_from_mongo(post)) for post in posts]

@api_router.post("/communities/{community_id}/posts", response_model=Post)
async def create_post(community_id: str, post_data: PostCreate):
    """Create a new post in a community"""
    current_user = await get_current_user()
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    new_post = Post(
        community_id=community_id,
        author_id=current_user.id,
        title=post_data.title,
        content=post_data.content,
        is_anonymous=post_data.is_anonymous,
        support_type=post_data.support_type
    )
    post_dict = prepare_for_mongo(new_post.dict())
    await db.posts.insert_one(post_dict)
    return new_post

# AI Companion Endpoints
@api_router.post("/ai/chat")
async def chat_with_ai(chat_request: ChatRequest):
    """Chat with AI mental health companion"""
    current_user = await get_current_user()
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Initialize AI chat with trauma-sensitive system message
        system_message = """You are a compassionate mental health companion for Circle of Care, a trauma-sensitive support platform. You specialize in PTSD, chronic pain, and general wellness support. 

        Key guidelines:
        - Always be gentle, understanding, and non-judgmental
        - Use trauma-informed language
        - Provide practical coping strategies and grounding techniques
        - Encourage professional help when needed
        - Never diagnose or provide medical advice
        - Validate emotions and experiences
        - Offer hope and encouragement
        - If this is a panic/crisis situation, prioritize immediate safety and calming techniques
        
        Remember: You're here to support, not replace professional therapy or medical care."""
        
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
        
        # Store chat in database
        chat_message = ChatMessage(
            user_id=current_user.id,
            message=chat_request.message,
            response=response,
            session_id=f"user_{current_user.id}_{uuid.uuid4()}"
        )
        chat_dict = prepare_for_mongo(chat_message.dict())
        await db.chat_history.insert_one(chat_dict)
        
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
                {"name": "Crisis Text Line", "contact": "Text HOME to 741741"},
                {"name": "National Suicide Prevention Lifeline", "contact": "988"},
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
            
            Keep response under 150 words for immediate consumption."""
            
            chat = LlmChat(
                api_key=os.environ['EMERGENT_LLM_KEY'],
                session_id=f"panic_{panic_request.user_id}_{uuid.uuid4()}",
                system_message=system_message
            ).with_model("openai", "gpt-5")
            
            user_message = UserMessage(text=f"I'm feeling {panic_request.severity} distress. {panic_request.trigger_description or ''}")
            
            # Set a short timeout for AI response to ensure immediate help
            import asyncio
            ai_response = await asyncio.wait_for(
                chat.send_message(user_message), 
                timeout=5.0  # 5 second timeout
            )
            emergency_response["ai_guidance"] = ai_response
            
        except asyncio.TimeoutError:
            logging.warning("AI response timeout during panic button - using fallback")
            emergency_response["ai_guidance"] = "You are safe. Focus on your breathing. This moment will pass. You are stronger than you know."
        except Exception as ai_error:
            logging.error(f"AI error during panic: {ai_error}")
            emergency_response["ai_guidance"] = "You are safe. Focus on your breathing. This moment will pass. You are stronger than you know."
        
        return emergency_response
        
    except Exception as e:
        logging.error(f"Critical panic button error: {e}")
        # Always return immediate help even if everything fails
        return {
            "immediate_response": "You are safe. Take slow, deep breaths. This moment will pass. You are stronger than you know.",
            "ai_guidance": "Focus on grounding yourself. You reached out for help, and that shows incredible strength.",
            "emergency_contacts": [
                {"name": "Crisis Text Line", "contact": "Text HOME to 741741"},
                {"name": "National Suicide Prevention Lifeline", "contact": "988"}
            ],
            "grounding_techniques": [
                "5-4-3-2-1 grounding: Name 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste",
                "Box breathing: Breathe in for 4, hold for 4, out for 4, hold for 4"
            ]
        }

# User Profile Endpoints
@api_router.get("/profile")
async def get_profile():
    """Get current user's profile"""
    current_user = await get_current_user()
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user

@api_router.patch("/profile")
async def update_profile(profile_data: dict):
    """Update user profile"""
    current_user = await get_current_user()
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Update allowed fields
    allowed_fields = ['display_name', 'bio', 'health_conditions', 'privacy_level', 'avatar_url']
    update_data = {k: v for k, v in profile_data.items() if k in allowed_fields}
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    await db.users.update_one({"id": current_user.id}, {"$set": update_data})
    return {"message": "Profile updated successfully"}

# Health endpoints for basic checks
@api_router.get("/")
async def root():
    return {"message": "Circle of Care API", "status": "healthy"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

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

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()