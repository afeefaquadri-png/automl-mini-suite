'use client'

import { useState } from 'react'
import DataUpload from './components/DataUpload'
import ModelTraining from './components/ModelTraining'
import Predictions from './components/Predictions'
import ModelComparison from './components/ModelComparison'
import Reports from './components/Reports'

export default function Home() {
  const [activeTab, setActiveTab] = useState('upload')
  const [jobId, setJobId] = useState<string | null>(null)
  const [modelId, setModelId] = useState<string | null>(null)
  const [dataInfo, setDataInfo] = useState<any>(null)

  const tabs = [
    { id: 'upload', name: 'Data Upload', icon: '📊' },
    { id: 'training', name: 'Model Training', icon: '🎯' },
    { id: 'predictions', name: 'Predictions', icon: '🔮' },
    { id: 'comparison', name: 'Model Comparison', icon: '📈' },
    { id: 'reports', name: 'Reports', icon: '📊' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🤖 ML AutoML Suite
          </h1>
          <p className="text-gray-600">
            Comprehensive Machine Learning Platform
          </p>
        </header>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow-md mb-6">
          <nav className="flex space-x-1 p-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 px-4 py-3 rounded-md font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="bg-white rounded-lg shadow-md p-6">
          {activeTab === 'upload' && (
            <DataUpload
              onDataLoaded={(jobId, dataInfo) => {
                setJobId(jobId)
                setDataInfo(dataInfo)
              }}
            />
          )}
          {activeTab === 'training' && (
            <ModelTraining
              jobId={jobId}
              dataInfo={dataInfo}
              onModelTrained={(modelId) => setModelId(modelId)}
            />
          )}
          {activeTab === 'predictions' && (
            <Predictions modelId={modelId} />
          )}
          {activeTab === 'comparison' && (
            <ModelComparison />
          )}
          {activeTab === 'reports' && (
            <Reports modelId={modelId} />
          )}
        </div>
      </div>
    </div>
  )
}
