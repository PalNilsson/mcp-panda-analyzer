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

"""Factory for creating LLM instances."""

import logging
from typing import Dict, Type, Optional, Any

from .interface import LLMInterface

logger = logging.getLogger(__name__)


class LLMFactory:
    """Factory for creating LLM instances."""

    # Will be populated with available LLM implementations
    _llm_registry: Dict[str, Type[LLMInterface]] = {}

    @classmethod
    def register(cls, name: str):
        """
        Decorator to register an LLM implementation.

        Args:
            name: Name to register the LLM under

        Returns:
            Decorator function
        """

        def decorator(llm_class: Type[LLMInterface]):
            cls._llm_registry[name] = llm_class
            logger.debug(f"Registered LLM implementation: {name}")
            return llm_class

        return decorator

    @classmethod
    def available_llms(cls) -> list:
        """
        Get list of available LLM types.

        Returns:
            List of registered LLM type names
        """
        return list(cls._llm_registry.keys())

    @classmethod
    def create_llm(cls, llm_type: str, **kwargs) -> LLMInterface:
        """
        Create and return an LLM instance based on the specified type.

        Args:
            llm_type: Type of LLM to create
            **kwargs: Arguments to pass to the LLM constructor

        Returns:
            An instance of the specified LLM

        Raises:
            ValueError: If the specified LLM type is not registered
        """
        if llm_type not in cls._llm_registry:
            available = ", ".join(cls._llm_registry.keys())
            raise ValueError(f"Unknown LLM type: {llm_type}. Available types: {available}")

        try:
            return cls._llm_registry[llm_type](**kwargs)
        except Exception as e:
            logger.error(f"Failed to create {llm_type} LLM: {e}")
            raise


# Import the LLM implementations to register them
try:
    from .claude import ClaudeLLM


    @LLMFactory.register("claude")
    class RegisteredClaudeLLM(ClaudeLLM):
        pass

except ImportError:
    logger.warning("Claude support not available. Install with pip install 'mcp-panda-analyzer[claude]'")

try:
    from .openai import OpenAILLM


    @LLMFactory.register("openai")
    class RegisteredOpenAILLM(OpenAILLM):
        pass

except ImportError:
    logger.warning("OpenAI support not available. Install with pip install 'mcp-panda-analyzer[openai]'")

try:
    from .llama import LlamaLLM


    @LLMFactory.register("llama")
    class RegisteredLlamaLLM(LlamaLLM):
        pass

except ImportError:
    logger.warning("Llama support not available. Install with pip install 'mcp-panda-analyzer[llama]'")
