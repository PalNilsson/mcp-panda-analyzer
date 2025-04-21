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

"""Claude LLM implementation."""

import os
import logging
from typing import Optional

from .interface import LLMInterface

logger = logging.getLogger(__name__)


class ClaudeLLM(LLMInterface):
    """Implementation of LLMInterface using Anthropic's Claude models."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "claude-3-opus-20240229"):
        """
        Initialize Claude LLM.

        Args:
            api_key: Anthropic API key (if None, will use environment variable)
            model_name: Claude model to use
        """
        try:
            import anthropic
            self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError("No API key provided for Claude. Set ANTHROPIC_API_KEY environment variable.")

            self._model_name = model_name
            self.client = anthropic.Anthropic(api_key=self.api_key)
            logger.info(f"Initialized Claude LLM with model: {model_name}")
        except ImportError:
            logger.error("Failed to import anthropic package. Please install with: pip install anthropic")
            raise

    def analyze_text(self, text: str, max_tokens: int = 1000) -> str:
        """Analyze text using Claude."""
        try:
            response = self.client.messages.create(
                model=self._model_name,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": text}
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude analysis failed: {e}")
            return f"Analysis failed: {str(e)}"

    @property
    def context_length(self) -> int:
        """Return Claude's context length based on model."""
        # These are approximate values - adjust based on the actual model
        model_context_lengths = {
            "claude-3-opus-20240229": 200000,
            "claude-3-sonnet-20240229": 180000,
            "claude-3-haiku-20240307": 150000,
            "claude-3.5-sonnet-20240620": 200000
        }
        return model_context_lengths.get(self._model_name, 100000)

    @property
    def model_name(self) -> str:
        """Return the model name."""
        return self._model_name
