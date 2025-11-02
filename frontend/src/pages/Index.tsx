import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ScatterChart, Scatter, AreaChart, Area, PieChart, Pie, Cell } from 'recharts';
import { AlertCircle, Wind, TrendingUp, MapPin, Users, Award, Bell, Settings, Clock, Zap, Brain, Target, Shield, AlertTriangle, CheckCircle, Download, Share2, ChevronDown, TrendingDown, Activity, Info, Calendar, BarChart3, Moon, Sun } from 'lucide-react';

const generateRealtimeData = () => {
  const cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'];
  return cities.map(city => ({
    city,
    aqi: Math.floor(Math.random() * 350) + 50,
    pm25: Math.floor(Math.random() * 200) + 30,
    pm10: Math.floor(Math.random() * 300) + 50,
    no2: Math.floor(Math.random() * 70) + 20,
    so2: Math.floor(Math.random() * 35) + 5,
    co: (Math.random() * 2 + 1).toFixed(1),
    o3: Math.floor(Math.random() * 90) + 20,
    temp: Math.floor(Math.random() * 15) + 20,
    humidity: Math.floor(Math.random() * 40) + 40,
    windSpeed: Math.floor(Math.random() * 15) + 5
  }));
};

const generateHistoricalData = () => {
  return Array.from({ length: 30 }, (_, i) => ({
    date: `Day ${30 - i}`,
    aqi: Math.floor(Math.random() * 200) + 100,
    pm25: Math.floor(Math.random() * 150) + 50
  }));
};

const generatePredictionData = () => {
  return Array.from({ length: 48 }, (_, i) => ({
    hour: `${i}h`,
    predicted: Math.floor(Math.random() * 150) + 100,
    lower: Math.floor(Math.random() * 120) + 80,
    upper: Math.floor(Math.random() * 180) + 120
  }));
};

const AQIBadge = ({ aqi }: { aqi: number }) => {
  const getDetails = (value: number) => {
    if (value <= 50) return { category: 'Good', color: 'from-green-500 to-green-600', icon: '😊' };
    if (value <= 100) return { category: 'Moderate', color: 'from-yellow-400 to-yellow-500', icon: '😐' };
    if (value <= 200) return { category: 'Poor', color: 'from-orange-500 to-orange-600', icon: '😷' };
    if (value <= 300) return { category: 'Very Poor', color: 'from-red-500 to-red-600', icon: '😨' };
    return { category: 'Severe', color: 'from-purple-700 to-purple-900', icon: '☠️' };
  };

  const details = getDetails(aqi);

  return (
    <div className={`bg-gradient-to-br ${details.color} text-white rounded-2xl p-6 shadow-xl text-center`}>
      <div className="text-5xl mb-2">{details.icon}</div>
      <div className="text-6xl font-bold mb-2">{aqi}</div>
      <div className="text-lg font-semibold">{details.category}</div>
    </div>
  );
};

