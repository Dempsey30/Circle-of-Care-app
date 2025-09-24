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
import { AlertTriangle, Heart, Users, MessageCircle, Shield, Star, ArrowRight, Menu, X, Zap, Phone, Mail, Eye, Flag } from "lucide-react";

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
              <div>
                <span className="text-xl font-bold text-emerald-800">Circle of Care</span>
                <p className="text-xs text-slate-500">By Brent Dempsey</p>
              </div>
            </div>

            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-slate-700 hover:text-emerald-700 font-medium transition-colors">Features</a>
              <a href="#communities" className="text-slate-700 hover:text-emerald-700 font-medium transition-colors">Communities</a>
              <a href="#support" className="text-slate-700 hover:text-emerald-700 font-medium transition-colors">Support</a>
              <a href="#contact" className="text-slate-700 hover:text-emerald-700 font-medium transition-colors">Contact</a>
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
              <a href="#contact" className="block px-3 py-2 text-slate-700 hover:text-emerald-700">Contact</a>
              <Button onClick={handleJoinNow} className="w-full mt-2 bg-gradient-to-r from-emerald-500 to-teal-600 text-white">
                Join Now
              </Button>
            </div>
          )}
        </div>
      </nav>

      {/* Security Notice */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white py-2">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center space-x-2 text-sm">
            <Eye className="h-4 w-4" />
            <span>🔒 Platform monitored 24/7 for your safety • No politics • Respectful community only</span>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <section className="pt-20 pb-32 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <Badge className="bg-emerald-100 text-emerald-800 hover:bg-emerald-200 px-4 py-1 text-sm font-medium">
                  Mental Health • Community • Support • Veterans
                </Badge>
                <h1 className="text-5xl lg:text-6xl font-bold text-slate-900 leading-tight">
                  Your Safe Space for
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-600"> Healing & Growth</span>
                </h1>
                <p className="text-xl text-slate-600 leading-relaxed max-w-2xl">
                  Join Circle of Care - a trauma-sensitive community where PTSD survivors, veterans, cancer fighters, chronic pain warriors, and wellness seekers find understanding, support, and healing together.
                </p>
                <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4">
                  <p className="text-sm text-emerald-800">
                    <strong>Created by Brent Dempsey</strong> - A platform built with compassion for your healing journey. 
                    Contact directly: <a href="mailto:circleofcaresupport@pm.me" className="underline">circleofcaresupport@pm.me</a>
                  </p>
                </div>
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
                <div className="flex items-center space-x-2">
                  <Eye className="h-5 w-5 text-emerald-600" />
                  <span>24/7 Monitoring</span>
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
              Discover powerful tools and supportive communities designed specifically for trauma recovery, cancer support, veteran care, and mental wellness.
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
                <CardTitle className="text-xl font-semibold text-slate-800">Specialized Communities</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-slate-600">PTSD recovery, cancer support, veteran networks, chronic pain warriors, and wellness circles.</p>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 border-0 bg-white/80 backdrop-blur-sm hover:scale-105">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-purple-100 to-indigo-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <MessageCircle className="h-8 w-8 text-purple-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">Live Peer Support</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-slate-600">Real-time chat with trained peer supporters, mentors, and fellow survivors on your healing journey.</p>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 border-0 bg-white/80 backdrop-blur-sm hover:scale-105">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-amber-100 to-orange-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <Shield className="h-8 w-8 text-amber-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">Security First</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-slate-600">Anonymous profiles, 24/7 monitoring, strict community guidelines, and complete control over sharing.</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Communities Section */}
      <section id="communities" className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-4xl font-bold text-slate-900">Find Your Support Community</h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto">
              Connect with others who understand your journey. Our communities are safe, moderated spaces where judgment has no place and healing happens together.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* PTSD Recovery */}
            <Card className="hover:shadow-xl transition-all duration-300 border border-red-100 bg-gradient-to-br from-red-50 to-pink-50">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-red-100 to-pink-200 rounded-2xl flex items-center justify-center">
                  <Heart className="h-8 w-8 text-red-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">PTSD Recovery Room</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 mb-4">Safe space for trauma survivors to heal and support each other.</p>
                <div className="text-sm text-slate-500">
                  <p>• Trauma-informed support</p>
                  <p>• Trigger warning protocols</p>
                  <p>• 24/7 crisis support available</p>
                </div>
              </CardContent>
            </Card>

            {/* Veterans Support */}
            <Card className="hover:shadow-xl transition-all duration-300 border border-blue-100 bg-gradient-to-br from-blue-50 to-indigo-50">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-blue-100 to-indigo-200 rounded-2xl flex items-center justify-center">
                  <Star className="h-8 w-8 text-blue-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">Veterans Support Network</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 mb-4">Dedicated space for veterans to connect and support each other.</p>
                <div className="text-sm text-slate-500">
                  <p>• All branches welcome</p>
                  <p>• Combat & service trauma support</p>
                  <p>• Transition assistance resources</p>
                </div>
              </CardContent>
            </Card>

            {/* Cancer Support */}
            <Card className="hover:shadow-xl transition-all duration-300 border border-purple-100 bg-gradient-to-br from-purple-50 to-pink-50">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-purple-100 to-pink-200 rounded-2xl flex items-center justify-center">
                  <Star className="h-8 w-8 text-purple-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">Cancer Fighters & Survivors</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 mb-4">Hope and strength for cancer patients, survivors, and families.</p>
                <div className="text-sm text-slate-500">
                  <p>• Treatment journey support</p>
                  <p>• Caregiver resources</p>
                  <p>• Celebration of milestones</p>
                </div>
              </CardContent>
            </Card>

            {/* Chronic Pain */}
            <Card className="hover:shadow-xl transition-all duration-300 border border-green-100 bg-gradient-to-br from-green-50 to-emerald-50">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-green-100 to-emerald-200 rounded-2xl flex items-center justify-center">
                  <Users className="h-8 w-8 text-green-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">Chronic Pain Warriors</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 mb-4">Understanding for invisible illnesses and chronic conditions.</p>
                <div className="text-sm text-slate-500">
                  <p>• Pain management strategies</p>
                  <p>• Daily living tips</p>
                  <p>• Emotional support</p>
                </div>
              </CardContent>
            </Card>

            {/* Mental Health */}
            <Card className="hover:shadow-xl transition-all duration-300 border border-cyan-100 bg-gradient-to-br from-cyan-50 to-blue-50">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-cyan-100 to-blue-200 rounded-2xl flex items-center justify-center">
                  <MessageCircle className="h-8 w-8 text-cyan-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">Anxiety & Depression Support</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 mb-4">Gentle support for mental health challenges and wellness.</p>
                <div className="text-sm text-slate-500">
                  <p>• Coping strategies</p>
                  <p>• Mindfulness resources</p>
                  <p>• Progress celebration</p>
                </div>
              </CardContent>
            </Card>

            {/* General Wellness */}
            <Card className="hover:shadow-xl transition-all duration-300 border border-emerald-100 bg-gradient-to-br from-emerald-50 to-teal-50">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-emerald-100 to-teal-200 rounded-2xl flex items-center justify-center">
                  <Heart className="h-8 w-8 text-emerald-600" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-800">General Wellness Circle</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 mb-4">Open community for anyone seeking wellness and self-care support.</p>
                <div className="text-sm text-slate-500">
                  <p>• All backgrounds welcome</p>
                  <p>• Wellness tips & strategies</p>
                  <p>• Supportive community</p>
                </div>
              </CardContent>
            </Card>
          </div>
          
          <div className="text-center mt-12">
            <Button 
              onClick={handleJoinNow}
              data-testid="join-communities-btn"
              className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-8 py-3 text-lg rounded-full font-semibold"
            >
              Join Our Communities <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
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
                Your mental health journey deserves compassionate, immediate support. Our AI companion, community, and direct support are available 24/7.
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

      {/* Contact Section */}
      <section id="contact" className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-4xl mx-auto">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-4xl font-bold text-slate-900">Get In Touch</h2>
            <p className="text-xl text-slate-600">
              Need personal support? Have questions? Want to connect directly with Brent?
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            <Card className="p-8 bg-gradient-to-br from-emerald-50 to-teal-50 border-emerald-200">
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-12 h-12 bg-emerald-500 rounded-full flex items-center justify-center">
                  <Mail className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-slate-800">Email Support</h3>
                  <p className="text-slate-600">Get personal help and support</p>
                </div>
              </div>
              <div className="space-y-2">
                <p className="text-lg font-medium text-emerald-700">circleofcaresupport@pm.me</p>
                <p className="text-sm text-slate-600">
                  Email Brent directly for support, questions, or to share your story. 
                  All emails are read personally and responded to with care.
                </p>
              </div>
            </Card>

            <Card className="p-8 bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center">
                  <Phone className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-slate-800">Phone Support</h3>
                  <p className="text-slate-600">Direct line for urgent support</p>
                </div>
              </div>
              <div className="space-y-2">
                <p className="text-lg font-medium text-blue-700">250-902-9869</p>
                <p className="text-sm text-slate-600">
                  Call Brent directly if you need immediate support or have urgent concerns. 
                  This platform is built with your safety and healing in mind.
                </p>
              </div>
            </Card>
          </div>
          
          <div className="mt-12 p-6 bg-slate-100 rounded-xl">
            <h3 className="text-lg font-semibold text-slate-800 mb-3">Community Guidelines & Safety</h3>
            <div className="text-sm text-slate-600 space-y-2">
              <p>• <strong>24/7 Monitoring:</strong> This platform is monitored around the clock for safety and security</p>
              <p>• <strong>Zero Tolerance:</strong> Harassment, bullying, and disrespectful behavior results in immediate removal</p>
              <p>• <strong>No Politics:</strong> Political and government discussions are not allowed to keep focus on healing</p>
              <p>• <strong>Respectful Communication:</strong> Keep profanity to a minimum and maintain a supportive atmosphere</p>
              <p>• <strong>Safe Space:</strong> This is a judgment-free zone dedicated to healing and mutual support</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center">
                  <Heart className="h-6 w-6 text-white" />
                </div>
                <div>
                  <span className="text-xl font-bold">Circle of Care</span>
                  <p className="text-xs text-slate-400">By Brent Dempsey</p>
                </div>
              </div>
              <p className="text-slate-400">
                A trauma-sensitive community supporting PTSD recovery, veteran care, cancer support, chronic pain management, and overall mental wellness.
              </p>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Emergency Support</h3>
              <div className="space-y-2 text-slate-400 text-sm">
                <p>Crisis Text Line: Text HOME to 741741</p>
                <p>National Suicide Prevention Lifeline: 988</p>
                <p>Veterans Crisis Line: 1-800-273-8255</p>
                <p>PTSD Foundation: 1-877-717-PTSD</p>
              </div>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Contact & Support</h3>
              <div className="space-y-2 text-slate-400 text-sm">
                <p className="flex items-center space-x-2">
                  <Mail className="h-4 w-4" />
                  <a href="mailto:circleofcaresupport@pm.me" className="hover:text-white transition-colors">
                    circleofcaresupport@pm.me
                  </a>
                </p>
                <p className="flex items-center space-x-2">
                  <Phone className="h-4 w-4" />
                  <a href="tel:250-902-9869" className="hover:text-white transition-colors">
                    250-902-9869
                  </a>
                </p>
                <p className="flex items-center space-x-2">
                  <Eye className="h-4 w-4" />
                  <span>24/7 Monitoring Active</span>
                </p>
              </div>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Privacy & Safety</h3>
              <p className="text-slate-400 text-sm">
                Your privacy and safety are our top priority. All communications are encrypted, 
                the platform is monitored 24/7, and you control what you share. 
                This is a safe, judgment-free zone dedicated to healing.
              </p>
            </div>
          </div>
          
          <div className="mt-12 pt-8 border-t border-slate-800 text-center text-slate-400">
            <p>&copy; 2025 Circle of Care. Created by Brent Dempsey with compassion for healing journeys.</p>
            <p className="mt-2 text-sm">🔒 Secure • 👁️ Monitored 24/7 • ❤️ Built for Healing</p>
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
  const [liveChatMessage, setLiveChatMessage] = useState("");
  const [liveChatHistory, setLiveChatHistory] = useState([]);
  const [showLiveChat, setShowLiveChat] = useState(false);
  const [websocket, setWebsocket] = useState(null);

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
      } catch (error) {
        console.error('Error loading communities:', error);
      }
    };

    if (user) {
      loadCommunities();
    }
  }, [user]);

  // Live chat WebSocket connection
  const connectLiveChat = (communityId) => {
    if (websocket) {
      websocket.close();
    }

    // Use the correct WebSocket URL format
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = window.location.hostname;
    const wsPort = window.location.protocol === 'https:' ? '443' : '3000';
    const wsUrl = `${wsProtocol}//${wsHost}:${wsPort}/ws/chat/${communityId}`;
    
    console.log('Connecting to WebSocket:', wsUrl);
    
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      console.log('Connected to live chat');
      setWebsocket(ws);
      setLiveChatHistory(prev => [...prev, {
        type: 'system',
        message: 'Connected to live chat! Welcome to the community.',
        timestamp: new Date().toISOString()
      }]);
    };
    
    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        setLiveChatHistory(prev => [...prev, message]);
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    };
    
    ws.onclose = () => {
      console.log('Disconnected from live chat');
      setWebsocket(null);
      setLiveChatHistory(prev => [...prev, {
        type: 'system',
        message: 'Disconnected from chat. Click "Live Chat" to reconnect.',
        timestamp: new Date().toISOString()
      }]);
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setLiveChatHistory(prev => [...prev, {
        type: 'error',
        message: 'Chat connection error. Trying to reconnect...',
        timestamp: new Date().toISOString()
      }]);
    };
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

    // Connect to live chat for this community
    connectLiveChat(community.id);
  };

  const sendLiveChatMessage = () => {
    if (websocket && liveChatMessage.trim()) {
      const messageData = {
        user_id: user.id,
        user_name: user.display_name || user.name,
        message: liveChatMessage,
        is_anonymous: false
      };
      
      websocket.send(JSON.stringify(messageData));
      setLiveChatMessage("");
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
          { name: "Circle of Care Support", contact: "circleofcaresupport@pm.me" },
          { name: "Circle of Care Phone", contact: "250-902-9869" },
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
        message: "I'm sorry, I'm temporarily unavailable. Please try again or reach out to our support at circleofcaresupport@pm.me"
      }]);
    } finally {
      setAiLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      if (websocket) {
        websocket.close();
      }
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
              <div>
                <span className="text-xl font-bold text-emerald-800">Circle of Care</span>
                <p className="text-xs text-slate-500">By Brent Dempsey • 24/7 Monitored</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* Live Chat Toggle */}
              <Button
                onClick={() => setShowLiveChat(!showLiveChat)}
                variant="outline"
                size="sm"
                className="border-emerald-300 text-emerald-700 hover:bg-emerald-50"
              >
                <MessageCircle className="h-4 w-4 mr-2" />
                Live Chat
              </Button>

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
                <div className="text-sm">
                  <span className="font-medium text-slate-700">{user?.display_name || user?.name}</span>
                  <p className="text-xs text-slate-500">Safe & Secure</p>
                </div>
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
                  <span>Support Communities</span>
                </CardTitle>
                <CardDescription>Find your healing community</CardDescription>
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
                  <CardTitle>Welcome to Your Safe Healing Space, {user?.display_name || user?.name}!</CardTitle>
                  <CardDescription>
                    Choose a community to join conversations, use live chat for real-time peer support, or chat with our AI companion below for immediate help.
                    For direct support, contact Brent at circleofcaresupport@pm.me or 250-902-9869.
                  </CardDescription>
                </CardHeader>
              </Card>
            )}

            {/* Live Chat Section */}
            {showLiveChat && selectedCommunity && (
              <Card data-testid="live-chat-section">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <MessageCircle className="h-5 w-5" />
                    <span>Live Chat - {selectedCommunity.name}</span>
                  </CardTitle>
                  <CardDescription>Connect with peers in real-time • Monitored 24/7</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4 mb-4 max-h-64 overflow-y-auto border rounded-lg p-3 bg-slate-50">
                    {liveChatHistory.map((msg, index) => (
                      <div key={index} className={`text-sm ${msg.type === 'user_joined' || msg.type === 'user_left' ? 'text-center text-slate-500 italic' : ''}`}>
                        {msg.type === 'message' && (
                          <div className="flex items-start space-x-2">
                            <Avatar className="h-6 w-6">
                              <AvatarFallback className="text-xs">{msg.user_name[0]}</AvatarFallback>
                            </Avatar>
                            <div>
                              <span className="font-medium text-slate-700">{msg.user_name}: </span>
                              <span className="text-slate-600">{msg.message}</span>
                              <div className="text-xs text-slate-400">{new Date(msg.timestamp).toLocaleTimeString()}</div>
                            </div>
                          </div>
                        )}
                        {(msg.type === 'user_joined' || msg.type === 'user_left') && (
                          <p>{msg.message}</p>
                        )}
                        {msg.type === 'moderation_warning' && (
                          <div className="bg-yellow-100 border border-yellow-300 rounded p-2 text-yellow-800">
                            <strong>Moderation:</strong> {msg.message}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                  <div className="flex space-x-2">
                    <Input
                      value={liveChatMessage}
                      onChange={(e) => setLiveChatMessage(e.target.value)}
                      placeholder="Type your message to the community..."
                      onKeyPress={(e) => e.key === 'Enter' && sendLiveChatMessage()}
                      data-testid="live-chat-input"
                      className="flex-1"
                    />
                    <Button 
                      onClick={sendLiveChatMessage} 
                      disabled={!liveChatMessage.trim()}
                      data-testid="send-live-chat-btn"
                      className="bg-emerald-500 hover:bg-emerald-600 text-white"
                    >
                      Send
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Community Posts */}
            {selectedCommunity && (
              <Card data-testid="community-posts-section">
                <CardHeader>
                  <CardTitle>{selectedCommunity.name}</CardTitle>
                  <CardDescription>
                    {selectedCommunity.description}
                    <div className="mt-2 text-xs text-slate-500">
                      Community Guidelines: {selectedCommunity.rules?.slice(0, 2).join(' • ')}
                    </div>
                  </CardDescription>
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
                  <Zap className="h-5 w-5" />
                  <span>AI Companion</span>
                  <Badge className="bg-green-100 text-green-800">24/7 Available</Badge>
                </CardTitle>
                <CardDescription>Trauma-informed AI support • Contact Brent directly: circleofcaresupport@pm.me</CardDescription>
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
                          <div className="text-red-800 font-semibold mb-2 flex items-center">
                            <AlertTriangle className="h-4 w-4 mr-2" />
                            Crisis Support Activated
                          </div>
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
                    placeholder="Share what's on your mind... I'm here to help."
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
        <DialogContent data-testid="panic-dialog" className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="text-red-600 flex items-center space-x-2">
              <AlertTriangle className="h-5 w-5" />
              <span>Crisis Support Activated</span>
            </DialogTitle>
            <DialogDescription>
              You've activated our panic button. You are safe. Help is available immediately.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="bg-red-50 p-4 rounded-lg">
              <h3 className="font-semibold text-red-800 mb-2">Emergency Contacts</h3>
              <div className="grid md:grid-cols-2 gap-2 text-sm text-red-700">
                <div><strong>Circle of Care Support:</strong> circleofcaresupport@pm.me</div>
                <div><strong>Circle of Care Phone:</strong> 250-902-9869</div>
                <div><strong>Crisis Text Line:</strong> Text HOME to 741741</div>
                <div><strong>National Suicide Prevention:</strong> 988</div>
                <div><strong>Veterans Crisis Line:</strong> 1-800-273-8255</div>
                <div><strong>PTSD Foundation:</strong> 1-877-717-PTSD</div>
              </div>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-blue-800 mb-2">Grounding Techniques</h3>
              <div className="text-sm text-blue-700 space-y-1">
                <p>• <strong>5-4-3-2-1:</strong> Name 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste</p>
                <p>• <strong>Box Breathing:</strong> Breathe in for 4, hold for 4, out for 4, hold for 4</p>
                <p>• <strong>Safe Place:</strong> You are in a safe space right now. You reached out, and that shows strength.</p>
              </div>
            </div>
            <Button 
              onClick={() => setShowPanicDialog(false)}
              className="w-full bg-emerald-500 hover:bg-emerald-600 text-white"
            >
              I'm Safe Now - Continue to Support
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