'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export default function ModelComparison() {
  const [models, setModels] = useState<any[]>([])
  const [selectedModels, setSelectedModels] = useState<string[]>([])
  const [comparisonData, setComparisonData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchModels()
  }, [])

  const fetchModels = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/models`)
      if (response.data.success) {
        setModels(response.data.data)
      }
    } catch (err) {
      console.error('Error fetching models:', err)
    }
  }

  const handleCompare = async () => {
    if (selectedModels.length === 0) return

    setLoading(true)
    try {
      const modelDetails = await Promise.all(
        selectedModels.map((id) =>
          axios.get(`${API_BASE_URL}/api/models/${id}`)
        )
      )

      const comparison = modelDetails.map((response, idx) => {
        const info = response.data.data
        const metrics = info.all_results[info.best_model]?.metrics || {}
        return {
          model: info.best_model,
          ...metrics,
        }
      })

      setComparisonData(comparison)
    } catch (err) {
      console.error('Error comparing models:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Model Comparison</h2>

      {models.length === 0 ? (
        <div className="p-4 bg-yellow-50 text-yellow-700 rounded-md">
          No models available. Train a model first!
        </div>
      ) : (
        <>
          <div className="space-y-4">
            <label className="block text-sm font-medium text-gray-700">
              Select Models to Compare
            </label>
            <div className="grid grid-cols-2 gap-2 max-h-60 overflow-y-auto border rounded-md p-4">
              {models.map((model) => (
                <label key={model.model_id} className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={selectedModels.includes(model.model_id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedModels([...selectedModels, model.model_id])
                      } else {
                        setSelectedModels(
                          selectedModels.filter((id) => id !== model.model_id)
                        )
                      }
                    }}
                    className="rounded"
                  />
                  <span>{model.best_model}</span>
                </label>
              ))}
            </div>

            <button
              onClick={handleCompare}
              disabled={loading || selectedModels.length === 0}
              className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
            >
              {loading ? 'Comparing...' : 'Compare Models'}
            </button>
          </div>

          {comparisonData.length > 0 && (
            <div className="mt-6">
              <h3 className="text-xl font-bold mb-4">Comparison Chart</h3>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={comparisonData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="model" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  {Object.keys(comparisonData[0] || {})
                    .filter((key) => key !== 'model')
                    .map((key, idx) => (
                      <Bar
                        key={key}
                        dataKey={key}
                        fill={`hsl(${idx * 60}, 70%, 50%)`}
                      />
                    ))}
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </>
      )}
    </div>
  )
}
