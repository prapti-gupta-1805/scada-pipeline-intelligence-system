# SCADA Pipeline Intelligence System

## Presentation Summary

This project is a proof-of-concept SCADA analytics platform designed to show how machine learning can support industrial pipeline operations. It combines a React-based frontend with a FastAPI backend to provide an end-to-end demo experience for fault classification, anomaly detection, and predictive maintenance.

The goal is not to replace a full industrial control system, but to demonstrate how AI-driven insights can help operators and engineers make faster, more informed decisions.

---

## One-Line Executive Summary

A full-stack AI demo for pipeline monitoring that uses machine learning to detect faults, identify anomalies, and predict maintenance risk from SCADA-style telemetry data.

---

## What the Project Does

The system allows users to:

- Classify likely pipeline faults from telemetry inputs
- Detect abnormal operating behavior using anomaly scoring
- Estimate equipment maintenance risk and intervention needs
- Review model outputs and explainability signals through a web dashboard

This makes the project useful as both a technical showcase and a functional prototype for AI-enabled operations monitoring.

---

## Why It Matters

Industrial environments generate huge volumes of sensor data, but manually analyzing that data is slow and error-prone. This project illustrates how AI can help:

- surface unusual operating conditions early
- reduce time spent on manual diagnosis
- support preventive maintenance planning
- provide a clearer view of model-backed decision support

---

## Core Features

### 1. Fault Classification
- Uses SCADA measurements such as pressure, flow rate, temperature, valve state, and pump state
- Implements a supervised classification workflow using a serialized scikit-learn classifier and scaler
- Predicts likely fault categories and confidence levels
- Includes class probability outputs and explainability features

### 2. Anomaly Detection
- Monitors telemetry for unusual patterns
- Uses an Isolation Forest model for unsupervised anomaly scoring
- Detects deviations from normal behavior and provides risk classification and top deviating features

### 3. Predictive Maintenance
- Estimates maintenance condition and intervention urgency
- Uses an XGBoost model with categorical encoders for condition prediction
- Takes pipeline and material characteristics, degradation indicators, and operating history into account
- Supports planned maintenance decision-making

### 4. Explainability
- SHAP-based explanations are included in the inference workflow to make model outputs more interpretable
- The analytics view also presents model-related artifacts such as confusion matrices, feature importance charts, and summary visuals

### 4. Web Dashboard
- Interactive frontend built with React and Vite
- Dedicated pages for dashboard overview, fault analysis, anomaly review, analytics, maintenance assessment, and project information
- Backend APIs expose model inference and metadata endpoints

---

## Architecture Overview

The repository is structured into four main areas:

- Frontend: React + Vite + Tailwind CSS for the user interface
- Backend: FastAPI server exposing inference routes and metadata endpoints
- Models: serialized inference modules and model artifacts for each workflow
- Data: sample CSV datasets used for model development and demo purposes

### Runtime Flow
1. A user interacts with the dashboard.
2. The frontend sends input data to the FastAPI backend.
3. The backend validates the payload and routes it to the appropriate model workflow.
4. The model returns predictions, probabilities, and explainability-related outputs.

---

## Tech Stack

### Frontend
- React
- Vite
- Tailwind CSS
- React Router DOM
- Axios
- Recharts
- Lucide React
- Framer Motion

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### Machine Learning
- scikit-learn
- XGBoost
- SHAP
- Isolation Forest
- Pandas
- NumPy
- Matplotlib

---

## Project Structure

- backend/: FastAPI application, API routes, schemas, services, and utilities
- frontend/: React app and UI components
- models/: model inference scripts and artifacts
- data/: sample datasets used to support the workflows
- README.md: project documentation and setup instructions

---

## Demo Narrative for a Manager

You can present the project like this:

> This project demonstrates how AI can be applied to industrial SCADA data to support pipeline operations. It combines telemetry-based analytics with a user-friendly web interface to show how the system can classify faults, detect anomalies, and estimate maintenance needs. The solution is currently a proof-of-concept, but it clearly illustrates the value of data-driven monitoring and decision support in operational environments.

---

## Current Status

The project is currently in a working proof-of-concept state with:

- functional frontend pages and navigation
- working backend inference endpoints
- model-backed prediction workflows
- analytics and explainability visual components

It is suitable for demonstration, portfolio presentation, and technical discussion, but it is not presented here as a production-ready industrial deployment.

---

## Suggested Talking Points

- This is a practical example of applying AI to real operational data.
- The system spans the full stack: frontend, backend, ML inference, and visualization.
- It demonstrates end-to-end thinking from data input to decision support.
- The project is modular and easy to extend with additional models or features.
- It is a strong example of applied machine learning in a domain-focused setting.

---

## Future Enhancements

Possible next steps include:

- adding authentication and role-based access
- integrating with live SCADA systems
- adding historical trend monitoring and alerting
- improving model retraining and deployment workflows
- adding automated testing and CI/CD

---

## Closing Note

This repository is best described as a polished, presentation-ready prototype that shows how AI can support pipeline monitoring and maintenance planning. It is strong evidence of technical execution, full-stack integration, and applied machine learning thinking.
