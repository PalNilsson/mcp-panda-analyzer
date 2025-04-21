#!/usr/bin/env python
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Authors:
# - Paul Nilsson, paul.nilsson@cern.ch, 2025

"""FastAPI server implementation for the MCP PanDA Analyzer."""

import os
import argparse
import logging
from typing import Optional, List, Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ..llm.factory import LLMFactory
from .service import download_log_file, extract_important_sections, create_analysis_prompt

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp-server")

# Constants
HARDCODED_JOB_ID = 6610588906
DEFAULT_LOG_FILE = "pilotlog.txt"

# Create the FastAPI application
app = FastAPI(
    title="MCP Grid Job Failure Analyzer",
    description="Analyze PanDA grid job failures using LLMs with Model Context Protocol",
    version="0.1.0"
)


class JobAnalysisRequest(BaseModel):
    job_id: Optional[int] = HARDCODED_JOB_ID
    filename: Optional[str] = DEFAULT_LOG_FILE
    llm_type: Optional[str] = "claude"  # Default LLM to use


class JobAnalysisResponse(BaseModel):
    job_id: int
    filename: str
    analysis_result: str
    file_size: int
    analysis_method: str  # "full" or "rag"
    llm_type: str


@app.post("/analyze_job", response_model=JobAnalysisResponse)
def analyze_job(request: JobAnalysisRequest) -> JobAnalysisResponse:
    """Analyze a grid job failure by downloading and processing the log file."""
    job_id = request.job_id
    filename = request.filename
    llm_type = request.llm_type

    logger.info(f"Starting analysis for job ID: {job_id}, file: {filename}, using LLM: {llm_type}")

    try:
        # Create LLM instance
        llm = LLMFactory.create_llm(llm_type)

        # Download the log file
        log_content = download_log_file(job_id, filename)
        file_size = len(log_content)

        logger.info(f"Downloaded log file. Size: {file_size} characters")

        # Determine if we need RAG based on the LLM's context length
        if file_size > llm.context_length:
            logger.info(f"Log file too large ({file_size} chars), using RAG to extract important sections")
            extracted_content = extract_important_sections(log_content)
            prompt = create_analysis_prompt(extracted_content, job_id, filename)
            analysis_result = llm.analyze_text(prompt)
            analysis_method = "rag"
        else:
            logger.info(f"Log file size ({file_size} chars) within context window, using full content")
            prompt = create_analysis_prompt(log_content, job_id, filename)
            analysis_result = llm.analyze_text(prompt)
            analysis_method = "full"

        # Return the analysis result
        return JobAnalysisResponse(
            job_id=job_id,
            filename=filename,
            analysis_result=analysis_result,
            file_size=file_size,
            analysis_method=analysis_method,
            llm_type=llm_type
        )

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/")
def root():
    """Root endpoint to check if the server is running."""
    return {
        "status": "ok",
        "message": "MCP Grid Job Failure Analyzer is running",
        "available_llms": LLMFactory.available_llms()
    }


def main():
    """Entry point for the server application."""
    parser = argparse.ArgumentParser(description="MCP Grid Job Failure Analyzer Server")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--host", default="0.0.0.0", help="Server host")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging level")
    parser.add_argument("--llm", default="claude", help="Default LLM type to use")
    parser.add_argument("--model-path", help="Path to model file (for Llama)")
    parser.add_argument("--model-name", help="Model name (for Claude/OpenAI)")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=getattr(logging, args.log_level))

    # Set environment variables based on arguments
    if args.model_path:
        os.environ["LLAMA_MODEL_PATH"] = args.model_path

    print(f"Starting MCP server on {args.host}:{args.port}...")
    print(f"Available LLM backends: {', '.join(LLMFactory.available_llms())}")

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
