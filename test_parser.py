import pytest
from readme_parser import parse_request_into_internship, filter_active_sections

def test_parse_request_into_internship_valid_line():
    line = (
        "| **[Skydio](https://simplify.jobs/c/Skydio?utm_source=GHList&utm_medium=company)** "
        "| People Operations Software Engineer Intern | San Mateo, CA "
        "| <div align=\"center\"><a href=\"https://www.skydio.com/jobs/6585180003?gh_jid=6585180003&utm_source=Simplify&ref=Simplify\">"
        "<img src=\"https://i.imgur.com/fbjwDvo.png\" width=\"52\" alt=\"Apply\"></a> "
        "<a href=\"https://simplify.jobs/p/20c372e3-f497-4d47-ba47-ebc0c3f25753?utm_source=GHList\">"
        "<img src=\"https://i.imgur.com/aVnQdox.png\" width=\"28\" alt=\"Simplify\"></a></div> | 0d |"
    )
    job = parse_request_into_internship(line)
    assert job == {
        "Company": "Skydio",
        "Role": "People Operations Software Engineer Intern",
        "Location": "San Mateo, CA",
        "Application Link": "https://simplify.jobs/c/Skydio?utm_source=GHList&utm_medium=company"
    }

def test_filter_active_sections_skips_inactive_block():
    lines = [
        "Intro line outside table\n",
        "<summary>🗃️ Inactive roles (2)</summary>\n",
        "| **[Tinder](https://simplify.jobs/c/Tinder)** | Android Intern | NYC | 🔒 | 1d |\n",
        "<details>\n",
        "| **[Maxar](https://simplify.jobs/c/Maxar)** | Test Intern | CO | 🔒 | 3d |\n",
        "</details>\n",
        "</details>\n",
        "| **[ByteDance](https://simplify.jobs/c/ByteDance)** | Backend Intern | SF | 🔒 | 0d |\n",
        "After inactive block line\n"
    ]
    filtered = list(filter_active_sections(lines))
    assert any("Intro line outside table" in l for l in filtered)
    assert any("After inactive block line" in l for l in filtered)
    assert all("Tinder" not in l for l in filtered)
    assert all("Maxar" not in l for l in filtered)
    assert any("ByteDance" in l for l in filtered)

