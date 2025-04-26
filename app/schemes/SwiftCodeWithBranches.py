from app.schemes.SwiftCodeResponse import SwiftCodeResponse
from app.schemes.SwiftCodeBranch import SwiftCodeBranch
from typing import Optional, List


class SwiftCodeWithBranches(SwiftCodeResponse):
    """
    Scheme for a headquarter Swift Code with branches
    """

    branches: Optional[List[SwiftCodeBranch]] = []
