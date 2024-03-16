"""Base platform."""
import dataclasses
import itertools
import re
from typing import ClassVar


@dataclasses.dataclass
class BasePlatform:
    """Base platform."""
    FORMATS: ClassVar[dict[str, str]] = {
        "file": r"git+file://%(domain)s/%(repo)s%(dot_git)s%(path_raw)s",
        "git": r"git://%(domain)s/%(repo)s%(dot_git)s%(path_raw)s",
        "git+https": r"git+https://%(domain)s/%(repo)s%(dot_git)s",
        "git+ssh": r"git+ssh://git@%(domain)s/%(repo)s%(dot_git)s%(path_raw)s",
        "https": r"https://%(domain)s/%(repo)s%(dot_git)s",
        "ssh": r"git@%(domain)s:%(repo)s%(dot_git)s%(path_raw)s",
    }

    PATTERNS: ClassVar[dict[str, str]] = {
        "file": r"(?P<protocols>(git\+)?(?P<protocol>file))://(?P<domain>.+?)"
                r"(?P<pathname>/(?P<repo>.+?)(?:\.git)?)$",
        "git": r"(?P<protocols>(?P<protocol>git))://(?P<domain>[^/]+?)/(?P<repo>.+)(?:(\.git)?(/)?)",
        "http": r"(?P<protocols>(?P<protocol>http))://(?P<domain>[^/]+?)/(?P<repo>.+)(?:(\.git)?(/)?)",
        "https": r"(?P<protocols>(?P<protocol>https))://(?P<domain>[^/]+?)/(?P<repo>.+)(?:(\.git)?(/)?)",
        "ssh": r"(?P<_user>.+)@(?P<domain>[^/]+?):(?P<repo>.+)(?:(\.git)?(/)?)",
    }

    # None means it matches all domains
    DOMAINS = None
    SKIP_DOMAINS = None
    DEFAULTS: ClassVar[dict[str, str]] = {}

    def __post_init__(self):
        """Initialize platform."""
        # Precompile PATTERNS
        self.COMPILED_PATTERNS = {proto: re.compile(regex, re.IGNORECASE) for proto, regex in self.PATTERNS.items()}

        # Supported protocols
        self.PROTOCOLS = list(self.FORMATS.keys())

        if self.__class__ == BasePlatform:
            sub = [subclass.SKIP_DOMAINS for subclass in self.__class__.__subclasses__() if subclass.SKIP_DOMAINS]
            if sub:
                self.SKIP_DOMAINS = list(itertools.chain.from_iterable(sub))

    @staticmethod
    def clean_data(data):
        """Clean data."""
        data["path"] = ""
        data["branch"] = ""
        data["protocols"] = list(filter(lambda x: x, data.get("protocols", "").split("+")))
        data["pathname"] = data.get("pathname", "").strip(":").rstrip("/")
        return data