const Index = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedCity, setSelectedCity] = useState('Delhi');
  const [realtimeData, setRealtimeData] = useState(generateRealtimeData());
  const [historicalData] = useState(generateHistoricalData());
  const [predictionData] = useState(generatePredictionData());
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  useEffect(() => {
    const interval = setInterval(() => {
      setRealtimeData(generateRealtimeData());
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  const selectedCityData = realtimeData.find(d => d.city === selectedCity) || realtimeData[0];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-blue-950 dark:to-indigo-950 transition-colors duration-300">
      <header className="bg-white dark:bg-gray-900 shadow-md sticky top-0 z-50 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg">
                <Wind className="text-white" size={28} />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-blue-600 dark:text-blue-400">BreatheSmart India</h1>
                <p className="text-xs text-gray-600 dark:text-gray-400">AI-Powered Air Quality Intelligence</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button 
                onClick={() => setIsDarkMode(!isDarkMode)}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
                aria-label="Toggle dark mode"
              >
                {isDarkMode ? <Sun size={20} className="text-yellow-500" /> : <Moon size={20} className="text-gray-700" />}
              </button>
              <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors">
                <Bell size={20} />
              </button>
              <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors">
                <Settings size={20} />
              </button>
            </div>
          </div>
        </div>
      </header>

      <nav className="bg-white dark:bg-gray-900 border-b dark:border-gray-800 sticky top-16 z-40 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex gap-6 overflow-x-auto">
            {['Dashboard', 'Predictions', 'Community', 'Policy Impact', 'Analytics'].map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab.toLowerCase().replace(' ', '-'))}
                className={`py-4 px-2 border-b-2 transition whitespace-nowrap ${
                  activeTab === tab.toLowerCase().replace(' ', '-')
                    ? 'border-blue-600 dark:border-blue-400 text-blue-600 dark:text-blue-400 font-semibold'
                    : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-6">
          <select
            value={selectedCity}
            onChange={(e) => setSelectedCity(e.target.value)}
            className="px-4 py-3 bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-xl font-medium text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
          >
            {realtimeData.map(city => (
              <option key={city.city} value={city.city}>{city.city}</option>
            ))}
          </select>
        </div>

        {activeTab === 'dashboard' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors duration-300">
              <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-4">{selectedCity} Current AQI</h3>
              <AQIBadge aqi={selectedCityData.aqi} />
              <div className="mt-6 space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">PM2.5</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">{selectedCityData.pm25} µg/m³</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">PM10</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">{selectedCityData.pm10} µg/m³</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">NO₂</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">{selectedCityData.no2} µg/m³</span>
                </div>
              </div>
            </div>

            <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors duration-300">
              <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-4">30-Day Trend</h3>
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={historicalData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="aqi" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
                  <Area type="monotone" dataKey="pm25" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <div className="lg:col-span-3 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors duration-300">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100">Health Impact</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Real-time assessment</p>
                </div>
                <Shield className="text-blue-600 dark:text-blue-400" size={32} />
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-red-50 p-4 rounded-lg">
                  <div className="text-xs text-red-600 mb-1">Health Risk</div>
                  <div className="text-2xl font-bold text-red-700">High</div>
                </div>
                <div className="bg-blue-50 p-4 rounded-lg">
                  <div className="text-xs text-blue-600 mb-1">Est. Cases</div>
                  <div className="text-2xl font-bold text-blue-700">{Math.floor(selectedCityData.aqi * 2.5)}</div>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <div className="text-xs text-green-600 mb-1">Economic Impact</div>
                  <div className="text-2xl font-bold text-green-700">₹{(selectedCityData.aqi * 0.15).toFixed(1)}Cr</div>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <div className="text-xs text-purple-600 mb-1">Vulnerable Pop.</div>
                  <div className="text-2xl font-bold text-purple-700">25%</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'predictions' && (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors duration-300">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100">48-Hour Prediction</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">AI model with 94% accuracy</p>
              </div>
              <Brain className="text-purple-600 dark:text-purple-400" size={32} />
            </div>
            <ResponsiveContainer width="100%" height={320}>
              <AreaChart data={predictionData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="upper" stroke="#d1d5db" fill="none" />
                <Area type="monotone" dataKey="predicted" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.3} />
                <Area type="monotone" dataKey="lower" stroke="#d1d5db" fill="none" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        )}

        {activeTab === 'community' && (
          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors duration-300">
              <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">Community Reports</h3>
              <div className="space-y-3">
                {[
                  { user: 'Rahul K.', location: 'Connaught Place', type: 'Construction Dust', votes: 45 },
                  { user: 'Priya S.', location: 'Andheri West', type: 'Industrial Smoke', votes: 32 }
                ].map((report, idx) => (
                  <div key={idx} className="border dark:border-gray-700 p-4 rounded-lg hover:shadow-md transition-shadow bg-white dark:bg-gray-900">
                    <div className="flex justify-between">
                      <div>
                        <div className="font-medium text-gray-900 dark:text-gray-100">{report.user}</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">{report.location}</div>
                        <span className="text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded mt-2 inline-block">
                          {report.type}
                        </span>
                      </div>
                      <div className="text-right">
                        <div className="font-medium text-gray-900 dark:text-gray-100">{report.votes} votes</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl shadow-lg p-6 text-white">
              <h3 className="text-xl font-bold mb-4">Your Impact Score</h3>
              <div className="text-5xl font-bold mb-2">1247</div>
              <div className="text-sm opacity-90">Total Points</div>
              <div className="mt-6 space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Reports Filed</span>
                  <span className="font-bold">12</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Votes Cast</span>
                  <span className="font-bold">34</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'policy-impact' && (
          <div className="grid lg:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors duration-300">
              <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">Policy Effectiveness</h3>
              <div className="space-y-4">
                {[
                  { name: 'Odd-Even Scheme', impact: 23, effectiveness: 78 },
                  { name: 'BS-VI Implementation', impact: 18, effectiveness: 85 }
                ].map((policy, idx) => (
                  <div key={idx} className="border dark:border-gray-700 p-4 rounded-lg bg-white dark:bg-gray-900">
                    <div className="flex justify-between mb-2">
                      <div className="font-medium text-gray-900 dark:text-gray-100">{policy.name}</div>
                      <div className="text-green-600 dark:text-green-400 font-bold">-{policy.impact}%</div>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div className="bg-blue-600 dark:bg-blue-500 h-2 rounded-full transition-all" style={{ width: `${policy.effectiveness}%` }} />
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">{policy.effectiveness}% effective</div>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors duration-300">
              <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">Cost-Benefit Analysis</h3>
              <div className="space-y-4">
                <div>
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Healthcare Savings</div>
                  <div className="text-3xl font-bold text-green-600 dark:text-green-400">₹2,450 Cr</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Implementation Cost</div>
                  <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">₹850 Cr</div>
                </div>
                <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg mt-4">
                  <div className="text-sm text-green-800 dark:text-green-400 mb-1">Net Benefit</div>
                  <div className="text-3xl font-bold text-green-600 dark:text-green-400">₹1,600 Cr</div>
                  <div className="text-xs text-green-700 dark:text-green-500 mt-1">ROI: 188%</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="grid lg:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors duration-300">
              <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">Pollution Source Analysis</h3>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={[
                  { metric: 'Vehicular', value: 85 },
                  { metric: 'Industrial', value: 72 },
                  { metric: 'Construction', value: 68 },
                  { metric: 'Biomass', value: 55 },
                  { metric: 'Other', value: 42 }
                ]}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="metric" />
                  <PolarRadiusAxis />
                  <Radar dataKey="value" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.6} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors duration-300">
              <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">Key Insights</h3>
              <div className="space-y-4">
                <div className="border-l-4 border-blue-500 dark:border-blue-400 pl-4">
                  <div className="font-medium text-gray-900 dark:text-gray-100">Peak Hours</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">7-10 AM shows 40% higher AQI</div>
                </div>
                <div className="border-l-4 border-green-500 dark:border-green-400 pl-4">
                  <div className="font-medium text-gray-900 dark:text-gray-100">Weather Impact</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Rain reduces AQI by 35%</div>
                </div>
                <div className="border-l-4 border-purple-500 dark:border-purple-400 pl-4">
                  <div className="font-medium text-gray-900 dark:text-gray-100">Seasonal Trend</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Winter months 60% worse than summer</div>
                </div>
                <div className="border-l-4 border-orange-500 dark:border-orange-400 pl-4">
                  <div className="font-medium text-gray-900 dark:text-gray-100">Traffic Correlation</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">85% correlation with vehicle density</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="bg-white dark:bg-gray-900 border-t dark:border-gray-800 mt-16 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center text-sm text-gray-600 dark:text-gray-400">
            © 2025 BreatheSmart India - | Powered by AI
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
