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

"""Example script for using the MCP PanDA Analyzer."""

import os
import sys
from mcp_panda_analyzer.client.agent import MCPAgent


def main():
    """Run a basic job analysis example."""
    # Set your API key if using Claude or OpenAI
    # os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

    # Initialize the agent
    agent = MCPAgent(server_url="http://localhost:8000")

    # Check server status
    server_status = agent.check_server_status()
    if server_status.get("status") != "ok":
        print(f"Error: MCP server is not available: {server_status.get('message')}")
        sys.exit(1)

    print(f"Server is available: {server_status.get('message')}")
    print(f"Available LLMs: {server_status.get('available_llms', [])}")

    # Analyze a job
    job_id = 6610588906  # Example job ID
    filename = "pilotlog.txt"
    llm_type = "claude"  # Use claude, llama, or openai

    print(f"Analyzing job {job_id} using {llm_type}...")
    results = agent.analyze_job(job_id, filename, llm_type)

    # Display the results
    agent.display_analysis_results(results)


if __name__ == "__main__":
    main()
