#Hybrid RAG Application

A containerized Hybrid Retrieval-Augmented Generation (RAG) application built with Streamlit (frontend), FastAPI (backend), and intelligent vector search capabilities. The application allows users to upload PDF documents and interact with their data seamlessly via a chat interface.

🚀 Live Demo
Access the live production application here: https://myhybridrag.online

🛠️ Tech Stack
Frontend: Streamlit (Python)
Backend: FastAPI / Uvicorn (Python)
Containerization: Docker & Docker Compose
Web Server & Reverse Proxy: Nginx
SSL/TLS Security: Let's Encrypt (Certbot)
Hosting: Hostinger VPS (Ubuntu)

📁 Project Structure
Hybrid-RAG-Application/
├── backend/               # FastAPI backend service & RAG logic
├── frontend/              # Streamlit user interface
├── docker-compose.yml     # Docker multi-container orchestration
└── README.md              # Project documentation


⚙️ Getting Started & Local Deployment
To run this application locally using Docker:
Clone the repository:
git clone https://github.com/your-username/Hybrid-RAG-Application.git
cd Hybrid-RAG-Application

Build and start the containers:
docker-compose up --build -d

Access the application:
Frontend: http://localhost:8501
Backend API docs: http://localhost:8000/docs

🌐 Production Deployment Guide (VPS + Nginx + SSL)
If you are deploying this on a Linux VPS (such as Hostinger, DigitalOcean, or AWS):
1. Configure Docker Services: Ensure your docker-compose.yml maps the Streamlit frontend to port 8501.
2. Setup Nginx Reverse Proxy: Configure /etc/nginx/sites-available/default to proxy incoming traffic to http://127.0.0.1:8501, ensuring WebSocket support headers (Upgrade and Connection) are enabled for Streamlit.
3. Secure with SSL: Install and configure a Let's Encrypt SSL certificate using Certbot:  sudo certbot --nginx -d myhybridrag.online
4. Test and Reload Nginx: sudo nginx -t && sudo systemctl reload nginx

sudo nginx -t && sudo systemctl reload nginx

