"""Docker 容器化构建器"""
import os

class DockerBuilder:
    @staticmethod
    def generate_dockerfile():
        return """FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "pytest", "tests/"]
"""

    @staticmethod
    def generate_compose():
        return """version: '3.8'
services:
  bearski:
    build: .
    volumes:
      - ./reports:/app/reports
      - ./screenshots:/app/screenshots
    environment:
      - BEARSKI_PARALLEL_WORKERS=4
"""

    @staticmethod
    def generate_requirements():
        return """selenium==4.15.0
requests==2.31.0
psutil==5.9.6
"""

    @staticmethod
    def save_all(output_dir="."):
        os.makedirs(output_dir, exist_ok=True)
        
        with open(f"{output_dir}/Dockerfile", "w") as f:
            f.write(DockerBuilder.generate_dockerfile())
        
        with open(f"{output_dir}/docker-compose.yml", "w") as f:
            f.write(DockerBuilder.generate_compose())
        
        with open(f"{output_dir}/requirements.txt", "w") as f:
            f.write(DockerBuilder.generate_requirements())
        
        return ["Dockerfile", "docker-compose.yml", "requirements.txt"]
