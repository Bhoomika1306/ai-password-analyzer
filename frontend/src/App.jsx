import { useState } from 'react'
import { Lock, Shield, AlertTriangle, CheckCircle, Sparkles, Copy, Eye, EyeOff } from 'lucide-react'
import './App.css'

function App() {
  const [password, setPassword] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showPassword, setShowPassword] = useState(false)
  const [copied, setCopied] = useState(false)
  const [shake, setShake] = useState(false)

  // HARDCODED RENDER BACKEND URL
  const response = await fetch('/api/analyze', {

  const analyzePassword = async () => {
    if (!password) return;
    
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setResult(data)
    } catch (err) {
      console.error('Error:', err)
      setError('Backend is waking up... Please wait 30 seconds and try again.')
    } finally {
      setLoading(false)
    }
  }

  const generatePassword = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*'
    let generated = ''
    for (let i = 0; i < 16; i++) {
      generated += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    setPassword(generated)
    setResult(null)
    setError(null)
  }

  const copyToClipboard = () => {
    if (password) {
      navigator.clipboard.writeText(password)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const getStrengthColor = (strength) => {
    switch (strength) {
      case 'Strong': return 'text-green-400'
      case 'Medium': return 'text-yellow-400'
      case 'Weak': return 'text-red-400'
      default: return 'text-gray-400'
    }
  }

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'Low': return 'text-green-400'
      case 'Medium': return 'text-yellow-400'
      case 'High': return 'text-red-400'
      default: return 'text-gray-400'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
          <div className="flex items-center justify-center mb-6">
            <div className="bg-purple-500/20 p-3 rounded-full">
              <Lock className="w-8 h-8 text-purple-300" />
            </div>
          </div>
          
          <h1 className="text-3xl font-bold text-center text-white mb-2">
            AI Password Analyzer
          </h1>
          <p className="text-center text-purple-200 mb-8">
            Check your password strength with ML
          </p>

          <div className="relative mb-6">
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password..."
              className="w-full px-4 py-3 pr-12 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
            <button
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-purple-300 hover:text-white"
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>

          <div className="flex gap-3 mb-6">
            <button
              onClick={analyzePassword}
              disabled={loading || !password}
              className="flex-1 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-800 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition-all flex items-center justify-center gap-2"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <Shield className="w-5 h-5" />
                  Analyze Password
                </>
              )}
            </button>
            
            <button
              onClick={generatePassword}
              className="bg-white/10 hover:bg-white/20 text-white font-semibold py-3 px-4 rounded-lg transition-all flex items-center gap-2"
            >
              <Sparkles className="w-5 h-5" />
            </button>
            
            <button
              onClick={copyToClipboard}
              className="bg-white/10 hover:bg-white/20 text-white font-semibold py-3 px-4 rounded-lg transition-all flex items-center gap-2"
            >
              {copied ? <CheckCircle className="w-5 h-5 text-green-400" /> : <Copy className="w-5 h-5" />}
            </button>
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-4 mb-4 flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0" />
              <p className="text-red-200 text-sm">{error}</p>
            </div>
          )}

          {result && (
            <div className="space-y-4">
              <div className="bg-white/5 rounded-lg p-4 border border-white/10">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-purple-200">Strength</span>
                  <span className={`font-bold ${getStrengthColor(result.strength)}`}>
                    {result.strength}
                  </span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-500 ${
                      result.strength === 'Strong' ? 'bg-green-400 w-full' :
                      result.strength === 'Medium' ? 'bg-yellow-400 w-2/3' :
                      'bg-red-400 w-1/3'
                    }`}
                  />
                </div>
                <div className="flex justify-between mt-1 text-xs text-purple-300">
                  <span>Score: {result.score}/100</span>
                </div>
              </div>

              <div className="bg-white/5 rounded-lg p-4 border border-white/10">
                <div className="flex items-center justify-between">
                  <span className="text-purple-200">Risk Level</span>
                  <span className={`font-bold ${getRiskColor(result.risk)}`}>
                    {result.risk}
                  </span>
                </div>
              </div>

              {result.suggestions && result.suggestions.length > 0 && (
                <div className="bg-white/5 rounded-lg p-4 border border-white/10">
                  <h3 className="text-purple-200 font-semibold mb-2 flex items-center gap-2">
                    <Sparkles className="w-4 h-4" />
                    Suggestions
                  </h3>
                  <ul className="space-y-1">
                    {result.suggestions.map((suggestion, index) => (
                      <li key={index} className="text-sm text-purple-300 flex items-start gap-2">
                        <span className="text-purple-400 mt-1">•</span>
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App