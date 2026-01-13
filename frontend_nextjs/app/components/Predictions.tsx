'use client'

import { useState } from 'react'
import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

interface PredictionsProps {
  modelId: string | null
}

export default function Predictions({ modelId }: PredictionsProps) {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [predictions, setPredictions] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handlePredict = async () => {
    if (!modelId || !file) {
      setError('Please select a model and file')
      return
    }

    setLoading(true)
    setError(null)
    setPredictions(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      // Read file and convert to JSON
      const text = await file.text()
      const lines = text.split('\n')
      const headers = lines[0].split(',')
      const data = lines.slice(1).map((line) => {
        const values = line.split(',')
        return headers.reduce((obj, header, idx) => {
          obj[header.trim()] = values[idx]?.trim() || ''
          return obj
        }, {} as any)
      })

      const response = await axios.post(`${API_BASE_URL}/api/predict`, {
        model_id: modelId,
        data: data,
      })

      if (response.data.success) {
        setPredictions(response.data.data.predictions)
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error making predictions')
    } finally {
      setLoading(false)
    }
  }

  if (!modelId) {
    return (
      <div className="p-4 bg-yellow-50 text-yellow-700 rounded-md">
        Please train a model first!
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Predictions</h2>

      <div className="space-y-4">
        <input
          type="file"
          accept=".csv,.json"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
        />

        <button
          onClick={handlePredict}
          disabled={loading || !file}
          className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
        >
          {loading ? 'Predicting...' : 'Make Predictions'}
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-md">{error}</div>
      )}

      {predictions && (
        <div className="mt-6">
          <h3 className="text-xl font-bold mb-4">Predictions</h3>
          <div className="bg-gray-50 rounded-md p-4">
            <pre className="text-sm overflow-x-auto">
              {JSON.stringify(predictions, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
