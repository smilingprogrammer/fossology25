import re





imput_prompt = "Copyright (C) 1989, 1991 Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed."
input_prompt = "copyright  copyrightsymbol   date    date   entity     franklin street  fifth floor  boston  ma  date    date  usa everyone is permitted to copy and distribute verbatim copies of this license document  but changing it is not allowed"
exp = "copyright law: that is to say, a work containing the Program or a portion of it, either verbatim or with modifications and/or translated into another language. (Hereinafter, translation is included without limitation in the term ""modification"".) Each licensee is addressed as ""you""."

import re
from typing import List, Dict


# === Regex patterns ===

# Copyright symbols + years + holders
COPYRIGHT_RE = re.compile(
    r"""
    (?:                              # Start non-capturing group
        ©                            # Symbol ©
        | \(c\)                      # or (c)
        | copyright                  # or the word 'copyright'
    )
    [\s,:]*                          # Optional space or punctuation
    (?P<years>(\d{4})(?:[\-,–]\d{4})?(?:,\s*\d{4})*)?  # Year or range
    [\s,]*(?:by)?[\s]*               # optional 'by'
    (?P<holder>
        (?!the\s+copyright)          # negative lookahead to avoid 'the copyright law'
        (?:(?!\b(all|rights?|reserved)\b)[\w\s\.\-&(),]*){1,3}  # Try 1-3 phrases
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

# License-related phrases
LICENSE_RE = re.compile(
    r"""
    (?:
        licensed\s+under\s+(?:the\s+)?     # 'licensed under (the)?'
        (?P<license>[^.\n]+?)              # license name (up to period or newline)
        (?:\s+license)?                    # optional word 'license'
    )
    |
    (?:
        released\s+under\s+(?:the\s+)?     # 'released under ...'
        (?P<released_license>[^.\n]+?)
        (?:\s+license)?
    )
    |
    (?:
        distributed\s+under\s+(?:the\s+)?  # 'distributed under ...'
        (?P<distributed_license>[^.\n]+?)
        (?:\s+license)?
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

# === Core function ===

def declutter_text(text: str) -> Dict[str, List[Dict[str, str]]]:
    cleaned = {
        "copyrights": [],
        "licenses": []
    }

    # Normalize double quotes
    text = text.replace('“', '"').replace('”', '"')

    # Extract copyright
    for match in COPYRIGHT_RE.finditer(text):
        years = match.group("years")
        holder = match.group("holder")

        # Basic cleanup
        if holder:
            holder = holder.strip(" ,.\n").strip()
        if years:
            years = years.strip(" ,.\n").strip()

        # Only if meaningful
        if holder or years:
            cleaned["copyrights"].append({
                "year": years if years else "",
                "holder": holder if holder else ""
            })

    # Extract licenses
    for match in LICENSE_RE.finditer(text):
        for key in ["license", "released_license", "distributed_license"]:
            license_text = match.group(key)
            if license_text:
                cleaned["licenses"].append(license_text.strip(" ,.\n"))

    return cleaned



ita = declutter_text(imput_prompt)
print(ita)
