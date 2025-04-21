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

import argparse
import json
import logging
import os
import sys
import requests
from typing import Dict, Any, Optional, Union

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp-agent")


class MCPAgent:
    """
    MCP Agent for communicating with the MCP server to analyze grid job failures.
    """

    def __init__(self, server_url: str = "http://localhost:8000"):
        """
        Initialize the MCP Agent.

        Args:
            server_url: URL of the MCP server
        """
        self.server_url = server_url
        logger.info(f"MCP Agent initialized with server URL: {server_url}")

    def check_server_status(self) -> Dict[str, Any]:
        """
        Check if the MCP server is available and get available LLMs.

        Returns:
            Dict containing server status information
        """
        try:
            response = requests.get(f"{self.server_url}/")
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "message": f"Server returned status code {response.status_code}"}
        except requests.RequestException as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            return {"status": "error", "message": f"Failed to connect to server: {str(e)}"}

    def analyze_job(self, job_id: int, filename: str = "pilotlog.txt", llm_type: str = "claude") -> Dict[str, Any]:
        """
        Request job analysis from the MCP server.

        Args:
            job_id: PanDA job ID to analyze
            filename: Log filename to analyze
            llm_type: Type of LLM to use

        Returns:
            Dict containing the analysis results
        """
        logger.info(f"Requesting analysis for job ID: {job_id}, file: {filename}, using LLM: {llm_type}")

        data = {
            "job_id": job_id,
            "filename": filename,
            "llm_type": llm_type
        }

        try:
            response = requests.post(
                f"{self.server_url}/analyze_job",
                json=data
            )

            if response.status_code == 200:
                return response.json()
            else:
                error_msg = f"Server returned error {response.status_code}: {response.text}"
                logger.error(error_msg)
                return {"error": error_msg}

        except requests.RequestException as e:
            error_msg = f"Request to MCP server failed: {e}"
            logger.error(error_msg)
            return {"error": error_msg}

    def display_analysis_results(self, results: Dict[str, Any]) -> None:
        """
        Display the job analysis results in a formatted way.

        Args:
            results: Analysis results from the server
        """
        if "error" in results:
            print(f"\n❌ Error: {results['error']}")
            return

        print("\n" + "=" * 70)
        print(f"📊 Analysis Results for PanDA Job: {results['job_id']}")
        print("=" * 70)
        print(f"📄 Log file: {results['filename']}")
        print(f"📏 File size: {results['file_size']} characters")
        print(f"🤖 LLM used: {results['llm_type']}")
        print(
            f"🔍 Analysis method: {'RAG-based extraction' if results['analysis_method'] == 'rag' else 'Full content analysis'}")
        print("\n" + "-" * 70)
        print("📝 Analysis:")
        print("-" * 70)
        print(results['analysis_result'])
        print("=" * 70)


def main():
    """
    Main function for running the MCP Agent as a CLI tool.
    """
    parser = argparse.ArgumentParser(description="MCP Agent for Grid Job Failure Analysis")
    parser.add_argument("--server", default="http://localhost:8000", help="MCP server URL")
    parser.add_argument("--job-id", type=int, default=6610588906, help="PanDA job ID to analyze")
    parser.add_argument("--filename", default="pilotlog.txt", help="Log filename to analyze")
    parser.add_argument("--llm", default="claude", help="LLM type to use")

    args = parser.parse_args()

    # Initialize the agent
    agent = MCPAgent(server_url=args.server)

    # Check if the server is available
    server_status = agent.check_server_status()
    if server_status.get("status") != "ok":
        print(f"❌ MCP server is not available: {server_status.get('message', 'Unknown error')}")
        sys.exit(1)

    print(f"✅ MCP server is available: {server_status.get('message')}")

    # Check if the requested LLM is available
    available_llms = server_status.get("available_llms", [])
    if available_llms and args.llm not in available_llms:
        print(
            f"⚠️  Warning: Requested LLM '{args.llm}' may not be available. Available LLMs: {', '.join(available_llms)}")

    # Request job analysis
    print(f"🔍 Analyzing PanDA job {args.job_id}, file: {args.filename}, using LLM: {args.llm}...")
    results = agent.analyze_job(args.job_id, args.filename, args.llm)

    # Display the results
    agent.display_analysis_results(results)


if __name__ == "__main__":
    main()
