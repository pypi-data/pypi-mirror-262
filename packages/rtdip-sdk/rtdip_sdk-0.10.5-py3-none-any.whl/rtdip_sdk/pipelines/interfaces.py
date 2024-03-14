# Copyright 2022 RTDIP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
from ._pipeline_utils.models import Libraries, SystemType


class PipelineComponentBaseInterface(ABC):
    @staticmethod
    @abstractmethod
    def system_type() -> SystemType:
        pass

    @staticmethod
    @abstractmethod
    def libraries() -> Libraries:
        pass

    @staticmethod
    @abstractmethod
    def settings() -> dict:
        pass
