import React, { useState } from 'react';
import { Plus, Trash2, Save, Download, Upload, Play, PlayCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './card.jsx';
import Papa from 'papaparse';
import './App.css';

const EvaluationDashboardCSV = () => {
  const [testCases, setTestCases] = useState([]);
  const [selectedTestCase, setSelectedTestCase] = useState(null);
  const [evaluationResults, setEvaluationResults] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        // Skip first two rows
        const newTestCases = results.data.slice(2).map((row, index) => ({
          id: index + 1,
          input: row['Question'] || '',
          expectedOutput: row['Answer'] || '',
          actualOutput: '',
          groundTruthPhrases: row['Ground Truth phrases'] 
            ? row['Ground Truth phrases'].split(',').map(phrase => phrase.trim()) 
            : [],
          relevantDocuments: row['Relevant Documents (File names)'] 
            ? row['Relevant Documents (File names)'].split(',').map(doc => doc.trim()) 
            : [],
          metrics: {
            relevance: 0,
            coherence: 0,
            groundedness: 0,
            context_recall: 0
          }
        }));

        setTestCases(newTestCases);
      },
      error: (error) => {
        console.error('CSV parsing error:', error);
        alert('Error parsing CSV file');
      }
    });
  };

  const addTestCase = () => {
    const newId = testCases.length > 0 ? Math.max(...testCases.map(tc => tc.id)) + 1 : 1;
    setTestCases([...testCases, {
      id: newId,
      input: '',
      expectedOutput: '',
      actualOutput: '',
      groundTruthPhrases: [],
      relevantDocuments: [],
      metrics: {
        relevance: 0,
        coherence: 0,
        groundedness: 0,
        context_recall: 0
      }
    }]);
  };

  const evaluateTestCase = (testCase) => {
    const updatedTestCase = {
      ...testCase,
      actualOutput: 'Evaluation result placeholder',
      metrics: {
        relevance: 0,
        coherence: 0,
        groundedness: 0,
        context_recall: 0
      }
    };

    setTestCases(prevTestCases => 
      prevTestCases.map(tc => 
        tc.id === testCase.id ? updatedTestCase : tc
      )
    );
  };

  const evaluateAllTestCases = () => {
    const updatedTestCases = testCases.map(testCase => ({
      ...testCase,
      actualOutput: 'Evaluation result placeholder',
      metrics: {
        relevance: 0,
        coherence: 0,
        groundedness: 0,
        context_recall: 0
      }
    }));

    setTestCases(updatedTestCases);
  };

  const updateTestCase = (id, field, value) => {
    setTestCases(testCases.map(tc => 
      tc.id === id ? { ...tc, [field]: value } : tc
    ));
  };

  const removeTestCase = (id) => {
    setTestCases(testCases.filter(tc => tc.id !== id));
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">Upload Test Data Below</h2>
          <div className="space-x-2">
            <input 
              type="file" 
              accept=".csv" 
              onChange={handleFileUpload} 
              className="hidden" 
              id="csv-upload"
            />
            <label 
              htmlFor="csv-upload" 
              className="px-4 py-2 bg-green-600 text-white rounded-md flex items-center gap-2 hover:bg-green-700 cursor-pointer"
            >
              <Upload size={16} /> Upload CSV
            </label>
            <button 
              className="px-4 py-2 bg-blue-600 text-white rounded-md flex items-center gap-2 hover:bg-blue-700"
              onClick={addTestCase}
              style={{marginLeft: '20px'}}
            >
              <Plus size={16} /> Add Test Case
            </button>
            {testCases.length > 0 && (
              <button 
                className="px-4 py-2 bg-blue-600 text-white rounded-md flex items-center gap-2 hover:bg-blue-700"
                onClick={evaluateAllTestCases}
                style={{marginLeft: '20px'}}
              >
                <Play size={16} /> Evaluate All
              </button>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6">
          {testCases.map((testCase) => (
            <Card key={testCase.id} className="shadow-md">
              <CardHeader className="flex flex-row items-center justify-between">
                <div className="flex items-center space-x-2">
                  <CardTitle>Test Case #{testCase.id}</CardTitle>
                  <button 
                    className="text-blue-600 hover:text-blue-800"
                    onClick={() => evaluateTestCase(testCase)}
                    style={{marginRight: "5px"}}
                  >
                    <PlayCircle size={16} />
                  </button>
                  <button 
                    className="text-red-500 hover:text-red-700"
                    onClick={() => removeTestCase(testCase.id)}
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div class="row">
                <div class="column">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2" style={{ paddingRight: '20px'}}>Input Query</label>
                    <textarea
                      className="w-full p-2 border rounded-md h-24"
                      value={testCase.input}
                      onChange={(e) => updateTestCase(testCase.id, 'input', e.target.value)}
                      placeholder="Enter your test query..."
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2" style={{ paddingRight: '20px'}}>Expected Output</label>
                    <textarea
                      className="w-full p-2 border rounded-md h-24"
                      value={testCase.expectedOutput}
                      onChange={(e) => updateTestCase(testCase.id, 'expectedOutput', e.target.value)}
                      placeholder="Enter expected response..."
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2" style={{ paddingRight: '20px'}}>Ground Truth Phrases</label>
                    <textarea
                      className="w-full p-2 border rounded-md h-24"
                      value={testCase.groundTruthPhrases.join(', ')}
                      onChange={(e) => updateTestCase(testCase.id, 'groundTruthPhrases', e.target.value.split(',').map(p => p.trim()))}
                      placeholder="Enter ground truth phrases..."
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2" style={{ paddingRight: '20px'}}>Relevant Documents</label>
                    <textarea
                      className="w-full p-2 border rounded-md h-24"
                      value={testCase.relevantDocuments.join(', ')}
                      onChange={(e) => updateTestCase(testCase.id, 'relevantDocuments', e.target.value.split(',').map(d => d.trim()))}
                      placeholder="Enter relevant document filenames..."
                    />
                  </div>
                </div>
                </div>

                <div class="column">
                <div className="bg-gray-50 p-4 rounded-md">
                  <h4 className="font-medium mb-2">Evaluation Metrics</h4>
                  <div className="grid grid-cols-4 gap-4">
                    <div>
                      <label className="block text-sm text-gray-600">Relevance</label>
                      <div className="text-lg font-medium">{testCase.metrics.relevance.toFixed(2)}</div>
                    </div>
                    <div>
                      <label className="block text-sm text-gray-600">Coherence</label>
                      <div className="text-lg font-medium">{testCase.metrics.coherence.toFixed(2)}</div>
                    </div>
                    <div>
                      <label className="block text-sm text-gray-600">Groundedness</label>
                      <div className="text-lg font-medium">{testCase.metrics.groundedness.toFixed(2)}</div>
                    </div>
                    <div>
                      <label className="block text-sm text-gray-600">Context Recall</label>
                      <div className="text-lg font-medium">{testCase.metrics.context_recall.toFixed(2)}</div>
                    </div>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2" style={{ paddingRight: '20px'}}>Actual Output</label>
                  <textarea
                    className="w-full p-2 border rounded-md h-24 bg-gray-50"
                    value={testCase.actualOutput}
                    readOnly
                    placeholder="Actual response will appear after evaluation..."
                  />
                </div>
                </div>
                </div>
                <hr />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EvaluationDashboardCSV;