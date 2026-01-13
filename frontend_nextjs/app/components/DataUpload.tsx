'use client'

import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

interface DataUploadProps {
  onDataLoaded: (jobId: string, dataInfo: any) => void
}

export default function DataUpload({ onDataLoaded }: DataUploadProps) {
  const [uploadMethod, setUploadMethod] = useState<'file' | 'mongodb' | 'postgresql'>('file')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  // MongoDB state
  const [mongoConnection, setMongoConnection] = useState('')
  const [mongoDatabase, setMongoDatabase] = useState('')
  const [mongoCollection, setMongoCollection] = useState('')

  // PostgreSQL state
  const [pgConnection, setPgConnection] = useState('')
  const [pgTable, setPgTable] = useState('')
  const [pgQuery, setPgQuery] = useState('')

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/json': ['.json'],
    },
    onDrop: async (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        await handleFileUpload(acceptedFiles[0])
      }
    },
  })

  const handleFileUpload = async (file: File) => {
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post(`${API_BASE_URL}/api/data/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      if (response.data.success) {
        setSuccess(true)
        onDataLoaded(response.data.data.job_id, response.data.data.data_info)
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error uploading file')
    } finally {
      setLoading(false)
    }
  }

  const handleMongoDBLoad = async () => {
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/data/database`, {
        type: 'mongodb',
        connection_string: mongoConnection,
        database: mongoDatabase,
        collection: mongoCollection,
      })

      if (response.data.success) {
        setSuccess(true)
        onDataLoaded(response.data.data.job_id, response.data.data.data_info)
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error loading from MongoDB')
    } finally {
      setLoading(false)
    }
  }

  const handlePostgreSQLLoad = async () => {
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/data/database`, {
        type: 'postgresql',
        connection_string: pgConnection,
        table: pgTable,
        query: pgQuery || null,
      })

      if (response.data.success) {
        setSuccess(true)
        onDataLoaded(response.data.data.job_id, response.data.data.data_info)
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error loading from PostgreSQL')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Data Upload</h2>

      {/* Method Selection */}
      <div className="flex space-x-4">
        <button
          onClick={() => setUploadMethod('file')}
          className={`px-4 py-2 rounded-md ${
            uploadMethod === 'file'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          File Upload
        </button>
        <button
          onClick={() => setUploadMethod('mongodb')}
          className={`px-4 py-2 rounded-md ${
            uploadMethod === 'mongodb'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          MongoDB
        </button>
        <button
          onClick={() => setUploadMethod('postgresql')}
          className={`px-4 py-2 rounded-md ${
            uploadMethod === 'postgresql'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          PostgreSQL
        </button>
      </div>

      {/* File Upload */}
      {uploadMethod === 'file' && (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
        >
          <input {...getInputProps()} />
          <p className="text-gray-600">
            {isDragActive
              ? 'Drop the file here...'
              : 'Drag & drop a file here, or click to select'}
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Supports CSV, Excel, JSON
          </p>
        </div>
      )}

      {/* MongoDB */}
      {uploadMethod === 'mongodb' && (
        <div className="space-y-4">
          <input
            type="password"
            placeholder="Connection String"
            value={mongoConnection}
            onChange={(e) => setMongoConnection(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
          />
          <input
            type="text"
            placeholder="Database"
            value={mongoDatabase}
            onChange={(e) => setMongoDatabase(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
          />
          <input
            type="text"
            placeholder="Collection"
            value={mongoCollection}
            onChange={(e) => setMongoCollection(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
          />
          <button
            onClick={handleMongoDBLoad}
            disabled={loading}
            className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Load from MongoDB'}
          </button>
        </div>
      )}

      {/* PostgreSQL */}
      {uploadMethod === 'postgresql' && (
        <div className="space-y-4">
          <input
            type="password"
            placeholder="Connection String"
            value={pgConnection}
            onChange={(e) => setPgConnection(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
          />
          <input
            type="text"
            placeholder="Table Name"
            value={pgTable}
            onChange={(e) => setPgTable(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
          />
          <textarea
            placeholder="Custom Query (optional)"
            value={pgQuery}
            onChange={(e) => setPgQuery(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            rows={3}
          />
          <button
            onClick={handlePostgreSQLLoad}
            disabled={loading}
            className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Load from PostgreSQL'}
          </button>
        </div>
      )}

      {/* Status Messages */}
      {loading && (
        <div className="p-4 bg-blue-50 text-blue-700 rounded-md">
          Processing...
        </div>
      )}
      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-md">
          {error}
        </div>
      )}
      {success && (
        <div className="p-4 bg-green-50 text-green-700 rounded-md">
          Data loaded successfully!
        </div>
      )}
    </div>
  )
}
