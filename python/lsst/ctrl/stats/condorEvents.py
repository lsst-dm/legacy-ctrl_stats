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
import re
from record import Record
from lsst.ctrl.stats import *

class CondorEvents(object):
        """
        Describes all of the Condor logging events that can happen.  Not
        All of these are used, even by Condor, but are included for
        completeness.
        """
        SubmittedEvent = "000"
        ExecutingEvent = "001"
        ExecutableErrorEvent = "002"
        CheckpointedEvent = "003"
        EvictedEvent = "004"
        TerminatedEvent = "005"
        UpdatedEvent = "006"
        ShadowExceptionEvent = "007"
        GenericEvent = "008"
        AbortedEvent = "009"
        SuspendedEvent = "010"
        UnsuspendedEvent = "011"
        HeldEvent = "012"
        ReleasedEvent = "013"
        ParallelNodeExecutedEvent = "014"
        ParallelNodeTerminatedEvent = "015"
        PostscriptTerminatedEvent = "016"
        SubmittedToGlobusEvent = "017"
        GlobusSubmitFailedEvent = "018"
        GlobusResourceUpEvent = "019"
        GlobusResourceDownEvent = "020"
        RemoteErrorEvent = "021"
        SocketLostEvent = "022"
        SocketReestablishedEvent = "023"
        SocketReconnectFailureEvent = "024"
        GridResourceUpEvent = "025"
        GridResourceDownEvent = "026"
        SubmittedToGridEvent = "027"
        JobAdInformationEvent = "028"
        JobRemoteStatusUnknownEvent = "029"
        JobRemoteStatusKnownAgainEvent = "030"
        # 031, 032 are marked as "unused" by Condor
        AttributeUpdateEvent = "033"

        events = { 
            SubmittedEvent: Submitted,
            ExecutingEvent: Executing,
            ExecutableErrorEvent: ExecutableError,
            CheckpointedEvent: Checkpointed,
            EvictedEvent: Evicted,
            TerminatedEvent: Terminated,
            UpdatedEvent: Updated,
            ShadowExceptionEvent: ShadowException,
            GenericEvent : Generic,
            AbortedEvent : Aborted,
            SuspendedEvent : Suspended,
            UnsuspendedEvent : Unsuspended,
            HeldEvent : Held,
            ReleasedEvent : Released,
            ParallelNodeExecutedEvent : ParallelNodeExecuted,
            ParallelNodeTerminatedEvent : ParallelNodeTerminated,
            PostscriptTerminatedEvent : PostscriptTerminated,
            SubmittedToGlobusEvent : SubmittedToGlobus,
            GlobusSubmitFailedEvent : GlobusSubmitFailed,
            GlobusResourceUpEvent : GlobusResourceUp,
            GlobusResourceDownEvent : GlobusResourceDown,
            RemoteErrorEvent : RemoteError,
            SocketLostEvent : SocketLost,
            SocketReestablishedEvent : SocketReestablished,
            SocketReconnectFailureEvent : SocketReconnectFailure,
            GridResourceUpEvent : GridResourceUp,
            GridResourceDownEvent : GridResourceDown,
            SubmittedToGridEvent : SubmittedToGrid,
            JobAdInformationEvent : JobAdInformation,
            JobRemoteStatusUnknownEvent : JobRemoteStatusUnknown,
            JobRemoteStatusKnownAgainEvent : JobRemoteStatusKnownAgain,
            AttributeUpdateEvent : AttributeUpdate
        }
