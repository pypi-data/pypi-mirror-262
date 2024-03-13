# Copyright 2019-2020 SURF.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict

from orchestrator.schemas.base import OrchestratorBaseModel

TagConfig = dict[str, list[dict[str, bool]]]


class FixedInputBaseSchema(OrchestratorBaseModel):
    fixed_input_id: UUID | None = None
    name: str
    value: str
    product_id: UUID | None = None


class FixedInputSchema(FixedInputBaseSchema):
    fixed_input_id: UUID
    created_at: datetime
    product_id: UUID
    model_config = ConfigDict(from_attributes=True)


class FixedInputConfigurationItemSchema(OrchestratorBaseModel):
    name: str
    description: str
    values: list[str]


class FixedInputConfigurationSchema(OrchestratorBaseModel):
    fixed_inputs: list[FixedInputConfigurationItemSchema]
    by_tag: TagConfig
