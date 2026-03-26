# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main_mcp.py .
COPY sample_data.py .
COPY models.py .

# Expose port 8080 (IBM Cloud Code Engine default)
EXPOSE 8080

# Set environment variable for port
ENV PORT=8080

# Run the MCP server with SSE transport
CMD python main_mcp.py --host 0.0.0.0 --port ${PORT} --path /mcp --transport sse