# -*- coding: utf-8 -*-
# Copyright European Organization for Nuclear Research (CERN) since 2012
#
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

''' remove replicas_tombstone and replicas_rse_id indexes '''

from alembic.op import create_index, drop_index

# Alembic revision identifiers
revision = '27e3a68927fb'
down_revision = '295289b5a800'


def upgrade():
    '''
    Upgrade the database to this revision
    '''

    drop_index('REPLICAS_TOMBSTONE_IDX', 'replicas')
    drop_index('REPLICAS_RSE_ID_IDX', 'replicas')


def downgrade():
    '''
    Downgrade the database to the previous revision
    '''
    create_index('REPLICAS_RSE_ID_IDX', 'replicas', ['rse_id'])
    create_index('REPLICAS_TOMBSTONE_IDX', 'replicas', ['tombstone'])
