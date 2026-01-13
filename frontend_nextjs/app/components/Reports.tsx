'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

interface ReportsProps {
  modelId: string | null
}

export default function Reports({ modelId: modelIdProp }: ReportsProps) {
  const [models, setModels] = useState<any[]>([])
  const [selectedModelId, setSelectedModelId] = useState<string | null>(modelIdProp)
  const [modelDetails, setModelDetails] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchModels()
    if (selectedModelId) {
      fetchModelDetails(selectedModelId)
    }
  }, [selectedModelId])

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

  const fetchModelDetails = async (id: string) => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_BASE_URL}/api/models/${id}`)
      if (response.data.success) {
        setModelDetails(response.data.data)
      }
    } catch (err) {
      console.error('Error fetching model details:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Model Reports</h2>

      {models.length === 0 ? (
        <div className="p-4 bg-yellow-50 text-yellow-700 rounded-md">
          No models available.
        </div>
      ) : (
        <>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Model
            </label>
            <select
              value={selectedModelId || ''}
              onChange={(e) => setSelectedModelId(e.target.value)}
              className="w-full px-4 py-2 border rounded-md"
            >
              <option value="">Select a model</option>
              {models.map((model) => (
                <option key={model.model_id} value={model.model_id}>
                  {model.best_model} ({model.problem_type})
                </option>
              ))}
            </select>
          </div>

          {loading && (
            <div className="p-4 bg-blue-50 text-blue-700 rounded-md">
              Loading...
            </div>
          )}

          {modelDetails && (
            <div className="mt-6 space-y-6">
              <div className="p-4 bg-green-50 rounded-md">
                <h3 className="text-xl font-bold mb-2">
                  {modelDetails.best_model} ({modelDetails.problem_type})
                </h3>
              </div>

              <div>
                <h4 className="text-lg font-semibold mb-4">Metrics</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {Object.entries(
                    modelDetails.all_results[modelDetails.best_model]?.metrics || {}
                  ).map(([key, value]: [string, any]) => (
                    <div
                      key={key}
                      className="p-4 bg-gray-50 rounded-md"
                    >
                      <div className="text-sm text-gray-600">
                        {key.replace('test_', '').replace('_', ' ').toUpperCase()}
                      </div>
                      <div className="text-2xl font-bold text-gray-800">
                        {typeof value === 'number' ? value.toFixed(4) : value}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="text-lg font-semibold mb-4">All Model Results</h4>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                          Model
                        </th>
                        {Object.keys(
                          modelDetails.all_results[
                            Object.keys(modelDetails.all_results)[0]
                          ]?.metrics || {}
                        ).map((metric) => (
                          <th
                            key={metric}
                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                          >
                            {metric.replace('test_', '').replace('_', ' ')}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {Object.entries(modelDetails.all_results).map(
                        ([name, result]: [string, any]) => (
                          <tr key={name}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                              {name}
                            </td>
                            {Object.values(result.metrics || {}).map(
                              (value: any, idx) => (
                                <td
                                  key={idx}
                                  className="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                                >
                                  {typeof value === 'number'
                                    ? value.toFixed(4)
                                    : value}
                                </td>
                              )
                            )}
                          </tr>
                        )
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
