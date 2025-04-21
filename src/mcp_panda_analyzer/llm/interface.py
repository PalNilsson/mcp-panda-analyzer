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

"""LLM interface definition for the Model Context Protocol."""

from abc import ABC, abstractmethod
from typing import Optional


class LLMInterface(ABC):
    """Abstract base class defining the interface for all LLM implementations."""

    @abstractmethod
    def analyze_text(self, text: str, max_tokens: int = 1000) -> str:
        """
        Analyze text using the LLM.

        Args:
            text: The text to analyze
            max_tokens: Maximum number of tokens to generate

        Returns:
            The generated analysis as a string
        """
        pass

    @property
    @abstractmethod
    def context_length(self) -> int:
        """Return the maximum context length supported by this model."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the name/identifier of this model."""
        pass
