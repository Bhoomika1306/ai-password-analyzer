import { useState, useEffect } from 'react'
import { 
  Eye, 
  EyeOff, 
  Lock, 
  Shield, 
  ShieldAlert, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle, 
  Zap, 
  RefreshCw,
  Copy,
  Check,
  Sparkles
} from 'lucide-react'

function App() {
  // State variables
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)
  const [shake, setShake] = useState(false)

  // Analyze password function
  const analyzePassword = async () => {
    if (!password) {
      setShake(true)
      setTimeout(() => setShake(false), 500)
      return
    }
    
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      })
      
      if (!response.ok) {
        throw new Error('Failed to analyze password')
      }
      
      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error('Error:', error)
      setError('Failed to analyze password. Make sure backend is running on port 5000!')
    } finally {
      setLoading(false)
    }
  }

  // Copy password to clipboard
  const copyPassword = () => {
    navigator.clipboard.writeText(password)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  // Generate a strong password
  const generatePassword = () => {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    let generated = ''
    for (let i = 0; i < 16; i++) {
      generated += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    setPassword(generated)
    setResult(null)
  }

  // Get color based on strength
  const getStrengthColor = (strength) => {
    const colors = {
      'Weak': 'bg-red-500',
      'Medium': 'bg-yellow-500',
      'Strong': 'bg-green-500'
    }
    return colors[strength] || 'bg-gray-500'
  }

  const getStrengthTextColor = (strength) => {
    const colors = {
      'Weak': 'text-red-400',
      'Medium': 'text-yellow-400',
      'Strong': 'text-green-400'
    }
    return colors[strength] || 'text-gray-400'
  }

  // Get risk icon and color
  const getRiskInfo = (risk) => {
    const info = {
      'High': { icon: ShieldAlert, color: 'text-red-400', bg: 'bg-red-500/10 border-red-500/20' },
      'Medium': { icon: Shield, color: 'text-yellow-400', bg: 'bg-yellow-500/10 border-yellow-500/20' },
      'Low': { icon: ShieldCheck, color: 'text-green-400', bg: 'bg-green-500/10 border-green-500/20' }
    }
    return info[risk] || { icon: Shield, color: 'text-gray-400', bg: 'bg-gray-500/10 border-gray-500/20' }
  }

  // Get strength width for progress bar
  const getStrengthWidth = (score) => {
    return `${score}%`
  }

  // Get strength emoji
  const getStrengthEmoji = (strength) => {
    const emojis = {
      'Weak': '🔴',
      'Medium': '🟡',
      'Strong': '🟢'
    }
    return emojis[strength] || '⚪'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background decorative elements */}
      <div className="absolute top-20 left-20 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      
      {/* Main Card */}
      <div className={`w-full max-w-md glass-card rounded-3xl shadow-2xl p-8 relative z-10 ${shake ? 'animate-shake' : ''}`}>
        
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="flex justify-center mb-4">
            <div className="p-4 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-2xl border border-blue-500/30 animate-pulse-glow">
              <Lock className="w-10 h-10 text-blue-400" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-white mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            AI Password Analyzer
          </h1>
          <p className="text-slate-400 text-sm">
            Powered by Machine Learning
          </p>
        </div>

        {/* Password Input */}
        <div className="mb-4 animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Enter Password
          </label>
          <div className="relative group">
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => {
                setPassword(e.target.value)
                setResult(null)
                setError(null)
              }}
              onKeyPress={(e) => e.key === 'Enter' && analyzePassword()}
              placeholder="Type your password..."
              className="w-full px-4 py-4 bg-slate-800/50 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all pr-24"
            />
            <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
              {password && (
                <button
                  onClick={copyPassword}
                  className="p-2 text-slate-400 hover:text-white transition-colors rounded-lg hover:bg-slate-700/50"
                  title="Copy password"
                >
                  {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
                </button>
              )}
              <button
                onClick={() => setShowPassword(!showPassword)}
                className="p-2 text-slate-400 hover:text-white transition-colors rounded-lg hover:bg-slate-700/50"
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3 mb-6 animate-fade-in" style={{ animationDelay: '0.2s' }}>
          <button
            onClick={analyzePassword}
            disabled={!password || loading}
            className={`flex-1 py-4 rounded-xl font-semibold text-white transition-all ${
              !password || loading
                ? 'bg-slate-700 cursor-not-allowed opacity-50'
                : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 shadow-lg hover:shadow-blue-500/25 transform hover:-translate-y-0.5 active:translate-y-0'
            }`}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <RefreshCw className="w-5 h-5 animate-spin" />
                Analyzing...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-2">
                <Zap className="w-5 h-5" />
                Analyze Password
              </span>
            )}
          </button>
          
          <button
            onClick={generatePassword}
            className="px-4 py-4 bg-slate-700/50 hover:bg-slate-600/50 border border-slate-600 rounded-xl text-white transition-all hover:shadow-lg"
            title="Generate strong password"
          >
            <Sparkles className="w-5 h-5" />
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm animate-fade-in flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
            {error}
          </div>
        )}

        {/* Results Section */}
        {result && !error && (
          <div className="space-y-5 animate-fade-in">
            
            {/* Strength Score Card */}
            <div className="bg-slate-800/30 rounded-2xl p-5 border border-slate-700/50">
              <div className="flex justify-between items-center mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{getStrengthEmoji(result.strength)}</span>
                  <span className="text-sm font-medium text-slate-300">Strength</span>
                </div>
                <span className={`text-lg font-bold ${getStrengthTextColor(result.strength)}`}>
                  {result.strength}
                </span>
              </div>
              
              {/* Progress Bar */}
              <div className="relative w-full bg-slate-700 rounded-full h-4 overflow-hidden">
                <div
                  className={`h-full rounded-full progress-bar ${getStrengthColor(result.strength)}`}
                  style={{ width: getStrengthWidth(result.score) }}
                />
              </div>
              
              <div className="flex justify-between mt-2">
                <span className="text-xs text-slate-500">0</span>
                <span className="text-xs font-medium text-slate-400">Score: {result.score}/100</span>
                <span className="text-xs text-slate-500">100</span>
              </div>
            </div>

            {/* Risk Level Card */}
            {(() => {
              const riskInfo = getRiskInfo(result.risk)
              const RiskIcon = riskInfo.icon
              return (
                <div className={`flex items-center gap-4 p-5 rounded-2xl border ${riskInfo.bg} animate-slide-in`}>
                  <div className={`p-3 rounded-xl bg-slate-800/50`}>
                    <RiskIcon className={`w-7 h-7 ${riskInfo.color}`} />
                  </div>
                  <div>
                    <p className="text-xs text-slate-400 uppercase tracking-wider">Risk Level</p>
                    <p className={`text-xl font-bold ${riskInfo.color}`}>
                      {result.risk}
                    </p>
                  </div>
                </div>
              )
            })()}

            {/* Suggestions */}
            {result.suggestions && result.suggestions.length > 0 && (
              <div className="animate-fade-in" style={{ animationDelay: '0.2s' }}>
                <h3 className="text-sm font-medium text-slate-300 flex items-center gap-2 mb-3">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  Suggestions to Improve
                </h3>
                <ul className="space-y-2 stagger-children">
                  {result.suggestions.map((suggestion, index) => (
                    <li
                      key={index}
                      className="flex items-start gap-3 text-sm text-slate-300 bg-slate-800/30 p-4 rounded-xl border border-slate-700/30 hover:border-slate-600/50 transition-colors"
                    >
                      <div className="p-1 bg-blue-500/10 rounded-lg flex-shrink-0 mt-0.5">
                        <CheckCircle className="w-4 h-4 text-blue-400" />
                      </div>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Success Message */}
            {result.strength === 'Strong' && result.suggestions.length === 0 && (
              <div className="p-5 bg-green-500/10 border border-green-500/20 rounded-2xl text-center animate-fade-in">
                <ShieldCheck className="w-12 h-12 text-green-400 mx-auto mb-2" />
                <p className="text-green-400 font-semibold">Excellent Password!</p>
                <p className="text-green-400/70 text-sm">Your password is strong and secure</p>
              </div>
            )}
          </div>
        )}
      </div>
      
      {/* Footer */}
      <div className="absolute bottom-4 text-center text-slate-600 text-xs">
        AI Password Strength Analyzer • Built with React + Flask + ML
      </div>
    </div>
  )
}

export default App
