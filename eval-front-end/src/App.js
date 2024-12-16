import React, {useState, useEffect} from "react";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import EvaluationDashboardCSV from './EvaluationDashboardCSV';
import './App.css';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

const textColor = "lightblue"  //color of text

// Main Component
const EvaluationDashboard = () => {
  const [data, setData] = useState(null);
  
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/output.json');
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, []);

  if (!data) {
    return (
      <div
        style={{
          padding: "20px",
          maxWidth: "900px",
          margin: "auto",
          backgroundColor: "black",
          color: textColor,
          borderRadius: "8px",
        }}
      >
        <h1 style={{ textAlign: "center" }}>RAG Model Evaluation Dashboard</h1>
        <p style={{ textAlign: "center" }}>Loading evaluation results...</p>
      </div>
    );
  }

  const totalQuestions = data.length;
  const averageAccuracy = Math.round(
    (data.reduce((sum, item) => sum + item.accuracy, 0) / totalQuestions) * 10) * 10;
  const averageRelevance = Math.round(
    (data.reduce((sum, item) => sum + item.relevance, 0) / totalQuestions) * 10) * 10;
  const averageGroundedness = Math.round(
    (data.reduce((sum, item) => sum + item.groundedness, 0) / totalQuestions) * 10) * 10;

  const barData = {
    labels: ["Accuracy" , "Relevance", "Groundedness"],
    datasets: [
      {
        data: [
          parseFloat(averageAccuracy),
          parseFloat(averageRelevance),
          parseFloat(averageGroundedness),
        ],
        backgroundColor: ["#4caf50", "#2196f3", "#ff9800"],
      },
    ],
  };

  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        titleColor: "white",
        bodyColor: "white",
        backgroundColor: "rgba(0, 0, 0, 0.8)",
      },
    },
    scales: {
      x: {
        ticks: {
          color: textColor,
        },
        grid: {
          color: "white",
        },
      },
      y: {
        ticks: {
          color: textColor,
        },
        grid: {
          color: "white",
        },
        max: 100,
      },
    },
  };

  return (
    <div
      style={{
        padding: "20px",
        margin: "auto",
        backgroundColor: "black",
        color: textColor,
        borderRadius: "8px",
        maxWidth: "100%",
      }}
    >
      <h1 style={{ textAlign: "center" }}>RAG Model Evaluation Dashboard</h1>

      <div style={{ textAlign: "center", marginTop: "20px",}}>
        <h2>Summary</h2>
        <div
            style={{
            width: "750px",
            height: "380px",
            margin: "0 auto",
            display: "flex",
            alignItems: "center", // Centers vertically within its height
            justifyContent: "center", // Centers horizontally
            padding: "10px",
            }}
        >
            <Bar data={barData} options={barChartOptions} />
        </div>
        <p>Total Questions: {totalQuestions}</p>
        <p>Average Accuracy: {averageAccuracy}%</p>
        <p>Average Relevance: {averageRelevance}%</p>
        <p>Average Groundedness: {averageGroundedness}%</p>
        </div>

      <div style={{ marginTop: "40px" }}>
        <h2 style={{ textAlign: "center" }}>Evaluation Results</h2>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            marginTop: "20px",
            color: textColor,
          }}
        >
          <thead>
            <tr style={{ backgroundColor: "#333", textAlign: "left" }}>
              <th style={{ padding: "10px", border: "1px solid #555" }}>Question</th>
              <th style={{ padding: "10px", border: "1px solid #555" }}>Correct Answer</th>
              <th style={{ padding: "10px", border: "1px solid #555" }}>Generated Answer</th>
              <th style={{ padding: "10px", border: "1px solid #555" }}>Accuracy</th>
              <th style={{ padding: "10px", border: "1px solid #555" }}>Relevance</th>
              <th style={{ padding: "10px", border: "1px solid #555" }}>Groundedness</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr
                key={index}
                style={{ backgroundColor: index % 2 === 0 ? "#222" : "#444" }}
              >
                <td style={{ padding: "10px", border: "1px solid #555" }}>{item.question}</td>
                <td style={{ padding: "10px", border: "1px solid #555" }}>{item.answer}</td>
                <td style={{ padding: "10px", border: "1px solid #555" }}>{item.generated_answer}</td>
                <td style={{ padding: "10px", border: "1px solid #555" }}>{(item.accuracy * 100).toFixed(2)}%</td>
                <td style={{ padding: "10px", border: "1px solid #555" }}>{(item.relevance * 100).toFixed(2)}%</td>
                <td style={{ padding: "10px", border: "1px solid #555" }}>{(item.groundedness * 100).toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EvaluationDashboard;