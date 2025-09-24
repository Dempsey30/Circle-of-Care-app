import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "./components/ui/avatar";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "./components/ui/dialog";
import { Input } from "./components/ui/input";
import { Textarea } from "./components/ui/textarea";
import { Label } from "./components/ui/label";
import { AlertTriangle, Heart, Users, MessageCircle, Shield, Star, ArrowRight, Menu, X, Zap } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Marketing Website Component
const Website = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleJoinNow = () => {
    const redirectUrl = `${window.location.origin}/dashboard`;
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-emerald-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center">
                <Heart className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold text-emerald-800">Circle of Care</span>
            </div>

            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-slate-700 hover:text-emerald-700 font-medium transition-colors">Features</a>
              <a href="#communities" className="text-slate-700 hover:text-emerald-700 font-medium transition-colors">Communities</a>
              <a href="#support" className="text-slate-700 hover:text-emerald-700 font-medium transition-colors">Support</a>
              <Button onClick={handleJoinNow} className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-6 py-2 rounded-full font-medium shadow-lg">
                Join Now
              </Button>
            </div>

            <div className="md:hidden">
              <Button variant="ghost" onClick={() => setIsMenuOpen(!isMenuOpen)} data-testid="mobile-menu-toggle">
                {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </Button>
            </div>
          </div>

          {/* Mobile Menu */}
          {isMenuOpen && (
            <div className="md:hidden py-4 space-y-2">
              <a href="#features" className="block px-3 py-2 text-slate-700 hover:text-emerald-700">Features</a>
              <a href="#communities" className="block px-3 py-2 text-slate-700 hover:text-emerald-700">Communities</a>
              <a href="#support" className="block px-3 py-2 text-slate-700 hover:text-emerald-700">Support</a>
              <Button onClick={handleJoinNow} className="w-full mt-2 bg-gradient-to-r from-emerald-500 to-teal-600 text-white">
                Join Now
              </Button>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-20 pb-32 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <Badge className="bg-emerald-100 text-emerald-800 hover:bg-emerald-200 px-4 py-1 text-sm font-medium">
                  Mental Health • Community • Support
                </Badge>
                <h1 className="text-5xl lg:text-6xl font-bold text-slate-900 leading-tight">
                  Your Safe Space for
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-600"> Healing & Growth</span>
                </h1>
                <p className="text-xl text-slate-600 leading-relaxed max-w-2xl">
                  Join Circle of Care - a trauma-sensitive community where PTSD survivors, chronic pain warriors, and wellness seekers find understanding, support, and healing together.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Button 
                  onClick={handleJoinNow} 
                  data-testid="join-now-hero-btn"
                  className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-8 py-4 text-lg rounded-full font-semibold shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105"
                >
                  Start Your Journey <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
                <Button variant="outline" className="px-8 py-4 text-lg rounded-full border-2 border-emerald-300 text-emerald-700 hover:bg-emerald-50">
                  Learn More
                </Button>
              </div>
              
              <div className="flex items-center space-x-6 text-sm text-slate-500">
                <div className="flex items-center space-x-2">
                  <Shield className="h-5 w-5 text-emerald-600" />
                  <span>100% Private & Secure</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Users className="h-5 w-5 text-emerald-600" />
                  <span>Anonymous Options</span>
                </div>
              </div>
            </div>
            
            <div className="relative">
              <div className="relative z-10 rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1604881991720-f91add269bed?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwxfHxtZW50YWwlMjBoZWFsdGglMjBzdXBwb3J0fGVufDB8fHx8MTc1ODc1MzA2Nnww&ixlib=rb-4.1.0&q=85"
                  alt="Supportive hands together representing community care and healing"
                  className="w-full h-96 object-cover"
                />
              </div>
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-br from-teal-400 to-cyan-500 rounded-full blur-xl opacity-70"></div>
              <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-full blur-xl opacity-70"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-4 sm:px-6 lg:px-8 bg-white/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-4xl font-bold text-slate-900">Healing Made Accessible</h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto">
              Discover powerful tools and supportive communities designed specifically for trauma recovery and mental wellness.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Card className="group hover:shadow-xl transition-all duration-300 border-0 bg-white/80 backdrop-blur-sm hover:scale-105">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-rose-100 to-pink-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <Zap className="h-8 w-8 text-rose-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">AI Companion</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-slate-600">24/7 trauma-informed AI support with panic button for instant help during crisis moments.</p>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 border-0 bg-white/80 backdrop-blur-sm hover:scale-105">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <Users className="h-8 w-8 text-emerald-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">Safe Communities</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-slate-600">Private groups for PTSD, chronic pain, cancer recovery, and general wellness support.</p>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 border-0 bg-white/80 backdrop-blur-sm hover:scale-105">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-purple-100 to-indigo-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <MessageCircle className="h-8 w-8 text-purple-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">Peer Support</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-slate-600">Connect with trained trauma coaches, mentors, and fellow survivors on your healing journey.</p>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 border-0 bg-white/80 backdrop-blur-sm hover:scale-105">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-amber-100 to-orange-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <Shield className="h-8 w-8 text-amber-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">Privacy First</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-slate-600">Anonymous profiles, encrypted chats, and complete control over what you share.</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Communities Section */}
      <section id="communities" className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <h2 className="text-4xl font-bold text-slate-900">Find Your Tribe</h2>
                <p className="text-xl text-slate-600 leading-relaxed">
                  Connect with others who understand your journey. Our communities are safe, moderated spaces where judgment has no place.
                </p>
              </div>
              
              <div className="grid gap-4">
                <div className="flex items-center space-x-4 p-4 bg-white/60 backdrop-blur-sm rounded-xl border border-emerald-100">
                  <div className="w-12 h-12 bg-gradient-to-br from-red-100 to-pink-100 rounded-xl flex items-center justify-center">
                    <Heart className="h-6 w-6 text-red-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-slate-800">PTSD Recovery Room</h3>
                    <p className="text-sm text-slate-600">Safe space for trauma survivors</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4 p-4 bg-white/60 backdrop-blur-sm rounded-xl border border-emerald-100">
                  <div className="w-12 h-12 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-xl flex items-center justify-center">
                    <Users className="h-6 w-6 text-emerald-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-slate-800">Chronic Pain Warriors</h3>
                    <p className="text-sm text-slate-600">Support for ongoing health challenges</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4 p-4 bg-white/60 backdrop-blur-sm rounded-xl border border-emerald-100">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-100 to-indigo-100 rounded-xl flex items-center justify-center">
                    <Star className="h-6 w-6 text-purple-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-slate-800">Cancer Fighters</h3>
                    <p className="text-sm text-slate-600">Community for cancer survivors</p>
                  </div>
                </div>
              </div>
              
              <Button 
                onClick={handleJoinNow}
                data-testid="join-communities-btn"
                className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-8 py-3 text-lg rounded-full font-semibold"
              >
                Join Our Communities <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </div>
            
            <div className="relative">
              <div className="relative z-10 rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1527525443983-6e60c75fff46?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwxfHxjb21tdW5pdHl8ZW58MHx8fHx8MTc1ODc1MzExM3ww&ixlib=rb-4.1.0&q=85"
                  alt="Community support - group holding hands on tree"
                  className="w-full h-96 object-cover"
                />
              </div>
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full blur-xl opacity-70"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Support Section */}
      <section id="support" className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-slate-50 to-emerald-50">
        <div className="max-w-7xl mx-auto text-center">
          <div className="space-y-8">
            <div className="space-y-4">
              <h2 className="text-4xl font-bold text-slate-900">Always Here When You Need Us</h2>
              <p className="text-xl text-slate-600 max-w-3xl mx-auto">
                Your mental health journey deserves compassionate, immediate support. Our AI companion and community are available 24/7.
              </p>
            </div>
            
            <div className="relative max-w-2xl mx-auto">
              <img 
                src="https://images.unsplash.com/photo-1541976844346-f18aeac57b06?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwyfHxtZW50YWwlMjBoZWFsdGglMjBzdXBwb3J0fGVufDB8fHx8MTc1ODc1MzA2Nnww&ixlib=rb-4.1.0&q=85"
                alt="Reaching hands showing support and help"
                className="w-full h-64 object-cover rounded-2xl shadow-xl"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 to-transparent rounded-2xl"></div>
              <div className="absolute bottom-8 left-8 right-8 text-white">
                <h3 className="text-2xl font-bold mb-2">Crisis Support Available</h3>
                <p className="text-lg opacity-90">Immediate help is just one click away</p>
              </div>
            </div>
            
            <Button 
              onClick={handleJoinNow}
              data-testid="get-support-btn" 
              className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-12 py-4 text-xl rounded-full font-bold shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105"
            >
              Get Support Now <ArrowRight className="ml-2 h-6 w-6" />
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center">
                  <Heart className="h-6 w-6 text-white" />
                </div>
                <span className="text-xl font-bold">Circle of Care</span>
              </div>
              <p className="text-slate-400">
                A trauma-sensitive community supporting PTSD recovery, chronic pain management, and overall mental wellness.
              </p>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Support</h3>
              <div className="space-y-2 text-slate-400">
                <p>Crisis Text Line: Text HOME to 741741</p>
                <p>National Suicide Prevention Lifeline: 988</p>
                <p>PTSD Foundation: 1-877-717-PTSD</p>
              </div>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Privacy</h3>
              <p className="text-slate-400">
                Your privacy and safety are our top priority. All communications are encrypted and you control what you share.
              </p>
            </div>
          </div>
          
          <div className="mt-12 pt-8 border-t border-slate-800 text-center text-slate-400">
            <p>&copy; 2025 Circle of Care. Built with compassion for healing journeys.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

// Dashboard Component (App Interface)
const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [communities, setCommunities] = useState([]);
  const [selectedCommunity, setSelectedCommunity] = useState(null);
  const [posts, setPosts] = useState([]);
  const [showPanicDialog, setShowPanicDialog] = useState(false);
  const [chatMessage, setChatMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [aiLoading, setAiLoading] = useState(false);

  // Handle Emergent Auth session
  useEffect(() => {
    const processAuth = async () => {
      const fragment = window.location.hash;
      const urlParams = new URLSearchParams(fragment.substring(1));
      const sessionId = urlParams.get('session_id');

      if (sessionId) {
        try {
          const response = await axios.post(`${API}/auth/session`, {}, {
            headers: { 'X-Session-ID': sessionId }
          });
          
          setUser(response.data);
          window.history.replaceState({}, document.title, window.location.pathname);
        } catch (error) {
          console.error('Auth error:', error);
        }
      } else {
        // Check existing session
        try {
          const response = await axios.get(`${API}/auth/me`, {
            withCredentials: true
          });
          setUser(response.data);
        } catch (error) {
          // Not authenticated, redirect to website
          window.location.href = '/';
        }
      }
      setLoading(false);
    };

    processAuth();
  }, []);

  // Load communities
  useEffect(() => {
    const loadCommunities = async () => {
      try {
        const response = await axios.get(`${API}/communities`, {
          withCredentials: true
        });
        setCommunities(response.data);
        
        // Set default communities if none exist
        if (response.data.length === 0) {
          await createDefaultCommunities();
        }
      } catch (error) {
        console.error('Error loading communities:', error);
      }
    };

    if (user) {
      loadCommunities();
    }
  }, [user]);

  const createDefaultCommunities = async () => {
    const defaultCommunities = [
      {
        name: "PTSD Recovery Room",
        description: "A safe space for PTSD survivors to share experiences and support each other",
        category: "ptsd"
      },
      {
        name: "Chronic Pain Warriors",
        description: "Support and understanding for those managing chronic pain conditions",
        category: "chronic-pain"
      },
      {
        name: "Cancer Fighters",
        description: "Community for cancer survivors and those currently fighting cancer",
        category: "cancer"
      },
      {
        name: "General Wellness",
        description: "Open community for general mental health and wellness support",
        category: "general-wellness"
      }
    ];

    for (const community of defaultCommunities) {
      try {
        await axios.post(`${API}/communities`, community, {
          withCredentials: true
        });
      } catch (error) {
        console.error('Error creating community:', community.name);
      }
    }

    // Reload communities
    const response = await axios.get(`${API}/communities`, {
      withCredentials: true
    });
    setCommunities(response.data);
  };

  const handleCommunitySelect = async (community) => {
    setSelectedCommunity(community);
    try {
      const response = await axios.get(`${API}/communities/${community.id}/posts`, {
        withCredentials: true
      });
      setPosts(response.data);
    } catch (error) {
      console.error('Error loading posts:', error);
    }
  };

  const handlePanicButton = async () => {
    setShowPanicDialog(true);
    try {
      const response = await axios.post(`${API}/ai/panic-button`, {
        user_id: user.id,
        severity: "moderate"
      }, {
        withCredentials: true
      });

      // Add panic response to chat history
      setChatHistory(prev => [...prev, {
        type: 'panic',
        immediate: response.data.immediate_response,
        ai_guidance: response.data.ai_guidance,
        emergency_contacts: response.data.emergency_contacts
      }]);
    } catch (error) {
      console.error('Panic button error:', error);
      setChatHistory(prev => [...prev, {
        type: 'panic',
        immediate: "You are safe. Take deep breaths. This moment will pass. You are stronger than you know.",
        emergency_contacts: [
          { name: "Crisis Text Line", contact: "Text HOME to 741741" },
          { name: "National Suicide Prevention Lifeline", contact: "988" }
        ]
      }]);
    }
  };

  const handleAIChat = async () => {
    if (!chatMessage.trim()) return;

    const userMessage = chatMessage;
    setChatMessage("");
    setAiLoading(true);

    // Add user message to chat history
    setChatHistory(prev => [...prev, {
      type: 'user',
      message: userMessage
    }]);

    try {
      const response = await axios.post(`${API}/ai/chat`, {
        message: userMessage,
        is_panic: false
      }, {
        withCredentials: true
      });

      // Add AI response to chat history
      setChatHistory(prev => [...prev, {
        type: 'ai',
        message: response.data.response
      }]);
    } catch (error) {
      console.error('AI chat error:', error);
      setChatHistory(prev => [...prev, {
        type: 'ai',
        message: "I'm sorry, I'm temporarily unavailable. Please try again or reach out to our community for support."
      }]);
    } finally {
      setAiLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post(`${API}/auth/logout`, {}, {
        withCredentials: true
      });
      window.location.href = '/';
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-emerald-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center">
                <Heart className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold text-emerald-800">Circle of Care</span>
            </div>

            <div className="flex items-center space-x-4">
              {/* Panic Button */}
              <Button
                onClick={handlePanicButton}
                data-testid="panic-button"
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full font-medium shadow-lg animate-pulse"
              >
                <AlertTriangle className="h-4 w-4 mr-2" />
                Need Help Now
              </Button>

              <div className="flex items-center space-x-2">
                <Avatar>
                  <AvatarImage src={user?.picture} alt={user?.name} />
                  <AvatarFallback>{user?.name?.[0]}</AvatarFallback>
                </Avatar>
                <span className="font-medium text-slate-700">{user?.display_name || user?.name}</span>
                <Button onClick={handleLogout} variant="ghost" size="sm">Logout</Button>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Communities Sidebar */}
          <div className="lg:col-span-1">
            <Card data-testid="communities-section">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Users className="h-5 w-5" />
                  <span>Communities</span>
                </CardTitle>
                <CardDescription>Find your support group</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                {communities.map(community => (
                  <Button
                    key={community.id}
                    variant={selectedCommunity?.id === community.id ? "default" : "ghost"}
                    onClick={() => handleCommunitySelect(community)}
                    data-testid={`community-${community.category}`}
                    className="w-full justify-start text-left h-auto p-3"
                  >
                    <div>
                      <div className="font-medium">{community.name}</div>
                      <div className="text-xs text-slate-500 mt-1">{community.description}</div>
                    </div>
                  </Button>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Welcome Message */}
            {!selectedCommunity && (
              <Card data-testid="welcome-section">
                <CardHeader>
                  <CardTitle>Welcome to Your Healing Journey, {user?.display_name || user?.name}!</CardTitle>
                  <CardDescription>
                    Choose a community to join conversations, or chat with our AI companion below for immediate support.
                  </CardDescription>
                </CardHeader>
              </Card>
            )}

            {/* Community Posts */}
            {selectedCommunity && (
              <Card data-testid="community-posts-section">
                <CardHeader>
                  <CardTitle>{selectedCommunity.name}</CardTitle>
                  <CardDescription>{selectedCommunity.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  {posts.length === 0 ? (
                    <div className="text-center py-8">
                      <p className="text-slate-500">No posts yet. Be the first to share your story or ask for support.</p>
                      <Button className="mt-4 bg-emerald-500 hover:bg-emerald-600 text-white">
                        Create First Post
                      </Button>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {posts.map(post => (
                        <Card key={post.id}>
                          <CardContent className="pt-4">
                            <h3 className="font-semibold text-slate-900">{post.title}</h3>
                            <p className="text-slate-600 mt-2">{post.content}</p>
                            <div className="flex items-center justify-between mt-3">
                              <Badge variant="outline">{post.support_type}</Badge>
                              <span className="text-xs text-slate-400">{new Date(post.created_at).toLocaleDateString()}</span>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* AI Companion Chat */}
            <Card data-testid="ai-companion-section">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <MessageCircle className="h-5 w-5" />
                  <span>AI Companion</span>
                </CardTitle>
                <CardDescription>24/7 trauma-informed support</CardDescription>
              </CardHeader>
              <CardContent>
                {/* Chat History */}
                <div className="space-y-4 mb-4 max-h-96 overflow-y-auto" data-testid="chat-history">
                  {chatHistory.map((chat, index) => (
                    <div key={index} className={`flex ${chat.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                      {chat.type === 'user' ? (
                        <div className="bg-emerald-500 text-white px-4 py-2 rounded-lg max-w-xs">
                          {chat.message}
                        </div>
                      ) : chat.type === 'ai' ? (
                        <div className="bg-slate-100 text-slate-800 px-4 py-2 rounded-lg max-w-lg">
                          {chat.message}
                        </div>
                      ) : (
                        <div className="bg-red-50 border border-red-200 p-4 rounded-lg w-full">
                          <div className="text-red-800 font-semibold mb-2">Crisis Support</div>
                          <p className="text-red-700 mb-3">{chat.immediate}</p>
                          {chat.ai_guidance && (
                            <p className="text-red-600 mb-3">{chat.ai_guidance}</p>
                          )}
                          <div className="space-y-1 text-sm text-red-600">
                            {chat.emergency_contacts?.map((contact, idx) => (
                              <div key={idx}><strong>{contact.name}:</strong> {contact.contact}</div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                  {aiLoading && (
                    <div className="flex justify-start">
                      <div className="bg-slate-100 px-4 py-2 rounded-lg">
                        <div className="animate-pulse">AI is typing...</div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Chat Input */}
                <div className="flex space-x-2">
                  <Input
                    value={chatMessage}
                    onChange={(e) => setChatMessage(e.target.value)}
                    placeholder="Share what's on your mind..."
                    onKeyPress={(e) => e.key === 'Enter' && handleAIChat()}
                    data-testid="ai-chat-input"
                    className="flex-1"
                  />
                  <Button 
                    onClick={handleAIChat} 
                    disabled={aiLoading || !chatMessage.trim()}
                    data-testid="send-chat-btn"
                    className="bg-emerald-500 hover:bg-emerald-600 text-white"
                  >
                    Send
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Panic Dialog */}
      <Dialog open={showPanicDialog} onOpenChange={setShowPanicDialog}>
        <DialogContent data-testid="panic-dialog">
          <DialogHeader>
            <DialogTitle className="text-red-600">Crisis Support Activated</DialogTitle>
            <DialogDescription>
              You've activated our panic button. You are safe. Help is available.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="bg-red-50 p-4 rounded-lg">
              <h3 className="font-semibold text-red-800 mb-2">Emergency Contacts</h3>
              <div className="space-y-1 text-sm text-red-700">
                <div><strong>Crisis Text Line:</strong> Text HOME to 741741</div>
                <div><strong>National Suicide Prevention Lifeline:</strong> 988</div>
                <div><strong>PTSD Foundation:</strong> 1-877-717-PTSD</div>
              </div>
            </div>
            <Button 
              onClick={() => setShowPanicDialog(false)}
              className="w-full bg-emerald-500 hover:bg-emerald-600 text-white"
            >
              I'm Safe Now
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

// Main App Component
function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Website />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;