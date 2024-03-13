"""
Copyright 2023 Impulse Innovations Limited


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Optional

from dara.core.definitions import ComponentInstance, JsComponentDef

TopBarFrameDef = JsComponentDef(name='TopBarFrame', js_module='@darajs/core', py_module='dara.core')


class TopBarFrame(ComponentInstance):
    content: ComponentInstance
    hide_logo: Optional[bool] = False
    logo_width: Optional[str] = '10rem'
    logo_path: Optional[str] = None
    logo_position: Optional[str] = None
    top_bar: Optional[ComponentInstance] = None
    top_bar_padding: Optional[str] = None
    top_bar_position: Optional[str] = None
    top_bar_height: Optional[str] = None

    class Config:
        extra = 'forbid'
