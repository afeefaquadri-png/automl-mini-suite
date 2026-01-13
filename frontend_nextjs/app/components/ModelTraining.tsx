'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

interface ModelTrainingProps {
  jobId: string | null
  dataInfo: any
  onModelTrained: (modelId: string) => void
}

export default function ModelTraining({ jobId, dataInfo, onModelTrained }: ModelTrainingProps) {
  const [XColumns, setXColumns] = useState<string[]>([])
  const [yColumn, setYColumn] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (dataInfo) {
      // Auto-select all columns except first as X, first as y
      const columns = dataInfo.columns || []
      if (columns.length > 0) {
        setYColumn(columns[columns.length - 1])
        setXColumns(columns.slice(0, -1))
      }
    }
  }, [dataInfo])

  const handleTrain = async () => {
    if (!jobId || XColumns.length === 0 || !yColumn) {
      setError('Please select columns')
      return
    }

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/train`, {
        job_id: jobId,
        X_columns: XColumns,
        y_column: yColumn,
      })

      if (response.data.success) {
        setResults(response.data.data)
        onModelTrained(response.data.data.model_id)
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error training models')
    } finally {
      setLoading(false)
    }
  }

  if (!jobId) {
    return (
      <div className="p-4 bg-yellow-50 text-yellow-700 rounded-md">
        Please upload data first!
      </div>
    )
  }

  const columns = dataInfo?.columns || []

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Model Training</h2>

      {/* Column Selection */}
      <div className="grid grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            X Columns (Features)
          </label>
          <div className="border rounded-md p-4 max-h-60 overflow-y-auto">
            {columns.map((col: string) => (
              <label key={col} className="flex items-center space-x-2 py-1">
                <input
                  type="checkbox"
                  checked={XColumns.includes(col)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setXColumns([...XColumns, col])
                    } else {
                      setXColumns(XColumns.filter((c) => c !== col))
                    }
                  }}
                  disabled={col === yColumn}
                  className="rounded"
                />
                <span className={col === yColumn ? 'text-gray-400' : ''}>
                  {col}
                </span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Y Column (Target)
          </label>
          <select
            value={yColumn}
            onChange={(e) => setYColumn(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
          >
            <option value="">Select target column</option>
            {columns.map((col: string) => (
              <option key={col} value={col}>
                {col}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button
        onClick={handleTrain}
        disabled={loading || XColumns.length === 0 || !yColumn}
        className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
      >
        {loading ? 'Training Models...' : 'Train Models'}
      </button>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-md">{error}</div>
      )}

      {results && (
        <div className="mt-6">
          <h3 className="text-xl font-bold mb-4">Training Results</h3>
          <div className="p-4 bg-green-50 text-green-700 rounded-md mb-4">
            Best Model: <strong>{results.best_model}</strong>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Model
                  </th>
                  {Object.keys(results.results[Object.keys(results.results)[0]]?.metrics || {}).map(
                    (metric) => (
                      <th
                        key={metric}
                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                      >
                        {metric.replace('test_', '').replace('_', ' ').toUpperCase()}
                      </th>
                    )
                  )}
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    CV Score
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {Object.entries(results.results).map(([name, result]: [string, any]) => (
                  <tr key={name}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {name}
                    </td>
                    {Object.values(result.metrics).map((value: any, idx) => (
                      <td key={idx} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {typeof value === 'number' ? value.toFixed(4) : value}
                      </td>
                    ))}
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {result.cv_mean.toFixed(4)} (±{result.cv_std.toFixed(4)})
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
