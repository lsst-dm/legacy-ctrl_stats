# flake8: noqa
#
# LSST Data Management System
# Copyright 2008-2012 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

from __future__ import absolute_import
from .jobAdInformation import JobAdInformation
from .jobRemoteStatusUnknown import JobRemoteStatusUnknown
from .jobRemoteStatusKnownAgain import JobRemoteStatusKnownAgain
from .attributeUpdate import AttributeUpdate
from .submitted import Submitted
from .executing import Executing
from .terminated import Terminated
from .updated import Updated
from .aborted import Aborted
from .evicted import Evicted
from .shadowException import ShadowException
from .held import Held
from .executableError import ExecutableError
from .checkpointed import Checkpointed
from .generic import Generic
from .unsuspended import Unsuspended
from .suspended import Suspended
from .released import Released
from .parallelNodeExecuted import ParallelNodeExecuted
from .parallelNodeTerminated import ParallelNodeTerminated
from .postscriptTerminated import PostscriptTerminated
from .submittedToGlobus import SubmittedToGlobus
from .globusSubmitFailed import GlobusSubmitFailed
from .globusResourceUp import GlobusResourceUp
from .globusResourceDown import GlobusResourceDown
from .remoteError import RemoteError
from .socketLost import SocketLost
from .socketReestablished import SocketReestablished
from .socketReconnectFailure import SocketReconnectFailure
from .gridResourceUp import GridResourceUp
from .gridResourceDown import GridResourceDown
from .submittedToGrid import SubmittedToGrid

import importlib
__all__ = [
    "submitted",
    "executing",
    "terminated",
    "updated",
    "aborted",
    "evicted",
    "shadowException",
    "held",
    "executableError",
    "checkpointed",
    "generic",
    "unsuspended",
    "suspended",
    "released",
    "parallelNodeExecuted",
    "parallelNodeTerminated",
    "postscriptTerminated",
    "submittedToGlobus",
    "globusSubmitFailed",
    "globusResourceUp",
    "globusResourceDown",
    "remoteError",
    "socketLost",
    "socketReestablished",
    "socketReconnectFailure",
    "gridResourceUp",
    "gridResourceDown",
    "submittedToGrid",
    "jobAdInformation",
    "jobRemoteStatusUnknown",
    "jobRemoteStatusKnownAgain",
    "attributeUpdate"
]

byCode = {}

for n in __all__:
    m = importlib.import_module("lsst.ctrl.stats.records." + n)
    byCode[m.eventCode] = m.eventClass  ## Index by number
